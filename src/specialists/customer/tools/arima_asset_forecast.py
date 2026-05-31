"""ARIMA资产预测工具."""
import json
import os
import time

import matplotlib.pyplot as plt
import pandas as pd
from qwen_agent.tools.base import BaseTool, register_tool
from statsmodels.tsa.arima.model import ARIMA

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


@register_tool('customer_arima_asset_forecast')
class ARIMAAssetForecastTool(BaseTool):
    """基于ARIMA模型预测整体资产或单客户的未来资产变化"""
    name = 'customer_arima_asset_forecast'
    description = '基于ARIMA模型预测整体资产或单客户的未来n个月资产变化，生成预测图表'
    parameters = [{
        'name': 'forecast_type',
        'type': 'string',
        'description': '预测类型：total(整体资产), customer(单客户资产)',
        'required': False,
        'default': 'total'
    }, {
        'name': 'customer_id',
        'type': 'string',
        'description': '客户ID（当forecast_type为customer时必填）',
        'required': False
    }, {
        'name': 'forecast_months',
        'type': 'integer',
        'description': '预测未来月数，默认3个月',
        'required': False,
        'default': 3
    }, {
        'name': 'min_history_months',
        'type': 'integer',
        'description': '最少历史月数要求，默认6个月',
        'required': False,
        'default': 6
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        forecast_type = args.get('forecast_type', 'total')
        customer_id = args.get('customer_id', None)
        forecast_months = int(args.get('forecast_months', 3))
        min_history_months = int(args.get('min_history_months', 6))

        from ....tools.config import get_settings
        settings = get_settings()
        from sqlalchemy import create_engine
        engine = create_engine(settings.customer_db_url, connect_args={'connect_timeout': 10})

        behavior = pd.read_sql('SELECT customer_id, stat_month, total_assets FROM enterprise_credit_clients.customer_behavior_assets', engine)

        behavior['stat_month'] = pd.to_datetime(behavior['stat_month'], errors='coerce')
        behavior = behavior.dropna(subset=['stat_month'])
        behavior = behavior.sort_values(['customer_id', 'stat_month'])

        img_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'image_show')
        os.makedirs(img_dir, exist_ok=True)

        if forecast_type == 'customer':
            if not customer_id:
                return "错误：预测单客户时必须提供customer_id参数"

            customer_data = behavior[behavior['customer_id'] == customer_id].copy()

            if customer_data.empty:
                return f"错误：未找到客户ID {customer_id} 的数据"

            if len(customer_data) < min_history_months:
                return f"错误：客户 {customer_id} 历史数据不足（需要至少{min_history_months}个月，实际{len(customer_data)}个月）"

            customer_data = customer_data.set_index('stat_month').sort_index()
            series = customer_data['total_assets']

            model = ARIMA(series, order=(0, 1, 0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=forecast_months)

            img_path = os.path.join(img_dir, f'customer_{customer_id}_forecast_{int(time.time() * 1000)}.png')
            plt.figure(figsize=(10, 6))
            plt.plot(series.index, series.values, label='历史资产', color='blue', linewidth=2)

            pred_dates = [series.index.max() + pd.DateOffset(months=i + 1) for i in range(forecast_months)]
            plt.plot(pred_dates, forecast, label='预测资产', color='red', linestyle='--', marker='o', linewidth=2)

            plt.title(f'客户 {customer_id} 资产预测（未来{forecast_months}个月）')
            plt.xlabel('月份')
            plt.ylabel('总资产（元）')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(img_path)
            plt.close()

            result = [f"## 客户 {customer_id} 资产预测分析"]
            result.append(f"\n- 数据期间: {series.index.min().strftime('%Y-%m')} ~ {series.index.max().strftime('%Y-%m')}")
            result.append(f"- 历史月数: {len(series)}个月")
            result.append(f"- 最新资产: {series.iloc[-1]:,.2f}元")
            result.append(f"\n### 未来{forecast_months}个月预测")
            for i, (date, value) in enumerate(zip(pred_dates, forecast)):
                change_pct = ((value - series.iloc[-1]) / series.iloc[-1]) * 100
                result.append(f"- {date.strftime('%Y-%m')}: {value:,.2f}元 ({change_pct:+.1f}%)")

            img_md = f'![客户资产预测图]({os.path.join("image_show", os.path.basename(img_path))})'
            result.append(f"\n{img_md}")

            return "\n".join(result)

        else:
            monthly_total = behavior.groupby(behavior['stat_month'].dt.to_period('M'))['total_assets'].sum()
            monthly_total.index = monthly_total.index.to_timestamp()
            monthly_total = monthly_total.sort_index()

            if len(monthly_total) < min_history_months:
                return f"错误：整体数据历史不足（需要至少{min_history_months}个月，实际{len(monthly_total)}个月）"

            model = ARIMA(monthly_total, order=(0, 1, 0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=forecast_months)

            img_path = os.path.join(img_dir, f'total_assets_forecast_{int(time.time() * 1000)}.png')
            plt.figure(figsize=(12, 6))
            plt.plot(monthly_total.index, monthly_total.values, label='历史AUM', color='blue', linewidth=2)

            pred_dates = [monthly_total.index.max() + pd.DateOffset(months=i + 1) for i in range(forecast_months)]
            plt.plot(pred_dates, forecast, label='预测AUM', color='red', linestyle='--', marker='o', linewidth=2)

            plt.title(f'全体客户AUM预测（未来{forecast_months}个月）')
            plt.xlabel('月份')
            plt.ylabel('资产管理规模 AUM（元）')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(img_path)
            plt.close()

            result = [f"## 全体客户AUM预测分析"]
            result.append(f"- 数据期间: {monthly_total.index.min().strftime('%Y-%m')} ~ {monthly_total.index.max().strftime('%Y-%m')}")
            result.append(f"- 历史月数: {len(monthly_total)}个月")
            result.append(f"- 最新AUM: {monthly_total.iloc[-1]:,.2f}元")
            result.append(f"- 客户总数: {behavior['customer_id'].nunique()}位")
            result.append(f"\n### 未来{forecast_months}个月AUM预测")
            for i, (date, value) in enumerate(zip(pred_dates, forecast)):
                change_pct = ((value - monthly_total.iloc[-1]) / monthly_total.iloc[-1]) * 100
                result.append(f"- {date.strftime('%Y-%m')}: {value:,.2f}元 ({change_pct:+.1f}%)")

            img_md = f'![整体AUM预测图]({os.path.join("image_show", os.path.basename(img_path))})'
            result.append(f"\n{img_md}")

            return "\n".join(result)
