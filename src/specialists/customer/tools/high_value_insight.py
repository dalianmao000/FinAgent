"""高价值用户画像工具 - 逻辑回归预测未来3个月资产100万+."""
import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from qwen_agent.tools.base import BaseTool, register_tool
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


@register_tool('customer_high_value_insight')
class HighValueUserInsightTool(BaseTool):
    """逻辑回归预测未来3个月资产100万+，输出高价值用户画像"""
    name = 'customer_high_value_insight'
    description = '逻辑回归预测未来3个月资产100万+，输出高价值用户画像或者主要特征及可视化'
    parameters = [{
        'name': 'stat_month',
        'type': 'string',
        'description': '分析截止月份（YYYY-MM），默认2025-05',
        'required': False
    }, {
        'name': 'min_months',
        'type': 'integer',
        'description': '最少历史月数，默认9',
        'required': False,
        'default': 9
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        stat_month = args.get('stat_month', None)
        min_months = int(args.get('min_months', 9))

        from ....tools.config import get_settings
        settings = get_settings()
        from sqlalchemy import create_engine
        engine = create_engine(settings.customer_db_url, connect_args={'connect_timeout': 10})

        base = pd.read_sql('SELECT * FROM enterprise_credit_clients.customer_base', engine)
        behavior = pd.read_sql('SELECT * FROM enterprise_credit_clients.customer_behavior_assets', engine)

        behavior['stat_month'] = pd.to_datetime(behavior['stat_month'], errors='coerce')
        behavior = behavior.dropna(subset=['stat_month'])
        if stat_month:
            end_month = pd.to_datetime(stat_month)
            behavior = behavior[behavior['stat_month'] <= end_month]

        counts = behavior.groupby('customer_id').size()
        valid_ids = counts[counts >= min_months].index
        behavior = behavior[behavior['customer_id'].isin(valid_ids)]

        behavior = behavior.sort_values(['customer_id', 'stat_month'])
        behavior['month_rank'] = behavior.groupby('customer_id')['stat_month'].rank(method='first', ascending=False)
        behavior_feature = behavior[behavior['month_rank'] > 3]
        behavior_target = behavior[behavior['month_rank'] <= 3]

        def get_target(df):
            return int((df['total_assets'] >= 1e6).any())

        target = behavior_target.groupby('customer_id').apply(get_target).reset_index(name='target')

        feature_cols = ['product_count', 'financial_repurchase_count', 'credit_card_monthly_expense',
                        'investment_monthly_count', 'app_login_count', 'app_financial_view_time',
                        'app_product_compare_count']

        def get_features(df):
            feats = {}
            for col in feature_cols:
                feats[f'{col}_mean'] = df[col].mean()
            return pd.Series(feats)

        features = behavior_feature.groupby('customer_id').apply(get_features).reset_index()
        model_data = features.merge(target, on='customer_id', how='inner')
        model_data = model_data.merge(base, on='customer_id', how='left')

        model_data['gender'] = model_data['gender'].map({'男': 1, '女': 0})
        model_data = pd.get_dummies(model_data, columns=['occupation', 'occupation_type', 'lifecycle_stage', 'marriage_status', 'city_level'], drop_first=True)
        model_data = model_data.fillna(0)

        X = model_data.drop(['customer_id', 'target', 'open_account_date', 'branch_name', 'name'], axis=1, errors='ignore')
        X = X.select_dtypes(include=[np.number, bool])
        y = model_data['target']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        lr = LogisticRegression(max_iter=1000)
        lr.fit(X_train_scaled, y_train)
        y_pred = lr.predict(X_test_scaled)
        y_prob = lr.predict_proba(X_test_scaled)[:, 1]
        auc = roc_auc_score(y_test, y_prob)

        coef = lr.coef_[0]
        feature_names = X.columns
        coef_df = pd.DataFrame({'feature': feature_names, 'coef': coef})
        coef_df_top15 = coef_df.reindex(coef_df['coef'].abs().sort_values(ascending=False).index).head(15)
        coef_md = coef_df_top15.to_markdown(index=False)

        y_all_pred = lr.predict(scaler.transform(X))
        model_data['pred'] = y_all_pred
        high_value = model_data[model_data['pred'] == 1]

        img_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'image_show')
        os.makedirs(img_dir, exist_ok=True)

        feat_imp_path = os.path.join(img_dir, f'customer_high_value_{int(time.time() * 1000)}.png')
        plt.figure(figsize=(8, 6))
        bar_colors = ['#377eb8' if v >= 0 else '#e41a1c' for v in coef_df_top15['coef']]
        import seaborn as sns
        sns.barplot(x='coef', y='feature', data=coef_df_top15, palette=bar_colors, orient='h')
        plt.xlabel('系数')
        plt.title('特征重要性Top15（正蓝负红）')
        plt.tight_layout()
        plt.savefig(feat_imp_path)
        plt.close()
        feat_imp_md = f'![特征重要性]({os.path.join("image_show", os.path.basename(feat_imp_path))})'

        result = f"### 逻辑回归AUC: {auc:.4f}\n\n### 主要特征系数（Top15）\n{coef_md}\n\n{feat_imp_md}"

        high_value_count = len(high_value)
        total_count = len(model_data)
        result += f"\n\n### 高价值用户统计\n- 高价值用户: {high_value_count}人 ({high_value_count/total_count*100:.1f}%)\n- 全体客户: {total_count}人"

        return result
