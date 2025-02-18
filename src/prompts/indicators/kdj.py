"""
KDJ指标分析的prompt模板
"""

def get_kdj_analysis_prompt(k_value: float, d_value: float, j_value: float, signal: str) -> str:
    """
    生成KDJ指标分析的prompt模板
    
    参数:
        k_value (float): K值
        d_value (float): D值
        j_value (float): J值
        signal (str): KDJ信号
    
    返回:
        str: 格式化后的prompt
    """
    return f"""
### KDJ指标分析
当前KDJ指标数据：
- K值：{k_value:.2f}
- D值：{d_value:.2f}
- J值：{j_value:.2f}
- 信号：{signal}

请基于以上KDJ指标数据进行分析：
1. KDJ指标形态特征
   - 当前KDJ指标位置（超买/超卖区间判断）
   - KDJ三线交叉形态分析
   - 指标背离情况研判

2. 市场情绪研判
   - 基于KDJ位置判断市场情绪
   - 结合K、D、J三线位置关系分析走势强弱
   - 超买超卖区间的持续性分析

3. 操作建议
   - 基于KDJ指标的交易信号建议
   - 风险提示和注意事项
""" 