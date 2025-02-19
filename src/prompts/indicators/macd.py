"""
MACD指标分析的prompt模板
"""

def get_macd_analysis_prompt(dif: float, dea: float, macd: float, 
                           long_term_trend: str, medium_term_trend: str,
                           short_term_signal: str, divergence: str,
                           strength: str, signal: str) -> str:
    """
    生成MACD指标分析的prompt模板
    
    参数:
        dif (float): DIF值
        dea (float): DEA值
        macd (float): MACD值
        long_term_trend (str): 长期趋势分析（40天）
        medium_term_trend (str): 中期趋势分析（20天）
        short_term_signal (str): 短期信号（10天）
        divergence (str): 背离分析结果
        strength (str): MACD强度
        signal (str): 综合信号
    
    返回:
        str: 格式化后的prompt
    """
    return f"""
### MACD指标分析

#### 1. 当前MACD指标数据
- DIF：{dif:.2f}
- DEA：{dea:.2f}
- MACD：{macd:.2f}

#### 2. 多周期趋势分析
- 长期趋势（40天）：{long_term_trend}
- 中期趋势（20天）：{medium_term_trend}
- 短期信号（10天）：{short_term_signal}

#### 3. 技术形态分析
- 背离状态：{divergence}
- MACD强度：{strength}
- DIF与DEA位置关系分析：
  * 当前DIF {'>=' if dif >= dea else '<'} DEA
  * MACD柱 {'为正' if macd > 0 else '为负'}，表示{'多头' if macd > 0 else '空头'}势能

#### 4. 综合研判
- 信号：{signal}

请基于以上MACD指标数据进行深入分析：

1. 趋势研判
   - 结合多周期趋势进行分析
   - 评估趋势的持续性和转折可能
   - 分析趋势强弱程度

2. 买卖信号研判
   - 结合短期信号和背离状态
   - 评估当前买卖信号的可靠性
   - 分析可能的假突破或假信号

3. 风险提示
   - 当前趋势的主要风险点
   - 需要重点关注的价位
   - 建议的止损止盈位置

4. 操作建议
   - 短期操作策略
   - 中期布局建议
   - 风险控制要点
""" 