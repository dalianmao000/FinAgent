"""SQL查询工具 - 执行SQL并自动可视化."""
import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from qwen_agent.tools.base import BaseTool, register_tool

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def auto_generate_chart(df_sql, save_path):
    """根据数据自动选择柱状图或折线图，trade_date自动排序和稀疏显示."""
    columns = df_sql.columns

    if 'trade_date' in df_sql.columns:
        df_sql = df_sql.sort_values('trade_date')

    x_col = 'trade_date' if 'trade_date' in df_sql.columns else df_sql.columns[0]
    x = df_sql[x_col]

    is_occupation_chart = any('职业' in str(col) for col in columns) or any('occupation' in str(col).lower() for col in columns)

    object_columns = df_sql.select_dtypes(include='O').columns.tolist()
    if columns[0] in object_columns:
        object_columns.remove(columns[0])
    num_columns = df_sql.select_dtypes(exclude='O').columns.tolist()

    plt.figure(figsize=(12, 8) if is_occupation_chart else (10, 6))

    if len(object_columns) > 0:
        pivot_df = df_sql.pivot_table(index=columns[0], columns=object_columns, values=num_columns, fill_value=0)

        if is_occupation_chart:
            bottoms = None
            for col in pivot_df.columns:
                plt.barh(range(len(pivot_df)), pivot_df[col], left=bottoms, label=str(col))
                if bottoms is None:
                    bottoms = pivot_df[col].copy()
                else:
                    bottoms += pivot_df[col]
            plt.yticks(range(len(pivot_df)), pivot_df.index, fontsize=10)
            plt.ylabel(columns[0])
        else:
            bottoms = None
            for col in pivot_df.columns:
                plt.bar(pivot_df.index, pivot_df[col], bottom=bottoms, label=str(col))
                if bottoms is None:
                    bottoms = pivot_df[col].copy()
                else:
                    bottoms += pivot_df[col]
            plt.xticks(rotation=45)
            plt.xlabel(columns[0])
    else:
        if is_occupation_chart:
            bottom = np.zeros(len(df_sql))
            for column in columns[1:]:
                plt.barh(x, df_sql[column], left=bottom, label=column)
                bottom += df_sql[column]
            plt.yticks(x, df_sql[columns[0]], fontsize=10)
            plt.ylabel(columns[0])
        else:
            bottom = np.zeros(len(df_sql))
            for column in columns[1:]:
                plt.bar(x, df_sql[column], bottom=bottom, label=column)
                bottom += df_sql[column]
            plt.xticks(rotation=45)
            plt.xlabel(columns[0])

    plt.ylabel("数值")
    plt.legend()
    plt.title("客户经营数据统计")
    plt.tight_layout()

    total_len = len(x)
    max_xticks = 12
    if total_len > max_xticks:
        step = total_len // max_xticks
        xtick_idx = list(range(0, total_len, step))
        if xtick_idx[-1] != total_len - 1:
            xtick_idx.append(total_len - 1)
        xtick_labels = [x.iloc[i] if hasattr(x, 'iloc') else x[i] for i in xtick_idx]
        plt.xticks(xtick_idx, xtick_labels, rotation=60)

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


@register_tool('customer_execute_sql')
class ExecuteSQLTool(BaseTool):
    """SQL查询工具，执行SQL并自动可视化"""
    name = 'customer_execute_sql'
    description = '执行SQL查询客户数据，并自动进行可视化'
    parameters = [{
        'name': 'sql_input',
        'type': 'string',
        'description': '完整的SQL查询语句',
        'required': True
    }, {
        'name': 'need_visualize',
        'type': 'boolean',
        'description': '是否需要可视化，默认True',
        'required': False,
        'default': True
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        sql_input = args['sql_input']
        need_visualize = args.get('need_visualize', True)

        from ....tools.config import get_settings
        settings = get_settings()
        from sqlalchemy import create_engine
        engine = create_engine(settings.customer_db_url, connect_args={'connect_timeout': 10})

        try:
            df = pd.read_sql(sql_input, engine)
            md = df.to_markdown(index=False)

            if len(df) == 1 or not need_visualize:
                return md

            desc_md = df.describe().to_markdown()

            img_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'image_show')
            os.makedirs(img_dir, exist_ok=True)
            filename = f'chart_{int(time.time() * 1000)}.png'
            save_path = os.path.join(img_dir, filename)

            auto_generate_chart(df, save_path)
            img_path = os.path.join('image_show', filename)
            img_md = f'![数据可视化]({img_path})'

            return f"{md}\n\n{desc_md}\n\n{img_md}"

        except Exception as e:
            return f"SQL执行或可视化出错: {str(e)}"
