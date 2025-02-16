"""
可视化模块 - 负责生成技术指标图表
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List

class TechnicalVisualizer:
    @staticmethod
    def plot_indicators(df: pd.DataFrame, stock_name: str) -> go.Figure:
        """
        绘制技术指标图表
        
        参数:
            df (pd.DataFrame): 包含技术指标的DataFrame
            stock_name (str): 股票名称
            
        返回:
            go.Figure: Plotly图表对象
        """
        # 创建子图
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('K线图 & BOLL', 'MACD', 'KDJ', 'RSI'),
            row_heights=[0.4, 0.2, 0.2, 0.2]
        )

        # 添加K线图
        fig.add_trace(
            go.Candlestick(
                x=df['trade_date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='K线'
            ),
            row=1, col=1
        )

        # 添加BOLL线
        fig.add_trace(
            go.Scatter(
                x=df['trade_date'],
                y=df['boll_upper'],
                name='BOLL上轨',
                line=dict(color='gray', dash='dash')
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=df['trade_date'],
                y=df['boll_mid'],
                name='BOLL中轨',
                line=dict(color='gray')
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=df['trade_date'],
                y=df['boll_lower'],
                name='BOLL下轨',
                line=dict(color='gray', dash='dash')
            ),
            row=1, col=1
        )

        # 添加MACD
        fig.add_trace(
            go.Bar(
                x=df['trade_date'],
                y=df['macd'],
                name='MACD柱',
                marker_color=df['macd'].apply(lambda x: 'red' if x > 0 else 'green')
            ),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['trade_date'], y=df['macd_dif'], name='DIF',
                      line=dict(color='blue')),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['trade_date'], y=df['macd_dea'], name='DEA',
                      line=dict(color='orange')),
            row=2, col=1
        )

        # 添加KDJ
        fig.add_trace(
            go.Scatter(x=df['trade_date'], y=df['kdj_k'], name='K值',
                      line=dict(color='blue')),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['trade_date'], y=df['kdj_d'], name='D值',
                      line=dict(color='orange')),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['trade_date'], y=df['kdj_j'], name='J值',
                      line=dict(color='purple')),
            row=3, col=1
        )

        # 添加RSI
        fig.add_trace(
            go.Scatter(x=df['trade_date'], y=df['rsi_6'], name='RSI6',
                      line=dict(color='blue')),
            row=4, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['trade_date'], y=df['rsi_12'], name='RSI12',
                      line=dict(color='orange')),
            row=4, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['trade_date'], y=df['rsi_24'], name='RSI24',
                      line=dict(color='purple')),
            row=4, col=1
        )

        # 更新布局
        fig.update_layout(
            title=f'{stock_name} 技术指标分析',
            xaxis_title='日期',
            height=1200,
            showlegend=True,
            template='plotly_white'
        )

        # 添加RSI参考线
        fig.add_hline(y=80, line_dash="dash", line_color="red", row=4, col=1)
        fig.add_hline(y=20, line_dash="dash", line_color="green", row=4, col=1)

        return fig 