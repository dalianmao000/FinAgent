"""产品关联规则分析工具 - Apriori."""
import json

import matplotlib.pyplot as plt
import pandas as pd
from qwen_agent.tools.base import BaseTool, register_tool

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


@register_tool('customer_product_association')
class ProductAssociationRulesTool(BaseTool):
    """基于Apriori算法挖掘产品关联规则"""
    name = 'customer_product_association'
    description = '基于Apriori算法挖掘产品关联规则，分析产品组合模式'
    parameters = [{
        'name': 'analysis_type',
        'type': 'string',
        'description': '分析类型：frequent_items(频繁项集), rules(关联规则), all(全部)',
        'required': False,
        'default': 'all'
    }, {
        'name': 'target_product',
        'type': 'string',
        'description': '目标产品：存款、理财、基金、保险',
        'required': False
    }, {
        'name': 'min_confidence',
        'type': 'number',
        'description': '最小置信度阈值(0-1)',
        'required': False,
        'default': 0.1
    }, {
        'name': 'min_lift',
        'type': 'number',
        'description': '最小提升度阈值(>1)',
        'required': False,
        'default': 1.0
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        analysis_type = args.get('analysis_type', 'all')
        target_product = args.get('target_product', None)
        min_confidence = float(args.get('min_confidence', 0.1))
        min_lift = float(args.get('min_lift', 1.0))

        from ....tools.config import get_settings
        settings = get_settings()
        from sqlalchemy import create_engine
        engine = create_engine(settings.customer_db_url, connect_args={'connect_timeout': 10})

        behavior = pd.read_sql('SELECT * FROM enterprise_credit_clients.customer_behavior_assets', engine)

        product_flags = ['deposit_flag', 'financial_flag', 'fund_flag', 'insurance_flag']
        product_map = {
            'deposit_flag': '存款',
            'financial_flag': '理财',
            'fund_flag': '基金',
            'insurance_flag': '保险'
        }

        behavior['stat_month'] = pd.to_datetime(behavior['stat_month'], errors='coerce')
        behavior = behavior.sort_values(['customer_id', 'stat_month'], ascending=[True, False])
        latest = behavior.groupby('customer_id').head(1)

        basket = latest[product_flags].copy()
        basket = basket.applymap(lambda x: 1 if x == 1 else 0)
        basket.columns = [product_map[c] for c in basket.columns]

        from mlxtend.frequent_patterns import apriori, association_rules

        min_support = 0.05
        frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)

        if len(frequent_itemsets) > 0:
            rules = association_rules(frequent_itemsets, metric='lift', min_threshold=min_lift)
            filtered_rules = rules[rules['confidence'] >= min_confidence].sort_values(['lift', 'confidence'], ascending=False)
        else:
            rules = pd.DataFrame()
            filtered_rules = pd.DataFrame()

        frequent_itemsets['items_count'] = frequent_itemsets['itemsets'].apply(len)
        frequent_itemsets['items_str'] = frequent_itemsets['itemsets'].apply(lambda x: ', '.join(sorted(x)))

        if not filtered_rules.empty:
            filtered_rules['antecedents_str'] = filtered_rules['antecedents'].apply(lambda x: ', '.join(sorted(x)))
            filtered_rules['consequents_str'] = filtered_rules['consequents'].apply(lambda x: ', '.join(sorted(x)))
            filtered_rules['rule_str'] = filtered_rules['antecedents_str'] + ' → ' + filtered_rules['consequents_str']

        results = []

        if analysis_type in ['frequent_items', 'all']:
            results.append("## 频繁项集分析")

            single_items = frequent_itemsets[frequent_itemsets['items_count'] == 1].sort_values('support', ascending=False)
            if not single_items.empty:
                results.append("\n### 单产品持有率")
                single_table = single_items[['items_str', 'support']].copy()
                single_table.columns = ['产品名称', '持有率']
                single_table['持有率'] = single_table['持有率'].apply(lambda x: f"{x:.1%}")
                results.append(single_table.to_markdown(index=False))

            combo_items = frequent_itemsets[frequent_itemsets['items_count'] > 1].sort_values('support', ascending=False)
            if not combo_items.empty:
                results.append("\n### 产品组合持有率")
                combo_table = combo_items[['items_str', 'support']].copy()
                combo_table.columns = ['产品组合', '持有率']
                combo_table['持有率'] = combo_table['持有率'].apply(lambda x: f"{x:.1%}")
                results.append(combo_table.to_markdown(index=False))

        if analysis_type in ['rules', 'all']:
            results.append("\n## 关联规则分析")

            if not filtered_rules.empty:
                rule_table = filtered_rules.head(10)[['rule_str', 'confidence', 'lift', 'support']].copy()
                rule_table.columns = ['关联规则', '置信度', '提升度', '支持度']
                rule_table['置信度'] = rule_table['置信度'].apply(lambda x: f"{x:.1%}")
                rule_table['提升度'] = rule_table['提升度'].apply(lambda x: f"{x:.2f}")
                rule_table['支持度'] = rule_table['支持度'].apply(lambda x: f"{x:.1%}")
                results.append(rule_table.to_markdown(index=False))
            else:
                results.append("无满足条件的关联规则")

        if target_product and not filtered_rules.empty:
            results.append(f"\n## 基于【{target_product}】的关联分析")
            target_rules = filtered_rules[
                filtered_rules['antecedents_str'].str.contains(target_product, na=False)
            ].head(5)

            if not target_rules.empty:
                target_table = target_rules[['rule_str', 'confidence', 'lift', 'support']].copy()
                target_table.columns = ['关联规则', '置信度', '提升度', '支持度']
                target_table['置信度'] = target_table['置信度'].apply(lambda x: f"{x:.1%}")
                target_table['提升度'] = target_table['提升度'].apply(lambda x: f"{x:.2f}")
                target_table['支持度'] = target_table['支持度'].apply(lambda x: f"{x:.1%}")
                results.append(target_table.to_markdown(index=False))
            else:
                results.append(f"无基于【{target_product}】的关联规则")

        return "\n".join(results)
