"""
MACD指标分析的prompt模板
"""

def get_macd_analysis_prompt(dif: float, dea: float, macd: float, signal: str) -> str:
    """
    生成MACD指标分析的prompt模板
    
    参数:
        dif (float): DIF值
        dea (float): DEA值
        macd (float): MACD值
        signal (str): MACD信号
    
    返回:
        str: 格式化后的prompt
    """
    return f"""
### MACD指标分析
当前MACD指标数据：
- DIF：{dif:.2f}
- DEA：{dea:.2f}
- MACD：{macd:.2f}
- 信号：{signal}

请基于以上MACD指标数据进行分析：
1. MACD指标形态特征
   - DIF与DEA的位置关系
   - MACD柱状图形态分析
   - 零轴位置判断

2. 趋势研判
   - 基于MACD判断当前趋势
   - DIF与DEA的交叉信号分析
   - MACD柱状量能变化分析

3. 背离分析
   - 顶背离/底背离判断
   - 背离强度评估
   - 可能的趋势转折点分析

4. 操作建议
   - 基于MACD的交易信号建议
   - 风险控制要点
""" 