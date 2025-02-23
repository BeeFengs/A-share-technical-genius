"""
K线形态分析模块
用于分析短期（5天）K线组合形态，结合成交量等指标提供交易信号
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np


def analyze_candlesticks(df: pd.DataFrame, 
                        long_term: pd.DataFrame,
                        medium_term: pd.DataFrame, 
                        short_term: pd.DataFrame) -> Dict[str, Any]:
    """
    综合分析K线形态
    
    参数:
        df: 完整的历史数据
        long_term: 40天数据
        medium_term: 20天数据
        short_term: 10天数据
        
    返回:
        Dict包含分析结果
    """
    # 主要使用最近的数据进行分析
    return analyze_candlestick_patterns(short_term)




def analyze_candlestick_patterns(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析K线形态，返回形态列表、星级评分和交易建议
    
    参数:
        df: 包含OHLCV数据的DataFrame，按时间升序排列
        
    返回:
        包含分析结果的字典，包括形态列表、星级评分和交易建议
    """
    if len(df) < 5:
        return {
            "error": "数据不足，需要至少5天的数据",
            "status": "error"
        }
    
    # 获取最近5天的数据
    recent_data = df.tail(5)
    latest_day = recent_data.iloc[-1]
    
    # 初始化结果字典
    result = {
        "patterns": [],     # 所有识别到的形态
        "strength": "",     # 星级评分
        "suggestion": ""    # 交易建议
    }
    
    # 用于计算强度的计数器
    pattern_weights = {
        "今日形态": 1,
        "两日形态": 2,
        "三日形态": 3,
        "四日形态": 4,
        "五日形态": 5
    }
    total_weight = 0
    
    # 用于判断趋势的计数器
    bullish_count = 0
    bearish_count = 0
    
    # 分析单日形态（今日）
    latest_open = latest_day['open']
    latest_close = latest_day['close']
    latest_high = latest_day['high']
    latest_low = latest_day['low']
    
    # 检查单日形态
    if is_doji(latest_open, latest_close, latest_high, latest_low):
        result["patterns"].append({"type": "今日形态", "pattern": "十字星"})
        total_weight += pattern_weights["今日形态"]
    
    if is_long_legged_doji(latest_open, latest_close, latest_high, latest_low):
        result["patterns"].append({"type": "今日形态", "pattern": "长腿十字星"})
        total_weight += pattern_weights["今日形态"]
    
    if is_gravestone_doji(latest_open, latest_close, latest_high, latest_low):
        result["patterns"].append({"type": "今日形态", "pattern": "墓碑十字星"})
        total_weight += pattern_weights["今日形态"]
        bearish_count += 1
    
    if is_spinning_top(latest_open, latest_close, latest_high, latest_low):
        result["patterns"].append({"type": "今日形态", "pattern": "纺锤线"})
        total_weight += pattern_weights["今日形态"]
    
    if is_hammer(latest_open, latest_close, latest_high, latest_low):
        result["patterns"].append({"type": "今日形态", "pattern": "锤子线"})
        total_weight += pattern_weights["今日形态"]
        bullish_count += 1
    
    if is_inverted_hammer(latest_open, latest_close, latest_high, latest_low):
        result["patterns"].append({"type": "今日形态", "pattern": "倒锤子线"})
        total_weight += pattern_weights["今日形态"]
        bullish_count += 1
    
    if is_hanging_man(latest_open, latest_close, latest_high, latest_low):
        result["patterns"].append({"type": "今日形态", "pattern": "吊颈线"})
        total_weight += pattern_weights["今日形态"]
        bearish_count += 1
    
    if is_shooting_star(latest_open, latest_close, latest_high, latest_low):
        result["patterns"].append({"type": "今日形态", "pattern": "流星线"})
        total_weight += pattern_weights["今日形态"]
        bearish_count += 1
    
    # 分析两日形态
    if len(recent_data) >= 2:
        prev_day = recent_data.iloc[-2]
        
        # 创建一个列表来存储所有可能的两日形态及其优先级
        two_day_patterns = []
        
        # 检查所有可能的两日形态并设置优先级
        if is_bullish_engulfing(prev_day, latest_day):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "看涨吞没形态",
                "priority": 5,
                "is_bullish": True
            })
        
        if is_bearish_engulfing(prev_day, latest_day):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "看跌吞没形态",
                "priority": 5,
                "is_bullish": False
            })
        
        if is_harami(prev_day, latest_day, True):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "看涨孕线形态",
                "priority": 4,
                "is_bullish": True
            })
        
        if is_harami(prev_day, latest_day, False):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "看跌孕线形态",
                "priority": 4,
                "is_bullish": False
            })
        
        if is_piercing_line(prev_day, latest_day):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "刺透形态",
                "priority": 4,
                "is_bullish": True
            })
        
        if is_dark_cloud_cover(prev_day, latest_day):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "乌云盖顶形态",
                "priority": 4,
                "is_bullish": False
            })
        
        if is_tweezer(prev_day, latest_day, True):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "镊子底形态",
                "priority": 3,
                "is_bullish": True
            })
        
        if is_tweezer(prev_day, latest_day, False):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "镊子顶形态",
                "priority": 3,
                "is_bullish": False
            })
        
        if is_gap(prev_day, latest_day, True):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "向上跳空缺口",
                "priority": 3,
                "is_bullish": True
            })
        
        if is_gap(prev_day, latest_day, False):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "向下跳空缺口",
                "priority": 3,
                "is_bullish": False
            })
        
        if is_flat_top_bottom(prev_day, latest_day, True):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "平头顶形态",
                "priority": 2,
                "is_bullish": False
            })
        
        if is_flat_top_bottom(prev_day, latest_day, False):
            two_day_patterns.append({
                "type": "两日形态",
                "pattern": "平头底形态",
                "priority": 2,
                "is_bullish": True
            })
        
        # 如果存在两日形态，选择优先级最高的一个
        if two_day_patterns:
            # 按优先级排序
            two_day_patterns.sort(key=lambda x: x["priority"], reverse=True)
            selected_pattern = two_day_patterns[0]
            
            # 添加选中的形态
            result["patterns"].append({
                "type": selected_pattern["type"],
                "pattern": selected_pattern["pattern"]
            })
            total_weight += pattern_weights["两日形态"]
            if selected_pattern["is_bullish"]:
                bullish_count += 2
            else:
                bearish_count += 2
    
    # 分析三日形态
    if len(recent_data) >= 3:
        three_days = recent_data.iloc[-3:]
        three_day_patterns = []
        
        # 检查所有可能的三日形态并设置优先级
        if is_morning_star(three_days):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "启明星形态",
                "priority": 5,
                "is_bullish": True
            })
        
        if is_evening_star(three_days):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "黄昏星形态",
                "priority": 5,
                "is_bullish": False
            })
        
        if is_three_white_soldiers(three_days):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "三白兵形态",
                "priority": 4,
                "is_bullish": True
            })
        
        if is_three_black_crows(three_days):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "三黑鸦形态",
                "priority": 4,
                "is_bullish": False
            })
        
        bullish_three_inside, bearish_three_inside = is_three_inside(three_days)
        if bullish_three_inside:
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "看涨三内形态",
                "priority": 3,
                "is_bullish": True
            })
        if bearish_three_inside:
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "看跌三内形态",
                "priority": 3,
                "is_bullish": False
            })
        
        bullish_three_outside, bearish_three_outside = is_three_outside(three_days)
        if bullish_three_outside:
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "看涨三外形态",
                "priority": 3,
                "is_bullish": True
            })
        if bearish_three_outside:
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "看跌三外形态",
                "priority": 3,
                "is_bullish": False
            })
        
        if is_three_mountains(three_days):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "三山形态",
                "priority": 4,
                "is_bullish": False
            })
        
        if is_three_rivers(three_days):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "三川形态",
                "priority": 4,
                "is_bullish": True
            })
        
        if is_three_stars(three_days):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "三星形态",
                "priority": 3,
                "is_bullish": True
            })
        
        if is_island_reversal(three_days, True):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "看涨岛型反转",
                "priority": 5,
                "is_bullish": True
            })
        
        if is_island_reversal(three_days, False):
            three_day_patterns.append({
                "type": "三日形态",
                "pattern": "看跌岛型反转",
                "priority": 5,
                "is_bullish": False
            })
        
        # 如果存在三日形态，选择优先级最高的一个
        if three_day_patterns:
            # 按优先级排序
            three_day_patterns.sort(key=lambda x: x["priority"], reverse=True)
            selected_pattern = three_day_patterns[0]
            
            # 添加选中的形态
            result["patterns"].append({
                "type": selected_pattern["type"],
                "pattern": selected_pattern["pattern"]
            })
            total_weight += pattern_weights["三日形态"]
            if selected_pattern["is_bullish"]:
                bullish_count += 3
            else:
                bearish_count += 3
    
    # 分析四日形态
    if len(recent_data) >= 4:
        four_days = recent_data.iloc[-4:]
        four_day_patterns = []
        
        bullish_three_line_strike, bearish_three_line_strike = is_three_line_strike(four_days)
        if bullish_three_line_strike:
            four_day_patterns.append({
                "type": "四日形态",
                "pattern": "看涨三线打击形态",
                "priority": 4,
                "is_bullish": True
            })
        if bearish_three_line_strike:
            four_day_patterns.append({
                "type": "四日形态",
                "pattern": "看跌三线打击形态",
                "priority": 4,
                "is_bullish": False
            })
        
        # 如果存在四日形态，选择优先级最高的一个
        if four_day_patterns:
            # 按优先级排序
            four_day_patterns.sort(key=lambda x: x["priority"], reverse=True)
            selected_pattern = four_day_patterns[0]
            
            # 添加选中的形态
            result["patterns"].append({
                "type": selected_pattern["type"],
                "pattern": selected_pattern["pattern"]
            })
            total_weight += pattern_weights["四日形态"]
            if selected_pattern["is_bullish"]:
                bullish_count += 4
            else:
                bearish_count += 4
    
    # 分析五日形态
    if len(recent_data) >= 5:
        five_day_patterns = []
        
        if is_rising_three_methods(recent_data):
            five_day_patterns.append({
                "type": "五日形态",
                "pattern": "上升三法形态",
                "priority": 5,
                "is_bullish": True
            })
        
        if is_falling_three_methods(recent_data):
            five_day_patterns.append({
                "type": "五日形态",
                "pattern": "下降三法形态",
                "priority": 5,
                "is_bullish": False
            })
        
        # 如果存在五日形态，选择优先级最高的一个
        if five_day_patterns:
            # 按优先级排序
            five_day_patterns.sort(key=lambda x: x["priority"], reverse=True)
            selected_pattern = five_day_patterns[0]
            
            # 添加选中的形态
            result["patterns"].append({
                "type": selected_pattern["type"],
                "pattern": selected_pattern["pattern"]
            })
            total_weight += pattern_weights["五日形态"]
            if selected_pattern["is_bullish"]:
                bullish_count += 5
            else:
                bearish_count += 5
    
    # 计算星级
    if len(result["patterns"]) > 0:
        # 根据形态数量和权重计算强度
        strength = min(5, total_weight / len(result["patterns"]))
        result["strength"] = convert_to_stars(strength)
        
        # 生成交易建议
        if bullish_count > bearish_count:
            if strength >= 4:
                result["suggestion"] = "强烈看涨信号"
            else:
                result["suggestion"] = "看涨信号"
        elif bearish_count > bullish_count:
            if strength >= 4:
                result["suggestion"] = "强烈看跌信号"
            else:
                result["suggestion"] = "看跌信号"
        else:
            result["suggestion"] = "市场震荡"
    else:
        result["strength"] = "☆☆☆☆☆"
        result["suggestion"] = "无明显信号"
    
    return result



