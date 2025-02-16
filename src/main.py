"""
主程序入口 - 技术指标分析程序
"""
import os
from dotenv import load_dotenv
from data_fetcher import TushareDataFetcher
from visualizer import TechnicalVisualizer
from report_generator import ReportGenerator
from datetime import datetime, timedelta
import calendar

def get_date_range(lookback_months=2):
    """
    获取动态的日期范围
    Args:
        lookback_months: 回溯月数，默认2个月
    Returns:
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)
    """
    end_date = datetime.now()
    
    # 计算起始日期（前N个月的1号）
    if end_date.month > lookback_months:
        start_month = end_date.month - lookback_months
        start_year = end_date.year
    else:
        start_month = end_date.month + 12 - lookback_months
        start_year = end_date.year - 1
    
    start_date = datetime(start_year, start_month, 1)
    
    return (
        start_date.strftime('%Y%m%d'),
        end_date.strftime('%Y%m%d')
    )

def analyze_indicators(df):
    """
    分析最新的技术指标数据
    """
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    analysis = {}
    
    # MACD分析
    analysis['MACD'] = {
        'DIF': latest['macd_dif'],
        'DEA': latest['macd_dea'],
        'MACD': latest['macd'],
        'signal': '金叉' if latest['macd'] > 0 and prev['macd'] < 0 else 
                 '死叉' if latest['macd'] < 0 and prev['macd'] > 0 else '无信号'
    }
    
    # KDJ分析
    analysis['KDJ'] = {
        'K': latest['kdj_k'],
        'D': latest['kdj_d'],
        'J': latest['kdj_j'],
        'signal': '超买' if latest['kdj_j'] > 100 else 
                 '超卖' if latest['kdj_j'] < 0 else '正常'
    }
    
    # RSI分析
    analysis['RSI'] = {
        'RSI6': latest['rsi_6'],
        'RSI12': latest['rsi_12'],
        'RSI24': latest['rsi_24'],
        'signal': '超买' if latest['rsi_6'] > 80 else
                 '超卖' if latest['rsi_6'] < 20 else '正常'
    }
    
    # BOLL分析
    analysis['BOLL'] = {
        'UPPER': latest['boll_upper'],
        'MID': latest['boll_mid'],
        'LOWER': latest['boll_lower'],
        'signal': '突破上轨' if latest['close'] > latest['boll_upper'] else
                 '突破下轨' if latest['close'] < latest['boll_lower'] else '区间内波动'
    }
    
    return analysis

def main():
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据获取器
    fetcher = TushareDataFetcher()
    
    # 获取股票列表
    stocks = fetcher.get_stock_basic()
    if stocks is None:
        print("获取股票列表失败")
        return
    
    # 获取用户输入
    print("\n可用的股票列表:")
    print(stocks[['ts_code', 'name']].head())
    print("...")
    
    ts_code = input("\n请输入股票代码（如：000001.SZ）: ")
    
    # 自动获取日期范围
    start_date, end_date = get_date_range()
    print(f"\n分析时间范围：{start_date} 至 {end_date}")
    
    # 获取数据
    df = fetcher.get_stock_data(ts_code, start_date, end_date)
    if df is None:
        print("获取数据失败")
        return
    
    # 分析指标
    analysis = analyze_indicators(df)
    
    # 打印分析结果
    print("\n=== 技术指标分析结果 ===")
    
    print("\nMACD分析:")
    print(f"DIF: {analysis['MACD']['DIF']:.2f}")
    print(f"DEA: {analysis['MACD']['DEA']:.2f}")
    print(f"MACD: {analysis['MACD']['MACD']:.2f}")
    print(f"信号: {analysis['MACD']['signal']}")
    
    print("\nKDJ分析:")
    print(f"K值: {analysis['KDJ']['K']:.2f}")
    print(f"D值: {analysis['KDJ']['D']:.2f}")
    print(f"J值: {analysis['KDJ']['J']:.2f}")
    print(f"信号: {analysis['KDJ']['signal']}")
    
    print("\nRSI分析:")
    print(f"RSI6: {analysis['RSI']['RSI6']:.2f}")
    print(f"RSI12: {analysis['RSI']['RSI12']:.2f}")
    print(f"RSI24: {analysis['RSI']['RSI24']:.2f}")
    print(f"信号: {analysis['RSI']['signal']}")
    
    print("\nBOLL分析:")
    print(f"上轨: {analysis['BOLL']['UPPER']:.2f}")
    print(f"中轨: {analysis['BOLL']['MID']:.2f}")
    print(f"下轨: {analysis['BOLL']['LOWER']:.2f}")
    print(f"信号: {analysis['BOLL']['signal']}")
    
    # 绘制图表
    stock_name = stocks[stocks['ts_code'] == ts_code]['name'].values[0]
    visualizer = TechnicalVisualizer()
    fig = visualizer.plot_indicators(df, stock_name)
    
    # 生成分析报告
    print("\n正在生成AI分析报告...")
    report_generator = ReportGenerator()
    report = report_generator.generate_report(stock_name, analysis, df)
    
    # 打印分析思路
    print("\n=== AI 分析思路 ===")
    print(report['thoughts'])
    
    print("\n=== AI 分析报告 ===")
    print(report['analysis'])
    
    # 保存图表
    fig.write_html(f"technical_analysis_{ts_code}.html")
    print(f"\n分析图表已保存为: technical_analysis_{ts_code}.html")

if __name__ == "__main__":
    main() 