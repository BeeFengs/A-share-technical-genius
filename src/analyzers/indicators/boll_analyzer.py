"""
布林带(BOLL)指标分析模块
分析布林带的趋势和信号，提供全面的技术分析
"""
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from enum import Enum

class TrendStrength(Enum):
    VERY_STRONG = "很强"
    STRONG = "强"
    MODERATE = "中等"
    WEAK = "弱"
    VERY_WEAK = "很弱"

class BollSignal(Enum):
    STRONG_BUY = "强烈买入"
    BUY = "买入"
    HOLD = "持有"
    SELL = "卖出"
    STRONG_SELL = "强烈卖出"

def analyze_boll(df: pd.DataFrame, long_term: pd.DataFrame, medium_term: pd.DataFrame, short_term: pd.DataFrame) -> Dict[str, Any]:
    """
    全面分析布林带指标数据
    
    参数:
        df (pd.DataFrame): 完整的数据
        long_term (pd.DataFrame): 长期数据（约40个交易日）
        medium_term (pd.DataFrame): 中期数据（约20个交易日）
        short_term (pd.DataFrame): 短期数据（约10个交易日）
        
    返回:
        Dict[str, Any]: 布林带综合分析结果
    """
    latest = df.iloc[-1]
    
    # 收集各维度分析结果
    signals = {}
    
    # 1. 分析长期趋势（40天）
    signals['long_term_trend'] = _analyze_long_term_trend(long_term)
    
    # 2. 分析中期趋势（20天）
    signals['medium_term_trend'] = _analyze_medium_term_trend(medium_term)
    
    # 3. 分析短期信号（10天）
    signals['short_term_signal'] = _analyze_short_term_signal(short_term)
    
    # 4. 分析带宽
    signals['bandwidth'] = _analyze_bandwidth(medium_term)
    
    # 5. 分析布林带形态
    signals['pattern'] = _analyze_boll_pattern(short_term)
    
    # 6. 分析趋势强度
    signals['strength'] = _analyze_strength(medium_term)
    
    # 7. 生成综合信号
    signals['signal'] = _generate_composite_signal(signals)
    
    return {
        'UPPER': latest['boll_upper'],
        'MID': latest['boll_mid'],
        'LOWER': latest['boll_lower'],
        'long_term_trend': signals['long_term_trend'],
        'medium_term_trend': signals['medium_term_trend'],
        'short_term_signal': signals['short_term_signal'],
        'bandwidth': signals['bandwidth'],
        'pattern': signals['pattern'],
        'strength': signals['strength'],
        'signal': signals['signal']
    }

def _analyze_long_term_trend(data: pd.DataFrame) -> str:
    """
    分析布林带长期趋势（40天）
    """
    # 计算中轨趋势
    mid_trend = _calculate_trend_direction(data['boll_mid'])
    
    # 计算价格相对于布林带的位置
    position_ratio = (data['close'] - data['boll_lower']) / (data['boll_upper'] - data['boll_lower'])
    avg_position = position_ratio.mean()
    
    if mid_trend > 0:
        if avg_position > 0.7:
            return "强势上涨（40天）"
        else:
            return "上涨趋势（40天）"
    elif mid_trend < 0:
        if avg_position < 0.3:
            return "强势下跌（40天）"
        else:
            return "下跌趋势（40天）"
    else:
        if avg_position > 0.6:
            return "高位震荡（40天）"
        elif avg_position < 0.4:
            return "低位震荡（40天）"
        else:
            return "中位震荡（40天）"

def _analyze_medium_term_trend(data: pd.DataFrame) -> str:
    """
    分析布林带中期趋势（20天）
    """
    # 计算带宽变化趋势
    bandwidth = (data['boll_upper'] - data['boll_lower']) / data['boll_mid'] * 100
    bandwidth_trend = _calculate_trend_slope(bandwidth)
    
    # 计算中轨斜率
    mid_slope = _calculate_trend_slope(data['boll_mid'])
    
    if abs(mid_slope) < 0.1:
        if abs(bandwidth_trend) < 0.1:
            return "窄幅震荡"
        else:
            return "宽幅震荡"
    elif mid_slope > 0:
        if mid_slope > 0.3:
            return "快速上升"
        else:
            return "缓慢上升"
    else:
        if mid_slope < -0.3:
            return "快速下降"
        else:
            return "缓慢下降"

def _analyze_short_term_signal(data: pd.DataFrame) -> str:
    """
    分析布林带短期信号（10天）
    """
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    # 判断突破情况
    if latest['close'] > latest['boll_upper'] and prev['close'] <= prev['boll_upper']:
        return "突破上轨"
    elif latest['close'] < latest['boll_lower'] and prev['close'] >= prev['boll_lower']:
        return "突破下轨"
    elif latest['close'] < latest['boll_upper'] and prev['close'] >= prev['boll_upper']:
        return "回落至上轨下方"
    elif latest['close'] > latest['boll_lower'] and prev['close'] <= prev['boll_lower']:
        return "反弹至下轨上方"
    
    # 判断中轨穿越
    if latest['close'] > latest['boll_mid'] and prev['close'] <= prev['boll_mid']:
        return "突破中轨"
    elif latest['close'] < latest['boll_mid'] and prev['close'] >= prev['boll_mid']:
        return "跌破中轨"
    
    return "区间运行"

