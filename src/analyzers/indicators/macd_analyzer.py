"""
MACD指标分析器
包含MACD指标的所有分析逻辑
"""
from typing import Dict, Any
import pandas as pd
import numpy as np

def analyze_macd(df: pd.DataFrame, 
                long_term: pd.DataFrame,
                medium_term: pd.DataFrame, 
                short_term: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    全面分析MACD指标
    
    参数:
        df (pd.DataFrame): 完整的历史数据
        long_term (pd.DataFrame): 长期数据（约40天）
        medium_term (pd.DataFrame): 中期数据（约20天）
        short_term (pd.DataFrame): 短期数据（约10天）
        
    返回:
        Dict[str, Dict[str, Any]]: 包含信号分析和指标数据的字典
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
    
    # 4. 分析背离
    signals['divergence'] = _analyze_divergence(long_term)
    
    # 5. 分析MACD强度
    signals['strength'] = _analyze_strength(medium_term)
    
    # 6. 生成综合信号
    signals['signal'] = _generate_composite_signal(signals)
    
    # 返回完整的分析结果
    return {
        'DIF': latest['macd_dif'],
        'DEA': latest['macd_dea'],
        'MACD': latest['macd'],
        'long_term_trend': signals['long_term_trend'],
        'medium_term_trend': signals['medium_term_trend'],
        'short_term_signal': signals['short_term_signal'],
        'divergence': signals['divergence'],
        'strength': signals['strength'],
        'signal': signals['signal']
    }

def _analyze_long_term_trend(data: pd.DataFrame) -> str:
    """
    分析MACD长期趋势（40天）
    """
    # 计算DIF和DEA的趋势
    dif_trend = _calculate_trend_direction(data['macd_dif'])
    dea_trend = _calculate_trend_direction(data['macd_dea'])
    
    # 计算MACD柱状量的累计值
    macd_sum = data['macd'].sum()
    
    if dif_trend > 0 and dea_trend > 0:
        trend = "强势上涨" if macd_sum > 0 else "上涨趋势转弱"
    elif dif_trend < 0 and dea_trend < 0:
        trend = "强势下跌" if macd_sum < 0 else "下跌趋势转弱"
    else:
        trend = "震荡整理"
        
    return f"{trend}（40天）"

def _analyze_medium_term_trend(data: pd.DataFrame) -> str:
    """
    分析MACD中期趋势（20天）
    """
    # 计算最近20天的MACD柱状趋势
    recent_macd = data['macd']
    
    # 计算趋势的斜率
    slope = _calculate_trend_slope(recent_macd)
    
    # 判断趋势强度
    if abs(slope) < 0.1:
        return "横盘震荡"
    elif slope > 0:
        return "上升趋势" if slope > 0.3 else "弱势上涨"
    else:
        return "下降趋势" if slope < -0.3 else "弱势下跌"

def _analyze_short_term_signal(data: pd.DataFrame) -> str:
    """
    分析MACD短期信号（10天）
    """
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    # 判断金叉死叉
    if latest['macd_dif'] > latest['macd_dea'] and prev['macd_dif'] <= prev['macd_dea']:
        return "金叉信号"
    elif latest['macd_dif'] < latest['macd_dea'] and prev['macd_dif'] >= prev['macd_dea']:
        return "死叉信号"
    
    # 判断MACD柱状的变化
    if latest['macd'] > 0 and latest['macd'] > prev['macd']:
        return "红柱放大"
    elif latest['macd'] > 0 and latest['macd'] < prev['macd']:
        return "红柱缩小"
    elif latest['macd'] < 0 and latest['macd'] < prev['macd']:
        return "绿柱放大"
    elif latest['macd'] < 0 and latest['macd'] > prev['macd']:
        return "绿柱缩小"
    
    return "无明显信号"

def _analyze_divergence(data: pd.DataFrame) -> str:
    """
    分析MACD背离
    """
    # 获取价格的高点和低点
    price_highs = _find_local_extremes(data['close'], is_high=True)
    price_lows = _find_local_extremes(data['close'], is_high=False)
    
    # 获取MACD的高点和低点
    macd_highs = _find_local_extremes(data['macd'], is_high=True)
    macd_lows = _find_local_extremes(data['macd'], is_high=False)
    
    # 判断顶背离
    if len(price_highs) >= 2 and len(macd_highs) >= 2:
        if price_highs[-1] > price_highs[-2] and macd_highs[-1] < macd_highs[-2]:
            return "顶背离"
    
    # 判断底背离
    if len(price_lows) >= 2 and len(macd_lows) >= 2:
        if price_lows[-1] < price_lows[-2] and macd_lows[-1] > macd_lows[-2]:
            return "底背离"
    
    return "无背离"

def _analyze_strength(data: pd.DataFrame) -> str:
    """
    分析MACD强度
    """
    latest = data.iloc[-1]
    
    # 计算MACD柱状量的标准差
    macd_std = data['macd'].std()
    
    # 判断当前MACD柱状量的强度
    current_strength = abs(latest['macd'])
    
    if current_strength > 2 * macd_std:
        return "极强" if latest['macd'] > 0 else "极弱"
    elif current_strength > macd_std:
        return "较强" if latest['macd'] > 0 else "较弱"
    else:
        return "普通"

def _generate_composite_signal(analysis: Dict[str, str]) -> str:
    """
    生成MACD综合信号
    """
    # 获取各维度分析结果
    long_term = analysis['long_term_trend']
    medium_term = analysis['medium_term_trend']
    short_term = analysis['short_term_signal']
    divergence = analysis['divergence']
    strength = analysis['strength']
    
    # 生成综合信号
    signal_parts = []
    
    # 添加背离信号（如果有）
    if divergence != "无背离":
        signal_parts.append(f"出现{divergence}")
    
    # 添加趋势信号
    if "上涨" in long_term or "上升" in medium_term:
        if "金叉" in short_term or "红柱" in short_term:
            signal_parts.append("多头趋势增强")
        elif "死叉" in short_term or "绿柱" in short_term:
            signal_parts.append("多头趋势减弱")
    elif "下跌" in long_term or "下降" in medium_term:
        if "死叉" in short_term or "绿柱" in short_term:
            signal_parts.append("空头趋势增强")
        elif "金叉" in short_term or "红柱" in short_term:
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

def _find_local_extremes(series: pd.Series, is_high: bool = True) -> list:
    """
    找出序列的局部极值点
    """
    extremes = []
    for i in range(1, len(series)-1):
        if is_high:
            if series[i] > series[i-1] and series[i] > series[i+1]:
                extremes.append(series[i])
        else:
            if series[i] < series[i-1] and series[i] < series[i+1]:
                extremes.append(series[i])
    return extremes 