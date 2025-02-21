"""
均线系统分析器
用于分析股票的各种均线指标，包括：
1. 均线交叉信号
2. 均线排列形态
3. 趋势判断
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

def analyze_ma_system(df: pd.DataFrame,
                     long_term: pd.DataFrame,
                     medium_term: pd.DataFrame,
                     short_term: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    全面分析均线系统
    
    参数:
        df (pd.DataFrame): 完整的历史数据
        long_term (pd.DataFrame): 长期数据（约250天）
        medium_term (pd.DataFrame): 中期数据（约60天）
        short_term (pd.DataFrame): 短期数据（约20天）
        
    返回:
        Dict[str, Dict[str, Any]]: 包含信号分析和指标数据的字典
    """
    latest = df.iloc[-1]
    ma_columns = [
        'ma_qfq_5', 'ma_qfq_10', 'ma_qfq_20',
        'ma_qfq_30', 'ma_qfq_60', 'ma_qfq_90', 'ma_qfq_250'
    ]
    
    # 1. 分析长期趋势（250天）
    long_term_trend = _analyze_long_term_trend(long_term, ma_columns)
    
    # 2. 分析中期趋势（60天）
    medium_term_trend = _analyze_medium_term_trend(medium_term, ma_columns)
    
    # 3. 分析短期信号（20天）
    short_term_signal = _analyze_short_term_signal(short_term, ma_columns)
    
    # 4. 分析均线形态
    formation = _analyze_formation(df, ma_columns)
    
    # 5. 分析均线强度
    strength = _analyze_strength(medium_term, ma_columns)
    
    # 6. 分析支撑阻力位
    support_resistance = _analyze_support_resistance(df, ma_columns)
    
    # 7. 生成综合信号
    signal = _generate_composite_signal({
        'long_term_trend': long_term_trend,
        'medium_term_trend': medium_term_trend,
        'short_term_signal': short_term_signal,
        'formation': formation,
        'strength': strength
    })
    
    # 返回完整的分析结果
    return {
        'ma_values': {col: latest[col] for col in ma_columns},
        'signals': {
            'long_term_trend': long_term_trend,
            'medium_term_trend': medium_term_trend,
            'short_term_signal': short_term_signal,
            'formation': formation,
            'strength': strength,
            'support_resistance': support_resistance,
            'signal': signal
        }
    }

def _analyze_long_term_trend(data: pd.DataFrame, ma_columns: list) -> Dict[str, Any]:
    """
    分析均线长期趋势（250天）
    """
    # 计算主要均线的趋势
    ma250_trend = _calculate_trend_direction(data['ma_qfq_250'])
    ma60_trend = _calculate_trend_direction(data['ma_qfq_60'])
    
    # 判断长期趋势
    if ma250_trend > 0 and ma60_trend > 0:
        trend = "强势上涨"
    elif ma250_trend < 0 and ma60_trend < 0:
        trend = "强势下跌"
    elif ma250_trend > 0 and ma60_trend < 0:
        trend = "上涨趋势转弱"
    elif ma250_trend < 0 and ma60_trend > 0:
        trend = "下跌趋势企稳"
    else:
        trend = "长期震荡"
    
    return {
        'trend': trend,
        'ma250_slope': ma250_trend,
        'ma60_slope': ma60_trend,
        'period': '250天'
    }

def _analyze_medium_term_trend(data: pd.DataFrame, ma_columns: list) -> Dict[str, Any]:
    """
    分析均线中期趋势（60天）
    """
    # 计算中期均线的趋势
    ma60_trend = _calculate_trend_direction(data['ma_qfq_60'])
    ma20_trend = _calculate_trend_direction(data['ma_qfq_20'])
    
    # 计算趋势的斜率
    slope = _calculate_trend_slope(data['ma_qfq_20'])
    
    # 判断趋势强度
    if abs(slope) < 0.1:
        trend = "横盘震荡"
    elif slope > 0:
        trend = "强势上涨" if ma60_trend > 0 and ma20_trend > 0 else "弱势上涨"
    else:
        trend = "强势下跌" if ma60_trend < 0 and ma20_trend < 0 else "弱势下跌"
    
    return {
        'trend': trend,
        'ma60_slope': ma60_trend,
        'ma20_slope': ma20_trend,
        'slope': slope,
        'period': '60天'
    }

