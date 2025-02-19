"""
技术指标分析模块
包含各种技术指标的分析逻辑
"""
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

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
    latest = df.iloc[-1]       # 最新一天
    
    analysis = {}
    
    # MACD全面分析
    macd_analysis = _analyze_macd_comprehensive(df, long_term, medium_term, short_term)
    analysis['MACD'] = {
        'DIF': latest['macd_dif'],
        'DEA': latest['macd_dea'],
        'MACD': latest['macd'],
        'long_term_trend': macd_analysis['long_term_trend'],
        'medium_term_trend': macd_analysis['medium_term_trend'],
        'short_term_signal': macd_analysis['short_term_signal'],
        'divergence': macd_analysis['divergence'],
        'strength': macd_analysis['strength'],
        'signal': macd_analysis['signal']
    }
    
    # KDJ分析
    analysis['KDJ'] = {
        'K': latest['kdj_k'],
        'D': latest['kdj_d'],
        'J': latest['kdj_j'],
        'signal': _analyze_kdj_trend(medium_term)
    }
    
    # RSI分析
    analysis['RSI'] = {
        'RSI6': latest['rsi_6'],
        'RSI12': latest['rsi_12'],
        'RSI24': latest['rsi_24'],
        'signal': _analyze_rsi_trend(medium_term)
    }
    
    # BOLL分析
    analysis['BOLL'] = {
        'UPPER': latest['boll_upper'],
        'MID': latest['boll_mid'],
        'LOWER': latest['boll_lower'],
        'signal': _analyze_boll_trend(medium_term)
    }
    
    return analysis

def _analyze_macd_comprehensive(df: pd.DataFrame, 
                              long_term: pd.DataFrame,
                              medium_term: pd.DataFrame, 
                              short_term: pd.DataFrame) -> Dict[str, str]:
    """
    全面分析MACD指标
    
    参数:
        df (pd.DataFrame): 完整的历史数据
        long_term (pd.DataFrame): 长期数据（约40天）
        medium_term (pd.DataFrame): 中期数据（约20天）
        short_term (pd.DataFrame): 短期数据（约10天）
        
    返回:
        Dict[str, str]: 包含多个维度的MACD分析结果
    """
    result = {}
    
    # 1. 分析长期趋势（40天）
    result['long_term_trend'] = _analyze_macd_long_term_trend(long_term)
    
    # 2. 分析中期趋势（20天）
    result['medium_term_trend'] = _analyze_macd_medium_term_trend(medium_term)
    
    # 3. 分析短期信号（10天）
    result['short_term_signal'] = _analyze_macd_short_term_signal(short_term)
    
    # 4. 分析背离
    result['divergence'] = _analyze_macd_divergence(long_term)
    
    # 5. 分析MACD强度
    result['strength'] = _analyze_macd_strength(medium_term)
    
    # 6. 生成综合信号
    result['signal'] = _generate_macd_composite_signal(result)
    
    return result

def _analyze_macd_long_term_trend(data: pd.DataFrame) -> str:
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

def _analyze_macd_medium_term_trend(data: pd.DataFrame) -> str:
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

def _analyze_macd_short_term_signal(data: pd.DataFrame) -> str:
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

def _analyze_macd_divergence(data: pd.DataFrame) -> str:
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

def _analyze_macd_strength(data: pd.DataFrame) -> str:
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

def _generate_macd_composite_signal(analysis: Dict[str, str]) -> str:
    """
    生成MACD综合信号
    """
    # 根据各维度分析结果生成综合信号
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

def _analyze_kdj_trend(data: pd.DataFrame) -> str:
    """
    分析KDJ趋势
    
    参数:
        data (pd.DataFrame): 最近的价格数据
        
    返回:
        str: KDJ趋势分析结果
    """
    latest = data.iloc[-1]
    
    # 计算KDJ区间
    k_mean = data['kdj_k'].mean()
    k_std = data['kdj_k'].std()
    
    # 判断超买超卖
    if latest['kdj_j'] > 100:
        strength = '强烈' if latest['kdj_j'] > 110 else '一般'
        return f'{strength}超买'
    elif latest['kdj_j'] < 0:
        strength = '强烈' if latest['kdj_j'] < -10 else '一般'
        return f'{strength}超卖'
    elif latest['kdj_k'] > k_mean + k_std:
        return '偏多'
    elif latest['kdj_k'] < k_mean - k_std:
        return '偏空'
    else:
        return '盘整'

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