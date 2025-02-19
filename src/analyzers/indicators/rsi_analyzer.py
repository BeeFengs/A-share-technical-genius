"""
RSI指标分析模块
分析相对强弱指标(RSI)的趋势和信号
"""
from typing import Dict, Any
import pandas as pd

def analyze_rsi(df: pd.DataFrame, long_term: pd.DataFrame, medium_term: pd.DataFrame, short_term: pd.DataFrame) -> Dict[str, Any]:
    """
    分析RSI指标数据
    
    参数:
        df (pd.DataFrame): 完整的数据
        long_term (pd.DataFrame): 长期数据（约40个交易日）
        medium_term (pd.DataFrame): 中期数据（约20个交易日）
        short_term (pd.DataFrame): 短期数据（约10个交易日）
        
    返回:
        Dict[str, Any]: RSI分析结果
    """
    latest = df.iloc[-1]
    
    return {
        'RSI6': latest['rsi_6'],
        'RSI12': latest['rsi_12'],
        'RSI24': latest['rsi_24'],
        'signal': _analyze_rsi_trend(medium_term)
    }

def _analyze_rsi_trend(data: pd.DataFrame) -> str:
    """
    分析RSI趋势
    
    参数:
        data (pd.DataFrame): 最近的价格数据
        
    返回:
        str: RSI趋势分析结果
    """
    latest = data.iloc[-1]
    
    # 分析RSI趋势
    rsi6_trend = data['rsi_6'].tail(5)
    trend = '上升' if rsi6_trend.is_monotonic_increasing else '下降' if rsi6_trend.is_monotonic_decreasing else '震荡'
    
    # 判断超买超卖
    if latest['rsi_6'] > 80:
        return f'超买（{trend}趋势）'
    elif latest['rsi_6'] < 20:
        return f'超卖（{trend}趋势）'
    elif latest['rsi_6'] > 60:
        return f'偏强（{trend}趋势）'
    elif latest['rsi_6'] < 40:
        return f'偏弱（{trend}趋势）'
    else:
        return f'盘整（{trend}趋势）' 