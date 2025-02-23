"""
技术指标分析模块
包含各种技术指标的分析逻辑
"""
from typing import Dict, Any
import pandas as pd
from .indicators import analyze_macd
from .indicators.kdj_analyzer import analyze_kdj
from .indicators.rsi_analyzer import analyze_rsi
from .indicators.boll_analyzer import analyze_boll
from .indicators.ma_system_analyzer import analyze_ma_system
from .indicators.candlestick_analyzer import analyze_candlesticks

def analyze_indicators(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    分析技术指标数据，使用历史数据进行更全面的分析
    
    参数:
        df (pd.DataFrame): 包含技术指标数据的DataFrame
        
    返回:
        Dict[str, Dict[str, Any]]: 各个技术指标的分析结果
    """
    # 使用不同的时间窗口进行分析
    long_term = df.tail(40)    # 约2个月的交易日
    medium_term = df.tail(20)  # 约1个月的交易日
    short_term = df.tail(10)   # 约2周的交易日
    
    analysis = {}
    
    # MACD分析
    analysis['MACD'] = analyze_macd(df, long_term, medium_term, short_term)
    
    # KDJ分析
    analysis['KDJ'] = analyze_kdj(df, long_term, medium_term, short_term)
    
    # RSI分析
    analysis['RSI'] = analyze_rsi(df, long_term, medium_term, short_term)
    
    # BOLL分析
    analysis['BOLL'] = analyze_boll(df, long_term, medium_term, short_term)
    
    # MA系统分析
    analysis['MA'] = analyze_ma_system(df, long_term, medium_term, short_term)
    
    # K线形态分析
    analysis['Candlestick'] = analyze_candlesticks(df, long_term, medium_term, short_term)
    
    return analysis 