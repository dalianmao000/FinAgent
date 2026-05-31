"""股票布林带异常检测工具."""
import os
import json
import time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from qwen_agent.tools.base import BaseTool, register_tool

from ....tools.config import get_settings

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


@register_tool('investment_boll_detection')
class BollDetectionTool(BaseTool):
    """对指定股票的历史价格进行布林带异常点检测"""
    name = 'investment_boll_detection'
    description = '对指定股票(ts_code)的历史价格进行布林带(Boll,20,2σ)异常点检测，输出超买/超卖日期及图表'
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
        if df.empty or len(df) < 21:
            return f"数据不足，无法检测。请确认股票代码或数据量。"

        df['close'] = df['close'].astype(float)
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['STD20'] = df['close'].rolling(window=20).std()
        df['UPPER'] = df['MA20'] + 2 * df['STD20']
        df['LOWER'] = df['MA20'] - 2 * df['STD20']

        overbought = df[df['close'] > df['UPPER']][['trade_date', 'close']]
        oversold = df[df['close'] < df['LOWER']][['trade_date', 'close']]

        plt.figure(figsize=(12, 6))
        plt.plot(df['trade_date'], df['close'], label='收盘价')
        plt.plot(df['trade_date'], df['MA20'], label='MA20')
        plt.plot(df['trade_date'], df['UPPER'], 'g--', label='上轨(+2σ)')
        plt.plot(df['trade_date'], df['LOWER'], 'r--', label='下轨(-2σ)')
        plt.scatter(overbought['trade_date'], overbought['close'], color='red', marker='^', label='超买')
        plt.scatter(oversold['trade_date'], oversold['close'], color='blue', marker='v', label='超卖')

        all_dates = list(df['trade_date'])
        total_len = len(all_dates)
        max_xticks = 12
        if total_len > max_xticks:
            step = total_len // max_xticks
            xtick_idx = list(range(0, total_len, step))
            if xtick_idx[-1] != total_len - 1:
                xtick_idx.append(total_len - 1)
            xtick_labels = [all_dates[i] for i in xtick_idx]
            plt.xticks(xtick_idx, xtick_labels, rotation=60)
        else:
            plt.xticks(rotation=45)

        plt.xlabel('日期')
        plt.ylabel('收盘价')
        plt.title(f'{ts_code} {start_date}~{end_date} 布林带异常点检测')
        plt.legend()
        plt.tight_layout()

        save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'image_show')
        os.makedirs(save_dir, exist_ok=True)
        filename = f'boll_{ts_code}_{int(time.time() * 1000)}.png'
        save_path = os.path.join(save_dir, filename)
        plt.savefig(save_path)
        plt.close()

        img_path = os.path.join('image_show', filename)
        img_md = f'![布林带异常点检测]({img_path})'

        result = f'### 超买点（收盘价>上轨）\n' + (overbought.to_markdown(index=False) if not overbought.empty else '无')
        result += f'\n\n### 超卖点（收盘价<下轨）\n' + (oversold.to_markdown(index=False) if not oversold.empty else '无')
        result += f'\n\n{img_md}'
        return result
