"""
KDJ指标分析模块
分析KDJ指标的趋势和信号
"""
from typing import Dict, Any
import pandas as pd
import numpy as np

def analyze_kdj(df: pd.DataFrame, long_term: pd.DataFrame, medium_term: pd.DataFrame, short_term: pd.DataFrame) -> Dict[str, Any]:
    """
    分析KDJ指标数据
    
    参数:
        df (pd.DataFrame): 完整的数据
        long_term (pd.DataFrame): 长期数据（约40个交易日）
        medium_term (pd.DataFrame): 中期数据（约20个交易日）
        short_term (pd.DataFrame): 短期数据（约10个交易日）
        
    返回:
        Dict[str, Any]: KDJ分析结果
    """
    latest = df.iloc[-1]
    
    # 分析各个时间维度的趋势
    long_trend = _analyze_kdj_trend(long_term, "long")
    medium_trend = _analyze_kdj_trend(medium_term, "medium")
    short_trend = _analyze_kdj_trend(short_term, "short")
    
    # 分析KDJ三线交叉形态
    cross_pattern = _analyze_cross_pattern(short_term)
    
    # 分析背离
    divergence = _analyze_divergence(medium_term)
    
    # 分析KDJ指标强度
    strength = _analyze_strength(medium_term)
    
    # 分析KDJ形态
    pattern = _analyze_kdj_pattern(short_term)
    
    # 生成综合信号
    signal = _generate_composite_signal(long_trend, medium_trend, short_trend, cross_pattern, divergence)
    
    return {
        'K': latest['kdj_k'],
        'D': latest['kdj_d'],
        'J': latest['kdj_j'],
        'long_term_trend': long_trend,
        'medium_term_trend': medium_trend,
        'short_term_trend': short_trend,
        'cross_pattern': cross_pattern,
        'divergence': divergence,
        'strength': strength,
        'pattern': pattern,
        'signal': signal
    }

def _analyze_kdj_trend(data: pd.DataFrame, timeframe: str) -> str:
    """
    分析KDJ趋势
    
    参数:
        data (pd.DataFrame): 价格数据
        timeframe (str): 时间维度（long/medium/short）
        
    返回:
        str: KDJ趋势分析结果
    """
    latest = data.iloc[-1]
    
    # 计算KDJ区间
    k_mean = data['kdj_k'].mean()
    k_std = data['kdj_k'].std()
    
    # 计算KDJ趋势斜率
    k_slope = (data['kdj_k'].iloc[-1] - data['kdj_k'].iloc[0]) / len(data)
    d_slope = (data['kdj_d'].iloc[-1] - data['kdj_d'].iloc[0]) / len(data)
    j_slope = (data['kdj_j'].iloc[-1] - data['kdj_j'].iloc[0]) / len(data)
    
    # 判断超买超卖
    if latest['kdj_j'] > 100:
        strength = '强烈' if latest['kdj_j'] > 110 else '一般'
        trend = f'{strength}超买'
    elif latest['kdj_j'] < 0:
        strength = '强烈' if latest['kdj_j'] < -10 else '一般'
        trend = f'{strength}超卖'
    elif latest['kdj_k'] > k_mean + k_std:
        if k_slope > 0 and d_slope > 0 and j_slope > 0:
            trend = '强势上涨'
        else:
            trend = '偏多'
    elif latest['kdj_k'] < k_mean - k_std:
        if k_slope < 0 and d_slope < 0 and j_slope < 0:
            trend = '强势下跌'
        else:
            trend = '偏空'
    else:
        if abs(k_slope) < 0.1 and abs(d_slope) < 0.1:
            trend = '盘整'
        else:
            trend = '震荡'
            
    return trend

