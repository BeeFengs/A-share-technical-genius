"""
布林带(BOLL)指标分析模块
分析布林带的趋势和信号
"""
from typing import Dict, Any
import pandas as pd

def analyze_boll(df: pd.DataFrame, long_term: pd.DataFrame, medium_term: pd.DataFrame, short_term: pd.DataFrame) -> Dict[str, Any]:
    """
    分析布林带指标数据
    
    参数:
        df (pd.DataFrame): 完整的数据
        long_term (pd.DataFrame): 长期数据（约40个交易日）
        medium_term (pd.DataFrame): 中期数据（约20个交易日）
        short_term (pd.DataFrame): 短期数据（约10个交易日）
        
    返回:
        Dict[str, Any]: 布林带分析结果
    """
    latest = df.iloc[-1]
    
    return {
        'UPPER': latest['boll_upper'],
        'MID': latest['boll_mid'],
        'LOWER': latest['boll_lower'],
        'signal': _analyze_boll_trend(medium_term)
    }

def _analyze_boll_trend(data: pd.DataFrame) -> str:
    """
    分析布林带趋势
    
    参数:
        data (pd.DataFrame): 最近的价格数据
        
    返回:
        str: 布林带趋势分析结果
    """
    latest = data.iloc[-1]
    recent = data.tail(5)  # 最近5天数据
    
    # 计算布林带宽度趋势
    band_widths = (recent['boll_upper'] - recent['boll_lower']) / recent['boll_mid'] * 100
    bandwidth_trend = '扩大' if band_widths.is_monotonic_increasing else '收窄' if band_widths.is_monotonic_decreasing else '平稳'
    
    # 分析价格位置
    if latest['close'] > latest['boll_upper']:
        return f'突破上轨（带宽{bandwidth_trend}）'
    elif latest['close'] < latest['boll_lower']:
        return f'突破下轨（带宽{bandwidth_trend}）'
    elif latest['close'] > latest['boll_mid']:
        return f'运行于上轨区间（带宽{bandwidth_trend}）'
    else:
        return f'运行于下轨区间（带宽{bandwidth_trend}）' 