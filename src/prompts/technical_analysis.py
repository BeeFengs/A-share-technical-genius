"""
技术分析报告的prompt模板
"""
from src.prompts.indicators import (
    get_macd_analysis_prompt,
    get_kdj_analysis_prompt,
    get_rsi_analysis_prompt,
    get_boll_analysis_prompt
)

def get_technical_analysis_prompt(stock_name: str, latest_price: float, price_change: float, 
                                vol_change: float, analysis: dict) -> str:
    """
    生成技术分析报告的prompt模板
    
    参数:
        stock_name (str): 股票名称
        latest_price (float): 最新收盘价
        price_change (float): 涨跌幅
        vol_change (float): 成交量变化
        analysis (dict): 技术指标分析结果
        
    返回:
        str: 格式化后的prompt
    """
    # 获取各个指标的分析prompt
    macd_prompt = get_macd_analysis_prompt(
        dif=analysis['MACD']['DIF'],
        dea=analysis['MACD']['DEA'],
        macd=analysis['MACD']['MACD'],
        signal=analysis['MACD']['signal']
    )
    
    kdj_prompt = get_kdj_analysis_prompt(
        k_value=analysis['KDJ']['K'],
        d_value=analysis['KDJ']['D'],
        j_value=analysis['KDJ']['J'],
        signal=analysis['KDJ']['signal']
    )
    
    rsi_prompt = get_rsi_analysis_prompt(
        rsi6=analysis['RSI']['RSI6'],
        rsi12=analysis['RSI']['RSI12'],
        rsi24=analysis['RSI']['RSI24'],
        signal=analysis['RSI']['signal']
    )
    
    boll_prompt = get_boll_analysis_prompt(
        upper=analysis['BOLL']['UPPER'],
        mid=analysis['BOLL']['MID'],
        lower=analysis['BOLL']['LOWER'],
        signal=analysis['BOLL']['signal']
    )
    
    return f"""
作为一名专业的股票技术分析师，请基于以下技术指标数据为{stock_name}生成一份深度技术分析报告。

# 市场数据
## 基础行情
- 最新收盘价：{latest_price:.2f}
- 涨跌幅：{price_change:.2f}%
- 成交量变化：{vol_change:.2f}%

# 技术指标分析
{macd_prompt}

{kdj_prompt}

{rsi_prompt}

{boll_prompt}

# 综合研判

请基于以上所有技术指标的分析结果，进行综合研判：

1. 多空力量对比
   - 结合各指标信号判断多空力量
   - 主力资金动向分析
   - 市场情绪研判

2. 趋势研判
   - 主趋势判断
   - 次级调整特征
   - 趋势持续性分析

3. 综合操作建议
   - 短期操作策略
   - 中期布局建议
   - 风险控制要点

注意事项：
- 分析需要客观、专业、严谨
- 必须有具体数据支撑
- 需要明确指出各个指标的信号含义
- 对于重要结论要给出具体依据
""" 