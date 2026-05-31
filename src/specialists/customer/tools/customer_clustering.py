"""客户聚类预测工具 - KMeans."""
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from qwen_agent.tools.base import BaseTool, register_tool
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


@register_tool('customer_kmeans_clustering')
class KMeansClusteringTool(BaseTool):
    """基于KMeans模型预测客户所属分群"""
    name = 'customer_kmeans_clustering'
    description = '基于KMeans模型预测客户所属分群（高净值成熟客户、中产活跃客户、新兴潜力客户）'
    parameters = [{
        'name': 'customer_id',
        'type': 'string',
        'description': '要预测的客户ID，可以是单个客户ID或多个客户ID（用逗号分隔）',
        'required': True
    }, {
        'name': 'show_features',
        'type': 'boolean',
        'description': '是否显示客户的特征值，默认True',
        'required': False,
        'default': True
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        customer_ids = args['customer_id']
        show_features = args.get('show_features', True)

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
            'lifecycle_stage', 'marriage_status', 'city_level'
        ]]

        behavior['stat_month'] = pd.to_datetime(behavior['stat_month'], errors='coerce')
        idx = behavior.groupby('customer_id')['stat_month'].idxmax()
        behavior_latest = behavior.loc[idx]

        behavior_latest = behavior_latest[[
            'customer_id', 'total_assets', 'deposit_balance', 'financial_balance', 'fund_balance', 'insurance_balance',
            'product_count', 'financial_repurchase_count', 'credit_card_monthly_expense',
            'investment_monthly_count', 'app_login_count', 'app_financial_view_time', 'app_product_compare_count'
        ]]

        all_data = base.merge(behavior_latest, on='customer_id', how='inner')

        cat_cols = ['gender', 'occupation', 'occupation_type', 'lifecycle_stage', 'marriage_status', 'city_level']
        label_encoders = {}
        for col in cat_cols:
            le = LabelEncoder()
            all_data[col] = le.fit_transform(all_data[col].astype(str))
            label_encoders[col] = le

        cluster_features = [
            'age', 'gender', 'occupation', 'occupation_type', 'monthly_income',
            'lifecycle_stage', 'marriage_status', 'city_level',
            'total_assets', 'deposit_balance', 'financial_balance', 'fund_balance', 'insurance_balance',
            'product_count', 'financial_repurchase_count', 'credit_card_monthly_expense',
            'investment_monthly_count', 'app_login_count', 'app_financial_view_time', 'app_product_compare_count'
        ]
        X = all_data[cluster_features]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=3, random_state=42)
        all_data['cluster'] = kmeans.fit_predict(X_scaled)

        target_customers = all_data[all_data['customer_id'].isin(customer_id_list)]

        if target_customers.empty:
            return f"未找到客户ID: {customer_ids} 的数据"

        cluster_means = all_data.groupby('cluster')[cluster_features].mean()

        cluster_names = {}
        cluster_descriptions = {}

        for cluster_id in cluster_means.index:
            means = cluster_means.loc[cluster_id]
            total_assets_avg = means['total_assets']
            monthly_income_avg = means['monthly_income']
            age_avg = means['age']

            if total_assets_avg >= 1500000:
                cluster_names[cluster_id] = "高净值成熟客户"
                cluster_descriptions[cluster_id] = {
                    "特征": f"资产高（平均{total_assets_avg/10000:.0f}万）、收入高（平均{monthly_income_avg/10000:.1f}万/月）",
                    "业务建议": "重点维护，定制高端理财、私行服务，提供专属客户经理"
                }
            elif total_assets_avg >= 400000:
                cluster_names[cluster_id] = "中产活跃客户"
                cluster_descriptions[cluster_id] = {
                    "特征": f"资产中等（平均{total_assets_avg/10000:.0f}万）、收入中等（平均{monthly_income_avg/10000:.1f}万/月）",
                    "业务建议": "推介理财、基金、保险等多元产品，提升复购率和资产沉淀"
                }
            else:
                cluster_names[cluster_id] = "新兴潜力客户"
                cluster_descriptions[cluster_id] = {
                    "特征": f"资产较低（平均{total_assets_avg/10000:.0f}万）、收入较低（平均{monthly_income_avg/10000:.1f}万/月）",
                    "业务建议": "重点激活，推送基础理财、APP活动、投资教育引导"
                }

        results = []
        gender_map = {0: '女', 1: '男'}

        for _, customer in target_customers.iterrows():
            cluster_id = customer['cluster']
            cluster_name = cluster_names[cluster_id]
            description = cluster_descriptions[cluster_id]

            result_text = f"### 客户 {customer['customer_id']} 预测结果\n"
            result_text += f"**分群**: {cluster_name} (Cluster {cluster_id})\n\n"
            result_text += f"**群体特征**: {description['特征']}\n\n"
            result_text += f"**业务建议**: {description['业务建议']}\n\n"

            if show_features:
                result_text += "**客户特征值**:\n"
                result_text += f"- 年龄: {customer['age']}岁\n"
                gender_decoded = gender_map.get(customer['gender'], '未知')
                result_text += f"- 性别: {gender_decoded}\n"
                result_text += f"- 月收入: {customer['monthly_income']:.2f}元\n"
                result_text += f"- 总资产: {customer['total_assets']:.2f}元\n"
                result_text += f"- 产品数量: {customer['product_count']}个\n\n"

            results.append(result_text)

        if len(customer_id_list) > 1:
            predictions = target_customers['cluster'].values
            cluster_counts = pd.Series(predictions).value_counts().sort_index()
            summary = "\n### 分群统计\n"
            for cluster_id, count in cluster_counts.items():
                summary += f"- {cluster_names[cluster_id]}: {count}人\n"
            results.append(summary)

        overall_summary = "\n### 全体客户分群概况\n"
        overall_counts = all_data['cluster'].value_counts().sort_index()
        for cluster_id, count in overall_counts.items():
            pct = count / len(all_data) * 100
            overall_summary += f"- {cluster_names[cluster_id]}: {count}人 ({pct:.1f}%)\n"
        results.append(overall_summary)

        return "\n".join(results)
