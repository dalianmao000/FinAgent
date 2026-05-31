"""LightGBM资产预测与SHAP解释工具."""
import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from qwen_agent.tools.base import BaseTool, register_tool
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


@register_tool('customer_lightgbm_prediction')
class LightGBMAssetPredictionTool(BaseTool):
    """LightGBM预测客户未来3个月资产100万+概率"""
    name = 'customer_lightgbm_prediction'
    description = 'LightGBM预测客户未来3个月资产100万+概率，提供SHAP解释和业务建议'
    parameters = [{
        'name': 'customer_id',
        'type': 'string',
        'description': '要预测的客户ID，可以是单个客户ID或多个客户ID（用逗号分隔）',
        'required': True
    }, {
        'name': 'show_shap_detail',
        'type': 'boolean',
        'description': '是否显示详细的SHAP解释图表，默认True',
        'required': False,
        'default': True
    }, {
        'name': 'min_history_months',
        'type': 'integer',
        'description': '最少历史月数要求，默认9个月',
        'required': False,
        'default': 9
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        customer_ids = args['customer_id']
        show_shap_detail = args.get('show_shap_detail', True)
        min_history_months = int(args.get('min_history_months', 9))

        if ',' in customer_ids:
            customer_id_list = [cid.strip() for cid in customer_ids.split(',')]
        else:
            customer_id_list = [customer_ids.strip()]

        from ....tools.config import get_settings
        settings = get_settings()
        from sqlalchemy import create_engine
        engine = create_engine(settings.customer_db_url, connect_args={'connect_timeout': 10})

        base = pd.read_sql('SELECT * FROM enterprise_credit_clients.customer_base', engine)
        behavior = pd.read_sql('SELECT * FROM enterprise_credit_clients.customer_behavior_assets', engine)

        base = base[[
            'customer_id', 'age', 'gender', 'occupation', 'occupation_type', 'monthly_income',
            'open_account_date', 'lifecycle_stage', 'marriage_status', 'city_level', 'branch_name'
        ]]

        behavior['stat_month'] = pd.to_datetime(behavior['stat_month'], errors='coerce')
        behavior = behavior.dropna(subset=['stat_month'])
        behavior = behavior.sort_values(['customer_id', 'stat_month'])

        behavior['month_rank'] = behavior.groupby('customer_id')['stat_month'].rank(method='first', ascending=False)
        behavior_feature = behavior[behavior['month_rank'] > 3]
        behavior_target = behavior[behavior['month_rank'] <= 3]

        def get_target(df):
            return int((df['total_assets'] >= 1e6).any())

        target = behavior_target.groupby('customer_id').apply(get_target).reset_index()
        target.columns = ['customer_id', 'target']

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

        cat_cols = ['gender', 'occupation', 'occupation_type', 'lifecycle_stage', 'marriage_status', 'city_level']
        label_encoders = {}
        for col in cat_cols:
            le = LabelEncoder()
            model_data[col] = le.fit_transform(model_data[col].astype(str))
            label_encoders[col] = le

        model_data = model_data.fillna(0)

        X = model_data.drop(['customer_id', 'target', 'open_account_date', 'branch_name'], axis=1)
        y = model_data['target']

        categorical_features = [X.columns.get_loc(col) for col in cat_cols]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        import lightgbm as lgb
        lgb_train = lgb.Dataset(X_train, y_train, categorical_feature=categorical_features)
        lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train, categorical_feature=categorical_features)
        params = {
            'objective': 'binary',
            'metric': 'auc',
            'boosting_type': 'gbdt',
            'learning_rate': 0.05,
            'num_leaves': 31,
            'max_depth': -1,
            'verbose': -1,
            'seed': 42
        }
        gbm = lgb.train(params, lgb_train, num_boost_round=100, valid_sets=[lgb_train, lgb_eval])

        y_prob_test = gbm.predict(X_test, num_iteration=gbm.best_iteration)
        auc = roc_auc_score(y_test, y_prob_test)
        acc = accuracy_score(y_test, (y_prob_test > 0.5).astype(int))

        target_customers = model_data[model_data['customer_id'].isin(customer_id_list)]
        if target_customers.empty:
            return f"未找到客户ID: {customer_ids} 的数据"

        for cid in customer_id_list:
            cust_behavior = behavior[behavior['customer_id'] == cid]
            if len(cust_behavior) < min_history_months:
                return f"客户 {cid} 历史数据不足（需要至少{min_history_months}个月，实际{len(cust_behavior)}个月）"

        X_pred = target_customers[X.columns]
        predictions = gbm.predict(X_pred, num_iteration=gbm.best_iteration)

        results = []
        results.append("## LightGBM资产预测分析")
        results.append(f"**模型性能**: AUC={auc:.4f}, 准确率={acc:.4f}")

        img_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'image_show')
        os.makedirs(img_dir, exist_ok=True)

        for i, (_, customer) in enumerate(target_customers.iterrows()):
            customer_id = customer['customer_id']
            pred_prob = predictions[i]

            results.append(f"\n### 客户 {customer_id} 预测结果")
            results.append(f"**预测概率**: {pred_prob:.4f} ({pred_prob * 100:.2f}%)")

            if pred_prob >= 0.7:
                risk_level = "高概率"
                advice = "建议优先关注，提供高端产品和服务"
            elif pred_prob >= 0.3:
                risk_level = "中等概率"
                advice = "建议重点培养，推荐理财和投资产品"
            else:
                risk_level = "低概率"
                advice = "建议基础维护，提供教育和引导服务"

            results.append(f"**风险等级**: {risk_level}")
            results.append(f"**业务建议**: {advice}")
            results.append(f"\n**客户信息**:")
            results.append(f"- 年龄: {customer['age']}岁")
            results.append(f"- 月收入: {customer['monthly_income']:,.2f}元")

            lifecycle_decoded = "未知"
            try:
                lifecycle_decoded = label_encoders['lifecycle_stage'].inverse_transform([customer['lifecycle_stage']])[0]
            except:
                pass
            results.append(f"- 生命周期: {lifecycle_decoded}")
            results.append(f"- 产品数量均值: {customer['product_count_mean']:.1f}个")

            if show_shap_detail and i == 0:
                try:
                    import shap
                    single_X = X_pred.iloc[[i]]
                    explainer = shap.TreeExplainer(gbm)
                    shap_values = explainer.shap_values(single_X)

                    if isinstance(shap_values, list):
                        single_shap_vec = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
                        expected_value = explainer.expected_value[1] if hasattr(explainer.expected_value, '__len__') else explainer.expected_value
                    else:
                        single_shap_vec = shap_values[0]
                        expected_value = explainer.expected_value

                    plt.figure(figsize=(10, 8))
                    shap.plots._waterfall.waterfall_legacy(
                        expected_value, single_shap_vec, single_X.iloc[0],
                        max_display=10, show=False
                    )
                    plt.title(f'客户 {customer_id} SHAP解释瀑布图')
                    plt.tight_layout()
                    waterfall_path = os.path.join(img_dir, f'shap_waterfall_{customer_id}_{int(time.time() * 1000)}.png')
                    plt.savefig(waterfall_path)
                    plt.close()

                    results.append(f"\n![SHAP瀑布图]({os.path.join('image_show', os.path.basename(waterfall_path))})")

                except Exception as e:
                    results.append(f"\n### SHAP分析出错: {str(e)}")

        if len(customer_id_list) > 1:
            results.append(f"\n### 批量预测汇总")
            high_prob = sum(1 for p in predictions if p >= 0.7)
            medium_prob = sum(1 for p in predictions if 0.3 <= p < 0.7)
            low_prob = sum(1 for p in predictions if p < 0.3)

            results.append(f"- **高概率客户**: {high_prob}人 ({high_prob / len(predictions) * 100:.1f}%)")
            results.append(f"- **中等概率客户**: {medium_prob}人 ({medium_prob / len(predictions) * 100:.1f}%)")
            results.append(f"- **低概率客户**: {low_prob}人 ({low_prob / len(predictions) * 100:.1f}%)")
            results.append(f"- **平均预测概率**: {np.mean(predictions):.4f}")

        return "\n".join(results)
