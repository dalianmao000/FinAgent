"""股票价格ARIMA预测工具."""
import os
import json
import time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from qwen_agent.tools.base import BaseTool, register_tool
from dotenv import load_dotenv

from ....tools.config import get_settings

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


@register_tool('investment_arima_prediction')
class ArimaPredictionTool(BaseTool):
    """对指定股票(ts_code)的历史价格进行ARIMA建模，预测未来n天收盘价"""
    name = 'investment_arima_prediction'
    description = '对指定股票的历史价格进行ARIMA(5,1,5)建模，预测未来n天收盘价'
    parameters = [{
        'name': 'ts_code',
        'type': 'string',
        'description': '股票代码，如600519.SH',
        'required': True
    }, {
        'name': 'n',
        'type': 'integer',
        'description': '预测天数',
        'required': True
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        ts_code = args['ts_code']
        n = int(args['n'])

        settings = get_settings()
        from sqlalchemy import create_engine
        engine = create_engine(settings.stock_db_url, connect_args={'connect_timeout': 10})

        today = datetime.now().date()
        start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
        end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')

        sql = f"""
            SELECT trade_date, close FROM stock_history_2020
            WHERE ts_code='{ts_code}' AND trade_date >= '{start_date}' AND trade_date <= '{end_date}'
            ORDER BY trade_date ASC
        """
        df = pd.read_sql(sql, engine)
        if df.empty or len(df) < 30:
            return f"数据不足，无法建模。请确认股票代码或数据量。"

        close_series = df['close'].astype(float)
        try:
            model = ARIMA(close_series, order=(5, 1, 5))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=n)

            last_date = pd.to_datetime(df['trade_date'].iloc[-1])
            pred_dates = [(last_date + timedelta(days=i + 1)).strftime('%Y-%m-%d') for i in range(n)]
            result_df = pd.DataFrame({'预测日期': pred_dates, '预测收盘价': forecast})

            plt.figure(figsize=(12, 6))
            plt.plot(df['trade_date'], close_series, label='历史收盘价')
            plt.plot(pred_dates, forecast, 'ro--', label='预测收盘价')

            all_dates = list(df['trade_date']) + pred_dates
            total_len = len(all_dates)
            max_xticks = 12
            if total_len > max_xticks:
                step = total_len // max_xticks
                xtick_idx = list(range(0, total_len, step))
                if xtick_idx[-1] != total_len - 1:
                    xtick_idx.append(total_len - 1)
                xtick_labels = [all_dates[i] for i in xtick_idx]
                plt.xticks(xtick_idx, xtick_labels, rotation=45)
            else:
                plt.xticks(rotation=45)

            plt.xlabel('日期')
            plt.ylabel('收盘价')
            plt.title(f'{ts_code} 历史与未来{n}天收盘价预测')
            plt.legend()
            plt.tight_layout()

            save_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'image_show')
            os.makedirs(save_dir, exist_ok=True)
            filename = f'arima_{ts_code}_{int(time.time() * 1000)}.png'
            save_path = os.path.join(save_dir, filename)
            plt.savefig(save_path)
            plt.close()

            img_path = os.path.join('image_show', filename)
            img_md = f'![历史与预测收盘价]({img_path})'
            return result_df.to_markdown(index=False) + '\n\n' + img_md
        except Exception as e:
            return f"ARIMA建模或预测出错: {str(e)}"