def _analyze_cross_pattern(data: pd.DataFrame) -> str:
    """
    分析KDJ三线交叉形态
    """
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    # 判断金叉死叉
    if latest['kdj_k'] > latest['kdj_d'] and prev['kdj_k'] <= prev['kdj_d']:
        if latest['kdj_j'] > latest['kdj_k']:
            return "黄金交叉（J线确认）"
        else:
            return "黄金交叉"
    elif latest['kdj_k'] < latest['kdj_d'] and prev['kdj_k'] >= prev['kdj_d']:
        if latest['kdj_j'] < latest['kdj_k']:
            return "死亡交叉（J线确认）"
        else:
            return "死亡交叉"
    elif abs(latest['kdj_k'] - latest['kdj_d']) < 1:
        return "交叉临界"
    else:
        return "无交叉信号"

def _analyze_divergence(data: pd.DataFrame) -> str:
    """
    分析KDJ指标与价格的背离情况
    """
    # 获取最高价和最低价的位置
    price_highs = data['close'].rolling(window=5, center=True).max()
    price_lows = data['close'].rolling(window=5, center=True).min()
    
    # 获取KDJ的高点和低点
    kdj_highs = data['kdj_k'].rolling(window=5, center=True).max()
    kdj_lows = data['kdj_k'].rolling(window=5, center=True).min()
    
    # 判断顶背离
    if (price_highs.iloc[-1] > price_highs.iloc[-5] and 
        kdj_highs.iloc[-1] < kdj_highs.iloc[-5]):
        return "顶背离"
    # 判断底背离
    elif (price_lows.iloc[-1] < price_lows.iloc[-5] and 
          kdj_lows.iloc[-1] > kdj_lows.iloc[-5]):
        return "底背离"
    else:
        return "无背离"

def _analyze_strength(data: pd.DataFrame) -> str:
    """
    分析KDJ指标强度
    """
    latest = data.iloc[-1]
    
    # 计算KDJ指标的标准差
    k_std = data['kdj_k'].std()
    d_std = data['kdj_d'].std()
    j_std = data['kdj_j'].std()
    
    # 计算当前值与均值的偏离程度
    k_dev = abs(latest['kdj_k'] - data['kdj_k'].mean()) / k_std
    d_dev = abs(latest['kdj_d'] - data['kdj_d'].mean()) / d_std
    j_dev = abs(latest['kdj_j'] - data['kdj_j'].mean()) / j_std
    
    # 判断强度
    avg_dev = (k_dev + d_dev + j_dev) / 3
    if avg_dev > 2:
        return "极强"
    elif avg_dev > 1.5:
        return "较强"
    elif avg_dev > 1:
        return "中等"
    else:
        return "较弱"

def _analyze_kdj_pattern(data: pd.DataFrame) -> str:
    """
    分析KDJ形态特征
    """
    latest = data.iloc[-1]
    
    # 判断三线位置关系
    if latest['kdj_j'] > latest['kdj_k'] > latest['kdj_d']:
        return "多头排列"
    elif latest['kdj_j'] < latest['kdj_k'] < latest['kdj_d']:
        return "空头排列"
    elif abs(latest['kdj_k'] - latest['kdj_d']) < 2:
        return "平行排列"
    else:
        return "发散排列"

def _generate_composite_signal(long_trend: str, medium_trend: str, short_trend: str, 
                             cross_pattern: str, divergence: str) -> str:
    """
    生成综合信号
    """
    # 根据不同时间维度的趋势和信号生成综合判断
    if "超买" in long_trend or "超买" in medium_trend:
        if "死亡交叉" in cross_pattern or "顶背离" in divergence:
            return "强烈卖出"
        else:
            return "谨慎持有"
    elif "超卖" in long_trend or "超卖" in medium_trend:
        if "黄金交叉" in cross_pattern or "底背离" in divergence:
            return "强烈买入"
        else:
            return "谨慎买入"
    elif "强势上涨" in short_trend:
        if "顶背离" in divergence:
            return "高位观望"
        else:
            return "持续做多"
    elif "强势下跌" in short_trend:
        if "底背离" in divergence:
            return "低位介入"
        else:
            return "持续观望"
    else:
        return "观望等待" 