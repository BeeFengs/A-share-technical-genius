"""
RSI指标分析模块
分析相对强弱指标(RSI)的趋势和信号
"""
from typing import Dict, Any
import pandas as pd
import numpy as np

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
    
    # 5. 分析RSI强度
    signals['strength'] = _analyze_strength(medium_term)
    
    # 6. 分析RSI形态
    signals['pattern'] = _analyze_rsi_pattern(short_term)
    
    # 7. 生成综合信号
    signals['signal'] = _generate_composite_signal(signals)
    
    return {
        'RSI6': latest['rsi_6'],
        'RSI12': latest['rsi_12'],
        'RSI24': latest['rsi_24'],
        'long_term_trend': signals['long_term_trend'],
        'medium_term_trend': signals['medium_term_trend'],
        'short_term_signal': signals['short_term_signal'],
        'divergence': signals['divergence'],
        'strength': signals['strength'],
        'pattern': signals['pattern'],
        'signal': signals['signal']
    }

def _analyze_long_term_trend(data: pd.DataFrame) -> str:
    """
    分析RSI长期趋势（40天）
    """
    # 计算RSI6的趋势
    rsi6_trend = _calculate_trend_direction(data['rsi_6'])
    rsi12_trend = _calculate_trend_direction(data['rsi_12'])
    rsi24_trend = _calculate_trend_direction(data['rsi_24'])
    
    # 计算RSI均值
    rsi6_mean = data['rsi_6'].mean()
    
    if rsi6_trend > 0 and rsi12_trend > 0 and rsi24_trend > 0:
        trend = "强势上涨" if rsi6_mean > 70 else "上涨趋势"
    elif rsi6_trend < 0 and rsi12_trend < 0 and rsi24_trend < 0:
        trend = "强势下跌" if rsi6_mean < 30 else "下跌趋势"
    else:
        if rsi6_mean > 60:
            trend = "高位震荡"
        elif rsi6_mean < 40:
            trend = "低位震荡"
        else:
            trend = "中位震荡"
    
    return f"{trend}（40天）"

def _analyze_medium_term_trend(data: pd.DataFrame) -> str:
    """
    分析RSI中期趋势（20天）
    """
    # 计算RSI6的趋势斜率
    slope = _calculate_trend_slope(data['rsi_6'])
    
    # 计算RSI的波动范围
    rsi_range = data['rsi_6'].max() - data['rsi_6'].min()
    
    if abs(slope) < 0.1:
        if rsi_range < 10:
            return "窄幅震荡"
        else:
            return "宽幅震荡"
    elif slope > 0:
        if slope > 0.3:
            return "快速上升"
        else:
            return "缓慢上升"
    else:
        if slope < -0.3:
            return "快速下降"
        else:
            return "缓慢下降"

def _analyze_short_term_signal(data: pd.DataFrame) -> str:
    """
    分析RSI短期信号（10天）
    """
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    # 判断RSI交叉情况
    if latest['rsi_6'] > latest['rsi_12'] and prev['rsi_6'] <= prev['rsi_12']:
        return "RSI快线上穿慢线"
    elif latest['rsi_6'] < latest['rsi_12'] and prev['rsi_6'] >= prev['rsi_12']:
        return "RSI快线下穿慢线"
    
    # 判断超买超卖区间突破
    if latest['rsi_6'] > 80 and prev['rsi_6'] <= 80:
        return "突破超买区间"
    elif latest['rsi_6'] < 20 and prev['rsi_6'] >= 20:
        return "突破超卖区间"
    elif latest['rsi_6'] < 80 and prev['rsi_6'] >= 80:
        return "离开超买区间"
    elif latest['rsi_6'] > 20 and prev['rsi_6'] <= 20:
        return "离开超卖区间"
    
    return "无明显信号"

def _analyze_divergence(data: pd.DataFrame) -> str:
    """
    分析RSI背离
    """
    # 获取价格的高点和低点
    price_highs = _find_local_extremes(data['close'], is_high=True)
    price_lows = _find_local_extremes(data['close'], is_high=False)
    
    # 获取RSI的高点和低点
    rsi_highs = _find_local_extremes(data['rsi_6'], is_high=True)
    rsi_lows = _find_local_extremes(data['rsi_6'], is_high=False)
    
    # 判断顶背离
    if len(price_highs) >= 2 and len(rsi_highs) >= 2:
        if price_highs[-1] > price_highs[-2] and rsi_highs[-1] < rsi_highs[-2]:
            return "顶背离（卖出信号）"
    
    # 判断底背离
    if len(price_lows) >= 2 and len(rsi_lows) >= 2:
        if price_lows[-1] < price_lows[-2] and rsi_lows[-1] > rsi_lows[-2]:
            return "底背离（买入信号）"
    
    return "无背离"

def _analyze_strength(data: pd.DataFrame) -> str:
    """
    分析RSI强度
    """
    latest = data.iloc[-1]
    
    # 计算RSI的标准差
    rsi_std = data['rsi_6'].std()
    
    # 计算当前RSI值与中值的偏离度
    deviation = abs(latest['rsi_6'] - 50)
    
    if deviation > 30:
        return "极强" if latest['rsi_6'] > 50 else "极弱"
    elif deviation > 20:
        return "较强" if latest['rsi_6'] > 50 else "较弱"
    elif deviation > 10:
        return "偏强" if latest['rsi_6'] > 50 else "偏弱"
    else:
        return "中性"

def _analyze_rsi_pattern(data: pd.DataFrame) -> str:
    """
    分析RSI形态特征
    """
    latest = data.iloc[-1]
    
    # 判断RSI三线位置关系
    if latest['rsi_6'] > latest['rsi_12'] > latest['rsi_24']:
        return "多头排列"
    elif latest['rsi_6'] < latest['rsi_12'] < latest['rsi_24']:
        return "空头排列"
    elif abs(latest['rsi_6'] - latest['rsi_12']) < 2 and abs(latest['rsi_12'] - latest['rsi_24']) < 2:
        return "三线平行"
    else:
        return "三线交叉"

def _generate_composite_signal(analysis: Dict[str, str]) -> str:
    """
    生成RSI综合信号
    """
    # 获取各维度分析结果
    long_term = analysis['long_term_trend']
    medium_term = analysis['medium_term_trend']
    short_term = analysis['short_term_signal']
    divergence = analysis['divergence']
    strength = analysis['strength']
    pattern = analysis['pattern']
    
    # 生成综合信号
    signal_parts = []
    
    # 添加背离信号（如果有）
    if divergence != "无背离":
        signal_parts.append(f"出现{divergence}")
    
    # 添加趋势信号
    if "上涨" in long_term or "上升" in medium_term:
        if "上穿" in short_term or "多头" in pattern:
            signal_parts.append("多头趋势增强")
        elif "下穿" in short_term:
            signal_parts.append("多头趋势减弱")
    elif "下跌" in long_term or "下降" in medium_term:
        if "下穿" in short_term or "空头" in pattern:
            signal_parts.append("空头趋势增强")
        elif "上穿" in short_term:
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