def _analyze_short_term_signal(data: pd.DataFrame, ma_columns: list) -> Dict[str, Any]:
    """
    分析均线短期信号（20天）
    """
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    # 1. 分析均线交叉信号
    cross_signals = _analyze_ma_crossover(data)
    
    # 2. 分析均线拐点
    turning_signals = _analyze_ma_turning_points(data)
    
    # 3. 分析均线密集区突破
    breakthrough = _analyze_ma_breakthrough(data)
    
    # 4. 分析短期趋势强度
    trend_strength = _analyze_short_term_trend_strength(data)
    
    # 5. 分析均线乖离率
    deviation = _analyze_ma_deviation(data)
    
    # 生成综合短期信号
    summary = _generate_short_term_summary(
        cross_signals, 
        turning_signals,
        breakthrough,
        trend_strength,
        deviation
    )
    
    return {
        'summary': summary,
        'cross_signals': cross_signals,
        'turning_signals': turning_signals,
        'breakthrough': breakthrough,
        'trend_strength': trend_strength,
        'deviation': deviation,
        'period': '20天'
    }

def _analyze_ma_crossover(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """分析均线交叉信号"""
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    signals = []
    
    # 检查短期均线和中期均线的交叉
    ma_pairs = [
        ('ma_qfq_5', 'ma_qfq_10'),
        ('ma_qfq_5', 'ma_qfq_20'),
        ('ma_qfq_10', 'ma_qfq_20'),
        ('ma_qfq_20', 'ma_qfq_30')
    ]
    
    for short_ma, long_ma in ma_pairs:
        today_diff = latest[short_ma] - latest[long_ma]
        yesterday_diff = prev[short_ma] - prev[long_ma]
        
        if today_diff > 0 and yesterday_diff < 0:
            strength = "强势" if abs(today_diff) > abs(yesterday_diff) * 1.5 else "普通"
            signals.append({
                'type': 'golden_cross',
                'short_ma': short_ma,
                'long_ma': long_ma,
                'strength': strength,
                'value': latest[short_ma],
                'diff': today_diff
            })
        elif today_diff < 0 and yesterday_diff > 0:
            strength = "强势" if abs(today_diff) > abs(yesterday_diff) * 1.5 else "普通"
            signals.append({
                'type': 'death_cross',
                'short_ma': short_ma,
                'long_ma': long_ma,
                'strength': strength,
                'value': latest[short_ma],
                'diff': today_diff
            })
    
    return signals

def _analyze_ma_turning_points(data: pd.DataFrame) -> Dict[str, List[Dict[str, Any]]]:
    """分析均线拐点信号"""
    # 使用最近5天的数据分析拐点
    recent_data = data.tail(5)
    turning_points = {}
    
    for ma in ['ma_qfq_5', 'ma_qfq_10', 'ma_qfq_20']:
        ma_values = recent_data[ma].values
        # 计算一阶导数（斜率）
        slopes = np.diff(ma_values)
        # 计算二阶导数（斜率变化）
        slope_changes = np.diff(slopes)
        
        # 判断拐点类型
        if len(slope_changes) >= 2:
            if slope_changes[-1] > 0 and slopes[-1] > 0:
                turn_type = "加速上涨"
            elif slope_changes[-1] > 0 and slopes[-1] < 0:
                turn_type = "下跌趋缓"
            elif slope_changes[-1] < 0 and slopes[-1] > 0:
                turn_type = "上涨趋缓"
            elif slope_changes[-1] < 0 and slopes[-1] < 0:
                turn_type = "加速下跌"
            else:
                turn_type = "无明显拐点"
                
            turning_points[ma] = {
                'type': turn_type,
                'slope': slopes[-1],
                'slope_change': slope_changes[-1],
                'value': ma_values[-1]
            }
    
    return turning_points

def _analyze_ma_breakthrough(data: pd.DataFrame) -> Dict[str, Any]:
    """分析均线密集区突破"""
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    # 计算均线密集区
    ma_values = [latest[ma] for ma in ['ma_qfq_5', 'ma_qfq_10', 'ma_qfq_20']]
    ma_std = np.std(ma_values)
    ma_mean = np.mean(ma_values)
    
    # 判断是否形成密集区
    is_convergence = ma_std / ma_mean < 0.01
    
    result = {
        'is_convergence': is_convergence,
        'ma_std': ma_std,
        'ma_mean': ma_mean,
        'type': 'no_breakthrough'
    }
    
    # 分析突破
    if is_convergence:
        price_change = latest['close'] - prev['close']
        volume_change = latest['vol'] / prev['vol']
        
        if price_change > 0 and volume_change > 1.5:
            result.update({
                'type': 'upward_breakthrough',
                'strength': 'strong' if volume_change > 2 else 'normal',
                'price_change_pct': price_change / prev['close'] * 100,
                'volume_change': volume_change
            })
        elif price_change < 0 and volume_change > 1.5:
            result.update({
                'type': 'downward_breakthrough',
                'strength': 'strong' if volume_change > 2 else 'normal',
                'price_change_pct': price_change / prev['close'] * 100,
                'volume_change': volume_change
            })
    
    return result

def _analyze_short_term_trend_strength(data: pd.DataFrame) -> Dict[str, Any]:
    """分析短期趋势强度"""
    recent_data = data.tail(5)
    
    # 计算短期均线的趋势强度
    ma5_trend = _calculate_trend_slope(recent_data['ma_qfq_5'])
    ma10_trend = _calculate_trend_slope(recent_data['ma_qfq_10'])
    
    # 计算价格动量
    momentum = (recent_data['close'].iloc[-1] / recent_data['close'].iloc[0] - 1) * 100
    
    # 计算成交量变化
    volume_change = recent_data['vol'].iloc[-1] / recent_data['vol'].mean()
    
    strength = 'strong' if abs(momentum) > 3 and volume_change > 1.2 else 'normal'
    
    return {
        'ma5_trend': ma5_trend,
        'ma10_trend': ma10_trend,
        'momentum': momentum,
        'volume_ratio': volume_change,
        'strength': strength,
        'period': '5天'
    }

def _analyze_ma_deviation(data: pd.DataFrame) -> Dict[str, Any]:
    """分析均线乖离率"""
    latest = data.iloc[-1]
    
    # 计算各均线对当前价格的乖离率
    deviations = {}
    for ma in ['ma_qfq_5', 'ma_qfq_10', 'ma_qfq_20']:
        deviation = (latest['close'] - latest[ma]) / latest[ma] * 100
        deviations[ma] = deviation
    
    # 判断乖离状态
    avg_deviation = np.mean(list(deviations.values()))
    max_deviation = max(abs(d) for d in deviations.values())
    
    if max_deviation > 5:
        status = "超买" if avg_deviation > 0 else "超卖"
    else:
        status = "正常"
    
    return {
        'deviations': deviations,
        'average_deviation': avg_deviation,
        'max_deviation': max_deviation,
        'status': status,
        'current_price': latest['close']
    }

def _analyze_formation(data: pd.DataFrame, ma_columns: list) -> Dict[str, Any]:
    """
    分析均线形态
    """
    latest = data.iloc[-1]
    
    # 检查多头排列
    is_bullish = all(latest[ma_columns[i]] > latest[ma_columns[i+1]] 
                    for i in range(len(ma_columns)-1))
    
    # 检查空头排列
    is_bearish = all(latest[ma_columns[i]] < latest[ma_columns[i+1]] 
                    for i in range(len(ma_columns)-1))
    
    # 计算均线密集程度
    ma_values = [latest[col] for col in ma_columns]
    dispersion = np.std(ma_values) / np.mean(ma_values)
    
    formation_type = "多头排列" if is_bullish else "空头排列" if is_bearish else "混乱排列"
    strength = "强" if dispersion > 0.05 else "中" if dispersion > 0.02 else "弱"
    
    return {
        'type': formation_type,
        'strength': strength,
        'dispersion': dispersion,
        'is_bullish': is_bullish,
        'is_bearish': is_bearish
    }

def _analyze_strength(data: pd.DataFrame, ma_columns: list) -> Dict[str, Any]:
    """
    分析均线系统强度
    """
    latest = data.iloc[-1]
    
    # 计算短期均线和长期均线的距离
    ma_distances = []
    for i in range(len(ma_columns)-1):
        distance = abs(latest[ma_columns[i]] - latest[ma_columns[i+1]]) / latest[ma_columns[i+1]]
        ma_distances.append(distance)
    
    avg_distance = np.mean(ma_distances)
    
    if avg_distance > 0.05:
        strength = "极强势"
    elif avg_distance > 0.03:
        strength = "强势"
    elif avg_distance > 0.01:
        strength = "中等强度"
    else:
        strength = "弱势"
    
    return {
        'strength': strength,
        'average_distance': avg_distance,
        'distances': dict(zip(ma_columns[:-1], ma_distances))
    }

def _analyze_support_resistance(data: pd.DataFrame, ma_columns: list) -> Dict[str, Any]:
    """
    分析均线支撑阻力位
    """
    latest = data.iloc[-1]
    latest_price = latest['close']
    
    support_levels = []
    resistance_levels = []
    
    for ma in ma_columns:
        ma_value = latest[ma]
        if ma_value < latest_price:
            support_levels.append({'ma': ma, 'value': ma_value})
        else:
            resistance_levels.append({'ma': ma, 'value': ma_value})
    
    support_levels = sorted(support_levels, key=lambda x: x['value'], reverse=True)
    resistance_levels = sorted(resistance_levels, key=lambda x: x['value'])
    
    return {
        'support_levels': support_levels,
        'resistance_levels': resistance_levels,
        'nearest_support': support_levels[0] if support_levels else None,
        'nearest_resistance': resistance_levels[0] if resistance_levels else None,
        'current_price': latest_price
    }

def _generate_composite_signal(analysis: Dict[str, Any]) -> str:
    """
    生成均线系统综合信号
    """
    # 获取各维度分析结果
    long_term = analysis['long_term_trend']
    medium_term = analysis['medium_term_trend']
    short_term = analysis['short_term_signal']
    formation = analysis['formation']
    strength = analysis['strength']
    
    # 生成综合信号
    signal_parts = []
    
    # 添加形态信号
    signal_parts.append(f"均线{formation['type']}（{formation['strength']}）")
    
    # 添加趋势信号
    if "上涨" in medium_term['trend']:
        if "上涨" in long_term['trend']:
            signal_parts.append("多头趋势确立")
        else:
            signal_parts.append("多头趋势形成中")
    elif "下跌" in medium_term['trend']:
        if "下跌" in long_term['trend']:
            signal_parts.append("空头趋势确立")
        else:
            signal_parts.append("空头趋势形成中")
    else:
        signal_parts.append("趋势不明确")
    
    # 添加短期信号
    if short_term['summary'] != "无明显短期信号":
        signal_parts.append(f"出现{short_term['summary']}")
    
    # 添加强度描述
    signal_parts.append(f"（{strength['strength']}）")
    
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

def _generate_short_term_summary(cross_signals: List[Dict[str, Any]],
                               turning_signals: Dict[str, Dict[str, Any]],
                               breakthrough: Dict[str, Any],
                               trend_strength: Dict[str, Any],
                               deviation: Dict[str, Any]) -> str:
    """
    生成短期信号综合总结
    """
    summary_parts = []
    
    # 1. 添加交叉信号
    if cross_signals:
        for signal in cross_signals:
            short_ma = signal['short_ma'].replace('ma_qfq_', '')
            long_ma = signal['long_ma'].replace('ma_qfq_', '')
            signal_type = "金叉" if signal['type'] == 'golden_cross' else "死叉"
            summary_parts.append(f"{short_ma}日线与{long_ma}日线形成{signal['strength']}{signal_type}")
    
    # 2. 添加拐点信号
    for ma, turn_info in turning_signals.items():
        ma_days = ma.replace('ma_qfq_', '')
        summary_parts.append(f"{ma_days}日均线{turn_info['type']}")
    
    # 3. 添加突破信号
    if breakthrough['type'] != 'no_breakthrough':
        direction = "向上" if breakthrough['type'] == 'upward_breakthrough' else "向下"
        strength = "强势" if breakthrough.get('strength') == 'strong' else "普通"
        summary_parts.append(f"均线密集区{direction}突破（{strength}）")
    
    # 4. 添加趋势强度
    if trend_strength['strength'] == 'strong':
        momentum_dir = "上涨" if trend_strength['momentum'] > 0 else "下跌"
        summary_parts.append(f"短期{momentum_dir}动能强劲")
    
    # 5. 添加乖离状态
    if deviation['status'] != "正常":
        summary_parts.append(f"均线系统{deviation['status']}（{abs(deviation['average_deviation']):.2f}%）")
    
    return "，".join(summary_parts) if summary_parts else "无明显短期信号" 