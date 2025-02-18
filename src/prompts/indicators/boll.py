"""
布林带指标分析的prompt模板
"""

def get_boll_analysis_prompt(upper: float, mid: float, lower: float, signal: str) -> str:
    """
    生成布林带指标分析的prompt模板
    
    参数:
        upper (float): 上轨值
        mid (float): 中轨值
        lower (float): 下轨值
        signal (str): 布林带信号
    
    返回:
        str: 格式化后的prompt
    """
    return f"""
### 布林带指标分析
当前布林带指标数据：
- 上轨：{upper:.2f}
- 中轨：{mid:.2f}
- 下轨：{lower:.2f}
- 信号：{signal}

请基于以上布林带指标数据进行分析：
1. 布林带形态特征
   - 带宽分析（上下轨距离）
   - 价格在带中的位置
   - 带形态变化趋势

2. 趋势研判
   - 中轨斜率判断趋势
   - 带宽扩张/收缩趋势
   - 价格突破情况分析

3. 波动性分析
   - 基于带宽判断市场波动性
   - 压力支撑位判断
   - 可能的突破方向预判

4. 操作建议
   - 基于布林带的交易信号建议
   - 风险控制要点
""" 