def _analyze_bandwidth(data: pd.DataFrame) -> str:
    """
    分析布林带带宽
    """
    latest = data.iloc[-1]
    recent = data.tail(5)
    
    # 计算带宽
    bandwidth = (latest['boll_upper'] - latest['boll_lower']) / latest['boll_mid'] * 100
    
    # 计算带宽变化趋势
    bandwidths = (recent['boll_upper'] - recent['boll_lower']) / recent['boll_mid'] * 100
    bandwidth_trend = '扩大' if bandwidths.is_monotonic_increasing else '收窄' if bandwidths.is_monotonic_decreasing else '平稳'
    
    if bandwidth > 4:
        return f"带宽过大（{bandwidth_trend}）"
    elif bandwidth > 3:
        return f"带宽较大（{bandwidth_trend}）"
    elif bandwidth > 2:
        return f"带宽适中（{bandwidth_trend}）"
    else:
        return f"带宽收窄（{bandwidth_trend}）"

def _analyze_boll_pattern(data: pd.DataFrame) -> str:
    """
    分析布林带形态特征
    """
    latest = data.iloc[-1]
    
    # 计算价格位置
    position = (latest['close'] - latest['boll_lower']) / (latest['boll_upper'] - latest['boll_lower'])
    
    # 计算带宽趋势
    bandwidths = (data['boll_upper'] - data['boll_lower']) / data['boll_mid'] * 100
    bandwidth_trend = _calculate_trend_direction(bandwidths)
    
    if position > 0.8 and bandwidth_trend > 0:
        return "上轨扩张"
    elif position < 0.2 and bandwidth_trend > 0:
        return "下轨扩张"
    elif position > 0.8 and bandwidth_trend < 0:
        return "上轨收敛"
    elif position < 0.2 and bandwidth_trend < 0:
        return "下轨收敛"
    elif abs(position - 0.5) < 0.1:
        return "中轨平衡"
    else:
        return "常态运行"

def _analyze_strength(data: pd.DataFrame) -> str:
    """
    分析布林带强度
    """
    latest = data.iloc[-1]
    
    # 计算标准差
    std = data['close'].std()
    
    # 计算当前带宽
    bandwidth = (latest['boll_upper'] - latest['boll_lower']) / latest['boll_mid'] * 100
    
    # 计算价格位置
    position = (latest['close'] - latest['boll_lower']) / (latest['boll_upper'] - latest['boll_lower'])
    
    if bandwidth > 4 or position > 0.9 or position < 0.1:
        return "极强" if latest['close'] > latest['boll_mid'] else "极弱"
    elif bandwidth > 3 or position > 0.8 or position < 0.2:
        return "较强" if latest['close'] > latest['boll_mid'] else "较弱"
    elif bandwidth > 2 or position > 0.7 or position < 0.3:
        return "偏强" if latest['close'] > latest['boll_mid'] else "偏弱"
    else:
        return "中性"

def _generate_composite_signal(analysis: Dict[str, str]) -> str:
    """
    生成布林带综合信号
    """
    # 获取各维度分析结果
    long_term = analysis['long_term_trend']
    medium_term = analysis['medium_term_trend']
    short_term = analysis['short_term_signal']
    bandwidth = analysis['bandwidth']
    pattern = analysis['pattern']
    strength = analysis['strength']
    
    # 生成综合信号
    signal_parts = []
    
    # 添加带宽信号
    if "过大" in bandwidth or "较大" in bandwidth:
        signal_parts.append("波动加剧")
    elif "收窄" in bandwidth:
        signal_parts.append("蓄势待发")
    
    # 添加趋势信号
    if "上涨" in long_term or "上升" in medium_term:
        if "突破上轨" in short_term or "上轨扩张" in pattern:
            signal_parts.append("多头趋势增强")
        elif "回落" in short_term:
            signal_parts.append("多头趋势减弱")
    elif "下跌" in long_term or "下降" in medium_term:
        if "突破下轨" in short_term or "下轨扩张" in pattern:
            signal_parts.append("空头趋势增强")
        elif "反弹" in short_term:
            signal_parts.append("空头趋势减弱")
    else:
        signal_parts.append("震荡整理")
    
    # 添加强度描述
    signal_parts.append(f"（{strength}）")
    
    return "，".join(signal_parts)

def _calculate_trend_direction(series: pd.Series) -> float:
    """
    计算序列的趋势方向
    """
    x = np.arange(len(series))
    slope, _ = np.polyfit(x, series, 1)
    return slope

def _calculate_trend_slope(series: pd.Series) -> float:
    """
    计算序列的斜率
    """
    x = np.arange(len(series))
    slope, _ = np.polyfit(x, series, 1)
    return slope 