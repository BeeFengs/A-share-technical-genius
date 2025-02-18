"""
RSI指标分析的prompt模板
"""

def get_rsi_analysis_prompt(rsi6: float, rsi12: float, rsi24: float, signal: str) -> str:
    """
    生成RSI指标分析的prompt模板
    
    参数:
        rsi6 (float): RSI6值
        rsi12 (float): RSI12值
        rsi24 (float): RSI24值
        signal (str): RSI信号
    
    返回:
        str: 格式化后的prompt
    """
    return f"""
### RSI指标分析
当前RSI指标数据：
- RSI6：{rsi6:.2f}
- RSI12：{rsi12:.2f}
- RSI24：{rsi24:.2f}
- 信号：{signal}

请基于以上RSI指标数据进行分析：
1. RSI指标形态特征
   - 三条RSI线的位置关系
   - 超买超卖区间判断
   - RSI曲线形态分析

2. 趋势强度研判
   - 基于RSI判断趋势强度
   - 短中长期RSI趋势对比
   - 背离情况分析

3. 市场情绪研判
   - 基于RSI位置判断市场情绪
   - 超买超卖区间持续性分析
   - 可能的趋势转折点判断

4. 操作建议
   - 基于RSI的交易信号建议
   - 风险控制要点
""" 