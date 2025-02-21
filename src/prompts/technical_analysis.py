"""
技术分析报告的prompt模板
"""
from src.prompts.indicators import (
    get_macd_analysis_prompt,
    get_kdj_analysis_prompt,
    get_rsi_analysis_prompt,
    get_boll_analysis_prompt,
    get_ma_system_analysis_prompt
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
        long_term_trend=analysis['MACD']['long_term_trend'],
        medium_term_trend=analysis['MACD']['medium_term_trend'],
        short_term_signal=analysis['MACD']['short_term_signal'],
        divergence=analysis['MACD']['divergence'],
        strength=analysis['MACD']['strength'],
        signal=analysis['MACD']['signal']
    )
    
    kdj_prompt = get_kdj_analysis_prompt(
        k_value=analysis['KDJ']['K'],
        d_value=analysis['KDJ']['D'],
        j_value=analysis['KDJ']['J'],
        analysis_result={
            'long_term_trend': analysis['KDJ']['long_term_trend'],
            'medium_term_trend': analysis['KDJ']['medium_term_trend'],
            'short_term_trend': analysis['KDJ']['short_term_trend'],
            'cross_pattern': analysis['KDJ']['cross_pattern'],
            'divergence': analysis['KDJ']['divergence'],
            'strength': analysis['KDJ']['strength'],
            'pattern': analysis['KDJ']['pattern'],
            'signal': analysis['KDJ']['signal']
        }
    )
    
    rsi_prompt = get_rsi_analysis_prompt(
        rsi6=analysis['RSI']['RSI6'],
        rsi12=analysis['RSI']['RSI12'],
        rsi24=analysis['RSI']['RSI24'],
        long_term_trend=analysis['RSI']['long_term_trend'],
        medium_term_trend=analysis['RSI']['medium_term_trend'],
        short_term_signal=analysis['RSI']['short_term_signal'],
        divergence=analysis['RSI']['divergence'],
        strength=analysis['RSI']['strength'],
        pattern=analysis['RSI']['pattern'],
        signal=analysis['RSI']['signal']
    )
    
    boll_prompt = get_boll_analysis_prompt(
        upper=analysis['BOLL']['UPPER'],
        mid=analysis['BOLL']['MID'],
        lower=analysis['BOLL']['LOWER'],
        long_term_trend=analysis['BOLL']['long_term_trend'],
        medium_term_trend=analysis['BOLL']['medium_term_trend'],
        short_term_signal=analysis['BOLL']['short_term_signal'],
        bandwidth=analysis['BOLL']['bandwidth'],
        pattern=analysis['BOLL']['pattern'],
        strength=analysis['BOLL']['strength'],
        signal=analysis['BOLL']['signal']
    )
    
    ma_prompt = get_ma_system_analysis_prompt(
        analysis_results={
            'ma_values': analysis['MA']['ma_values'],
            'long_term_trend': analysis['MA']['signals']['long_term_trend'],
            'medium_term_trend': analysis['MA']['signals']['medium_term_trend'],
            'short_term_signal': analysis['MA']['signals']['short_term_signal'],
            'formation': analysis['MA']['signals']['formation'],
            'strength': analysis['MA']['signals']['strength'],
            'support_resistance': analysis['MA']['signals']['support_resistance'],
            'signal': analysis['MA']['signals']['signal']
        }
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

{ma_prompt}

# 综合研判

请基于以上所有技术指标的分析结果，进行综合研判：

1. 多空力量对比
   - 结合各指标信号判断多空力量
   - 主力资金动向分析
   - 市场情绪研判
   - 均线系统排列形态研判

2. 趋势研判
   - 主趋势判断
   - 次级调整特征
   - 趋势持续性分析
   - 均线系统趋势确认

3. 支撑阻力分析
   - 关键价位识别
   - 均线支撑阻力位
   - 突破可能性分析
   - 风险点位预警

4. 综合操作建议
   - 短期操作策略
   - 中期布局建议
   - 风险控制要点
   - 分批建仓方案

注意事项：
- 分析需要客观、专业、严谨
- 必须有具体数据支撑
- 需要明确指出各个指标的信号含义
- 对于重要结论要给出具体依据
- 建议结合均线系统进行交叉验证
""" 