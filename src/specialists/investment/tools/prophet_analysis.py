"""股票Prophet周期性分析工具."""
import os
import json
import time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
from qwen_agent.tools.base import BaseTool, register_tool

from ....tools.config import get_settings

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


@register_tool('investment_prophet_analysis')
class ProphetAnalysisTool(BaseTool):
    """对指定股票的历史价格用prophet进行周期性分析"""
    name = 'investment_prophet_analysis'
    description = '对指定股票(ts_code)的历史价格用prophet进行周期性分析，输出趋势、周、年分解图'
    parameters = [{
        'name': 'ts_code',
        'type': 'string',
        'description': '股票代码，必填',
        'required': True
    }, {
        'name': 'start_date',
        'type': 'string',
        'description': '起始日期，格式YYYY-MM-DD，可选，默认过去一年',
        'required': False
    }, {
        'name': 'end_date',
        'type': 'string',
        'description': '结束日期，格式YYYY-MM-DD，可选，默认昨天',
        'required': False
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        ts_code = args['ts_code']
        today = datetime.now().date()

        if 'start_date' in args and args['start_date']:
            start_date = args['start_date']
        else:
            start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
        if 'end_date' in args and args['end_date']:
            end_date = args['end_date']
        else:
            end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')

        settings = get_settings()
        from sqlalchemy import create_engine
        engine = create_engine(settings.stock_db_url, connect_args={'connect_timeout': 10})

        sql = f"""
            SELECT trade_date, close FROM stock_history_2020
            WHERE ts_code='{ts_code}' AND trade_date >= '{start_date}' AND trade_date <= '{end_date}'
            ORDER BY trade_date ASC
        """
        df = pd.read_sql(sql, engine)
        if df.empty or len(df) < 30:
            return f"数据不足，无法分析。请确认股票代码或数据量。"

        df['ds'] = pd.to_datetime(df['trade_date'])
        df['y'] = df['close'].astype(float)

        m = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        m.fit(df[['ds', 'y']])
        future = m.make_future_dataframe(periods=0)
        forecast = m.predict(future)

        fig = m.plot_components(forecast)
        plt.suptitle(f'{ts_code} {start_date}~{end_date} 周期性分解', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'image_show')
        os.makedirs(save_dir, exist_ok=True)
        filename = f'prophet_{ts_code}_{int(time.time() * 1000)}.png'
        save_path = os.path.join(save_dir, filename)
        fig.savefig(save_path)
        plt.close(fig)

        img_path = os.path.join('image_show', filename)
        img_md = f'![Prophet周期性分解]({img_path})'
        return img_md
