"""
技术分析报告的prompt模板
"""
from src.analyzers.technical_indicators import analyze_indicators
import pandas as pd

def get_technical_analysis_prompt(stock_name: str, latest_price: float, price_change: float, \
                                vol_change: float, df: pd.DataFrame, analysis: dict) -> str:
    """
    生成技术分析报告的prompt模板
    
    参数:
        stock_name (str): 股票名称
        latest_price (float): 最新收盘价
        price_change (float): 涨跌幅
        vol_change (float): 成交量变化
        df (pd.DataFrame): 包含技术指标数据的DataFrame
        analysis (dict): 技术指标分析结果
        
    返回:
        str: 格式化后的prompt
    """
    # 获取各个指标的分析结果
    # 这里可以使用 analysis 参数来生成更详细的报告内容
    # 例如：
    # analysis_summary = analysis.get('summary', '无总结信息')
    
    return f"""

#Role    
您是一位精通技术分析的金融中国A股股票专家，擅长多指标共振分析，  

# 目标
请对以下个股{stock_name}的六大技术指标进行综合分析，给出客观的技术信号和参考建议，
# 要求
语言需要通俗易懂，适合普通投资者理解。

# 市场数据
## 基础行情
- 最新收盘价：{latest_price:.2f}
- 涨跌幅：{price_change:.2f}%
- 成交量变化：{vol_change:.2f}%

# 六大指标共振分析
## 1. K线形态分析
{analysis.get('Candlestick', '无数据')}  

## 2. MA系统分析
{analysis.get('MA', '无数据')}  

## 3. MACD分析
{analysis.get('MACD', '无数据')}  

## 4. KDJ分析
{analysis.get('KDJ', '无数据')}  

## 5. RSI分析
{analysis.get('RSI', '无数据')}  

## 6. BOLL分析
{analysis.get('BOLL', '无数据')}  

# 综合研判

请基于以上所有技术指标的分析结果，进行共振研判：

1. 计算总共振强度并用通俗语言表述市场技术面的整体倾向，如"多指标共振显示强积极信号"

2. 分别从趋势、动能和区间三个维度进行确认分析

3. 提供参考的短期和中期市场展望，使用"技术指标显示看多/看空信号"等表述代替直接的买卖建议

4. 列出关键价格区间（支撑位和压力位）

5. 分析潜在风险点，帮助用户全面了解市场情况

请使用简明易懂的语言，少用专业术语，必须使用时请提供简短解释。分析结果需要同时适合初学者和有一定经验的投资者阅读。

最后请以"以上分析仅代表技术面信息，供参考，不构成投资建议"作为结尾。
""" 