def is_doji(open_price: float, close_price: float, high: float, low: float) -> bool:
    """
    判断是否为十字星形态
    """
    body = abs(open_price - close_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    return body <= total_range * 0.1 and upper_shadow > body and lower_shadow > body

def is_hammer(open_price: float, close_price: float, high: float, low: float) -> bool:
    """
    判断是否为锤子线形态
    """
    body = abs(open_price - close_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    return (lower_shadow >= body * 2 and 
            upper_shadow <= body * 0.1 and 
            body >= total_range * 0.1)

def is_shooting_star(open_price: float, close_price: float, high: float, low: float) -> bool:
    """
    判断是否为流星线形态
    """
    body = abs(open_price - close_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    return (upper_shadow >= body * 2 and 
            lower_shadow <= body * 0.1 and 
            body >= total_range * 0.1)

def is_bullish_engulfing(day1: pd.Series, day2: pd.Series) -> bool:
    """
    判断是否为看涨吞没形态
    """
    return (day1['close'] < day1['open'] and  # 第一天阴线
            day2['close'] > day2['open'] and  # 第二天阳线
            day2['open'] < day1['close'] and  # 第二天开盘价低于第一天收盘价
            day2['close'] > day1['open'])     # 第二天收盘价高于第一天开盘价

def is_bearish_engulfing(day1: pd.Series, day2: pd.Series) -> bool:
    """
    判断是否为看跌吞没形态
    """
    return (day1['close'] > day1['open'] and  # 第一天阳线
            day2['close'] < day2['open'] and  # 第二天阴线
            day2['open'] > day1['close'] and  # 第二天开盘价高于第一天收盘价
            day2['close'] < day1['open'])     # 第二天收盘价低于第一天开盘价

def is_morning_star(days: pd.DataFrame) -> bool:
    """
    判断是否为启明星形态
    """
    if len(days) < 3:
        return False
        
    day1, day2, day3 = days.iloc[0], days.iloc[1], days.iloc[2]
    
    return (day1['close'] < day1['open'] and                     # 第一天阴线
            abs(day2['close'] - day2['open']) < (day2['high'] - day2['low']) * 0.3 and  # 第二天十字星
            day3['close'] > day3['open'] and                     # 第三天阳线
            day2['high'] < day1['close'] and                     # 第二天价格跳空低开
            day3['close'] > (day1['open'] + day1['close']) / 2)  # 第三天收盘价回升超过第一天实体一半

def is_evening_star(days: pd.DataFrame) -> bool:
    """
    判断是否为黄昏星形态
    """
    if len(days) < 3:
        return False
        
    day1, day2, day3 = days.iloc[0], days.iloc[1], days.iloc[2]
    
    return (day1['close'] > day1['open'] and                     # 第一天阳线
            abs(day2['close'] - day2['open']) < (day2['high'] - day2['low']) * 0.3 and  # 第二天十字星
            day3['close'] < day3['open'] and                     # 第三天阴线
            day2['low'] > day1['close'] and                      # 第二天价格跳空高开
            day3['close'] < (day1['open'] + day1['close']) / 2)  # 第三天收盘价下跌超过第一天实体一半

def is_three_white_soldiers(days: pd.DataFrame) -> bool:
    """
    判断是否为三白兵形态
    """
    if len(days) < 3:
        return False
    
    # 检查三天都是阳线，且每天收盘价都比前一天高
    return all(days.iloc[i]['close'] > days.iloc[i]['open'] and  # 当天是阳线
               (i == 0 or days.iloc[i]['close'] > days.iloc[i-1]['close']) and  # 收盘价上升
               (i == 0 or days.iloc[i]['open'] > days.iloc[i-1]['open'])  # 开盘价上升
               for i in range(3))

def is_three_black_crows(days: pd.DataFrame) -> bool:
    """
    判断是否为三黑鸦形态
    """
    if len(days) < 3:
        return False
    
    # 检查三天都是阴线，且每天收盘价都比前一天低
    return all(days.iloc[i]['close'] < days.iloc[i]['open'] and  # 当天是阴线
               (i == 0 or days.iloc[i]['close'] < days.iloc[i-1]['close']) and  # 收盘价下降
               (i == 0 or days.iloc[i]['open'] < days.iloc[i-1]['open'])  # 开盘价下降
               for i in range(3))

def is_rising_three_methods(days: pd.DataFrame) -> bool:
    """
    判断是否为上升三法形态
    """
    if len(days) < 5:
        return False
    
    day1, day5 = days.iloc[0], days.iloc[4]
    middle_days = days.iloc[1:4]
    
    return (day1['close'] > day1['open'] and  # 第一天大阳线
            day5['close'] > day5['open'] and  # 最后一天大阳线
            day5['close'] > day1['close'] and  # 突破新高
            all(middle_days.iloc[i]['close'] < middle_days.iloc[i]['open']  # 中间三天是小阴线
                for i in range(len(middle_days))) and
            all(middle_days.iloc[i]['low'] > day1['open']  # 中间三天的最低价高于第一天开盘价
                for i in range(len(middle_days))))

def is_falling_three_methods(days: pd.DataFrame) -> bool:
    """
    判断是否为下降三法形态
    """
    if len(days) < 5:
        return False
    
    day1, day5 = days.iloc[0], days.iloc[4]
    middle_days = days.iloc[1:4]
    
    return (day1['close'] < day1['open'] and  # 第一天大阴线
            day5['close'] < day5['open'] and  # 最后一天大阴线
            day5['close'] < day1['close'] and  # 突破新低
            all(middle_days.iloc[i]['close'] > middle_days.iloc[i]['open']  # 中间三天是小阳线
                for i in range(len(middle_days))) and
            all(middle_days.iloc[i]['high'] < day1['open']  # 中间三天的最高价低于第一天开盘价
                for i in range(len(middle_days))))

def check_volume_confirmation(volume: float, avg_volume: float) -> float:
    """
    检查成交量确认强度
    返回0-1之间的确认强度得分
    """
    volume_ratio = volume / avg_volume
    if volume_ratio >= 2:
        return 1.0
    elif volume_ratio >= 1.5:
        return 0.8
    elif volume_ratio >= 1:
        return 0.6
    else:
        return 0.3

def is_harami(day1: pd.Series, day2: pd.Series, bullish: bool = True) -> bool:
    """
    判断是否为孕线形态（看涨/看跌）
    
    参数:
        day1: 第一天数据
        day2: 第二天数据
        bullish: True为看涨孕线，False为看跌孕线
    """
    if bullish:
        return (day1['close'] < day1['open'] and  # 第一天阴线
                day2['close'] > day2['open'] and  # 第二天阳线
                day2['open'] > day1['close'] and  # 第二天实体在第一天实体内
                day2['close'] < day1['open'] and
                abs(day2['close'] - day2['open']) < abs(day1['close'] - day1['open']) * 0.5)  # 第二天实体小于第一天的一半
    else:
        return (day1['close'] > day1['open'] and  # 第一天阳线
                day2['close'] < day2['open'] and  # 第二天阴线
                day2['open'] < day1['close'] and  # 第二天实体在第一天实体内
                day2['close'] > day1['open'] and
                abs(day2['close'] - day2['open']) < abs(day1['close'] - day1['open']) * 0.5)  # 第二天实体小于第一天的一半

def is_tweezer(day1: pd.Series, day2: pd.Series, bullish: bool = True) -> bool:
    """
    判断是否为镊子底/顶形态
    """
    price_diff_threshold = (day1['high'] - day1['low']) * 0.001  # 允许0.1%的误差
    
    if bullish:  # 镊子底
        return (day1['close'] < day1['open'] and  # 第一天阴线
                day2['close'] > day2['open'] and  # 第二天阳线
                abs(day1['low'] - day2['low']) <= price_diff_threshold)  # 两天低点相同
    else:  # 镊子顶
        return (day1['close'] > day1['open'] and  # 第一天阳线
                day2['close'] < day2['open'] and  # 第二天阴线
                abs(day1['high'] - day2['high']) <= price_diff_threshold)  # 两天高点相同

def is_piercing_line(day1: pd.Series, day2: pd.Series) -> bool:
    """
    判断是否为刺透形态
    """
    mid_point = (day1['open'] + day1['close']) / 2
    return (day1['close'] < day1['open'] and  # 第一天阴线
            day2['close'] > day2['open'] and  # 第二天阳线
            day2['open'] < day1['close'] and  # 第二天开盘价低于第一天收盘价
            day2['close'] > mid_point)  # 第二天收盘价高于第一天实体中点

def is_dark_cloud_cover(day1: pd.Series, day2: pd.Series) -> bool:
    """
    判断是否为乌云盖顶形态
    """
    mid_point = (day1['open'] + day1['close']) / 2
    return (day1['close'] > day1['open'] and  # 第一天阳线
            day2['close'] < day2['open'] and  # 第二天阴线
            day2['open'] > day1['close'] and  # 第二天开盘价高于第一天收盘价
            day2['close'] < mid_point)  # 第二天收盘价低于第一天实体中点

def is_inside_bar(day1: pd.Series, day2: pd.Series) -> bool:
    """
    判断是否为内包形态
    """
    return (day2['high'] < day1['high'] and  # 第二天最高价低于第一天最高价
            day2['low'] > day1['low'])  # 第二天最低价高于第一天最低价

def is_outside_bar(day1: pd.Series, day2: pd.Series) -> bool:
    """
    判断是否为外包形态
    """
    return (day2['high'] > day1['high'] and  # 第二天最高价高于第一天最高价
            day2['low'] < day1['low'])  # 第二天最低价低于第一天最低价

def is_three_inside(days: pd.DataFrame) -> Tuple[bool, bool]:
    """
    判断是否为三内形态（看涨/看跌）
    返回: (是否看涨三内, 是否看跌三内)
    """
    if len(days) < 3:
        return False, False
        
    day1, day2, day3 = days.iloc[0], days.iloc[1], days.iloc[2]
    
    bullish = (is_inside_bar(day1, day2) and  # 前两天形成内包
               day1['close'] < day1['open'] and  # 第一天阴线
               day3['close'] > day3['open'] and  # 第三天阳线
               day3['close'] > day2['high'])     # 第三天突破上方
               
    bearish = (is_inside_bar(day1, day2) and  # 前两天形成内包
               day1['close'] > day1['open'] and  # 第一天阳线
               day3['close'] < day3['open'] and  # 第三天阴线
               day3['close'] < day2['low'])      # 第三天突破下方
               
    return bullish, bearish

def is_three_outside(days: pd.DataFrame) -> Tuple[bool, bool]:
    """
    判断是否为三外形态（看涨/看跌）
    返回: (是否看涨三外, 是否看跌三外)
    """
    if len(days) < 3:
        return False, False
        
    day1, day2, day3 = days.iloc[0], days.iloc[1], days.iloc[2]
    
    bullish = (is_outside_bar(day1, day2) and  # 前两天形成外包
               day1['close'] < day1['open'] and  # 第一天阴线
               day2['close'] > day2['open'] and  # 第二天阳线
               day3['close'] > day3['open'] and  # 第三天阳线
               day3['close'] > day2['high'])     # 第三天创新高
               
    bearish = (is_outside_bar(day1, day2) and  # 前两天形成外包
               day1['close'] > day1['open'] and  # 第一天阳线
               day2['close'] < day2['open'] and  # 第二天阴线
               day3['close'] < day3['open'] and  # 第三天阴线
               day3['close'] < day2['low'])      # 第三天创新低
               
    return bullish, bearish

def is_three_line_strike(days: pd.DataFrame) -> Tuple[bool, bool]:
    """
    判断是否为三线打击形态（看涨/看跌）
    返回: (是否看涨三线打击, 是否看跌三线打击)
    """
    if len(days) < 4:
        return False, False
    
    # 检查前三天
    bullish = all(days.iloc[i]['close'] < days.iloc[i]['open'] for i in range(3))  # 前三天都是阴线
    bearish = all(days.iloc[i]['close'] > days.iloc[i]['open'] for i in range(3))  # 前三天都是阳线
    
    if bullish:
        # 看涨三线打击
        return (days.iloc[3]['close'] > days.iloc[3]['open'] and  # 第四天是阳线
                days.iloc[3]['close'] > days.iloc[0]['open']), False  # 第四天收盘价高于第一天开盘价
    elif bearish:
        # 看跌三线打击
        return False, (days.iloc[3]['close'] < days.iloc[3]['open'] and  # 第四天是阴线
                      days.iloc[3]['close'] < days.iloc[0]['open'])  # 第四天收盘价低于第一天开盘价
    
    return False, False

def convert_to_stars(strength: float) -> str:
    """
    将强度分数转换为星级显示
    
    参数:
        strength: 0-5之间的强度分数
        
    返回:
        星级字符串，例如: "★★★☆☆"
    """
    # 确保strength在0-5之间
    strength = max(0, min(5, strength))
    
    # 计算实心星和空心星的数量
    full_stars = int(strength)
    empty_stars = 5 - full_stars
    
    # 如果有小数部分且大于0.5，添加半星
    if strength - full_stars >= 0.5:
        return "★" * full_stars + "★" + "☆" * (empty_stars - 1)
    
    return "★" * full_stars + "☆" * empty_stars

def is_long_legged_doji(open_price: float, close_price: float, high: float, low: float) -> bool:
    """
    判断是否为长腿十字星形态
    """
    body = abs(open_price - close_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    return (body <= total_range * 0.1 and 
            upper_shadow >= total_range * 0.3 and 
            lower_shadow >= total_range * 0.3)

def is_gravestone_doji(open_price: float, close_price: float, high: float, low: float) -> bool:
    """
    判断是否为墓碑十字星形态
    """
    body = abs(open_price - close_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    return (body <= total_range * 0.1 and 
            upper_shadow >= total_range * 0.6 and 
            lower_shadow <= total_range * 0.1)

def is_spinning_top(open_price: float, close_price: float, high: float, low: float) -> bool:
    """
    判断是否为纺锤线形态
    """
    body = abs(open_price - close_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    return (body <= total_range * 0.3 and 
            upper_shadow >= body and 
            lower_shadow >= body and
            abs(upper_shadow - lower_shadow) <= total_range * 0.1)

def is_inverted_hammer(open_price: float, close_price: float, high: float, low: float) -> bool:
    """
    判断是否为倒锤子线形态
    """
    body = abs(open_price - close_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    return (upper_shadow >= body * 2 and 
            lower_shadow <= body * 0.1 and 
            body >= total_range * 0.1)

def is_hanging_man(open_price: float, close_price: float, high: float, low: float) -> bool:
    """
    判断是否为吊颈线形态
    """
    body = abs(open_price - close_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    return (lower_shadow >= body * 2 and 
            upper_shadow <= body * 0.1 and 
            body >= total_range * 0.1 and
            close_price < open_price)  # 必须是阴线

def is_gap(day1: pd.Series, day2: pd.Series, bullish: bool = True) -> bool:
    """
    判断是否为跳空缺口形态
    """
    if bullish:
        return day2['low'] > day1['high']  # 向上跳空
    else:
        return day2['high'] < day1['low']  # 向下跳空

def is_flat_top_bottom(day1: pd.Series, day2: pd.Series, is_top: bool = True) -> bool:
    """
    判断是否为平头顶/底形态
    """
    price_diff_threshold = (day1['high'] - day1['low']) * 0.001  # 允许0.1%的误差
    
    if is_top:
        return abs(day1['high'] - day2['high']) <= price_diff_threshold  # 平头顶
    else:
        return abs(day1['low'] - day2['low']) <= price_diff_threshold   # 平头底

def is_three_mountains(days: pd.DataFrame) -> bool:
    """
    判断是否为三山形态（看跌反转）
    """
    if len(days) < 3:
        return False
    
    highs = [days.iloc[i]['high'] for i in range(3)]
    return (highs[1] > highs[0] and 
            highs[1] > highs[2] and 
            abs(highs[0] - highs[2]) <= (days.iloc[0]['high'] - days.iloc[0]['low']) * 0.1)

def is_three_rivers(days: pd.DataFrame) -> bool:
    """
    判断是否为三川形态（看涨反转）
    """
    if len(days) < 3:
        return False
    
    lows = [days.iloc[i]['low'] for i in range(3)]
    return (lows[1] < lows[0] and 
            lows[1] < lows[2] and 
            abs(lows[0] - lows[2]) <= (days.iloc[0]['high'] - days.iloc[0]['low']) * 0.1)

def is_three_stars(days: pd.DataFrame) -> bool:
    """
    判断是否为三星形态
    """
    if len(days) < 3:
        return False
    
    # 检查是否都是十字星
    return all(is_doji(days.iloc[i]['open'], 
                      days.iloc[i]['close'],
                      days.iloc[i]['high'],
                      days.iloc[i]['low']) for i in range(3))

def is_island_reversal(days: pd.DataFrame, bullish: bool = True) -> bool:
    """
    判断是否为岛型反转形态
    """
    if len(days) < 3:
        return False
    
    day1, day2, day3 = days.iloc[0], days.iloc[1], days.iloc[2]
    
    if bullish:
        return (day2['low'] > day1['high'] and  # 第一个跳空（向上）
                day3['high'] < day2['low'])      # 第二个跳空（向下）
    else:
        return (day2['high'] < day1['low'] and  # 第一个跳空（向下）
                day3['low'] > day2['high'])      # 第二个跳空（向上）



