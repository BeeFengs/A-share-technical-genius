"""
主程序入口 - 技术指标分析程序
"""
import os
from dotenv import load_dotenv
from src.data_fetcher import TushareDataFetcher
from src.visualizer import TechnicalVisualizer
from src.report_generator import ReportGenerator
from src.analyzers import analyze_indicators
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
    print(f"DIF值: {analysis['MACD']['DIF']:.2f}")
    print(f"DEA值: {analysis['MACD']['DEA']:.2f}")
    print(f"MACD值: {analysis['MACD']['MACD']:.2f}")
    print(f"长期趋势: {analysis['MACD']['long_term_trend']}")
    print(f"中期趋势: {analysis['MACD']['medium_term_trend']}")
    print(f"短期信号: {analysis['MACD']['short_term_signal']}")
    print(f"背离情况: {analysis['MACD']['divergence']}")
    print(f"指标强度: {analysis['MACD']['strength']}")
    print(f"综合信号: {analysis['MACD']['signal']}")
    
    print("\nKDJ分析:")
    print(f"K值: {analysis['KDJ']['K']:.2f}")
    print(f"D值: {analysis['KDJ']['D']:.2f}")
    print(f"J值: {analysis['KDJ']['J']:.2f}")
    print(f"长期趋势: {analysis['KDJ']['long_term_trend']}")
    print(f"中期趋势: {analysis['KDJ']['medium_term_trend']}")
    print(f"短期趋势: {analysis['KDJ']['short_term_trend']}")
    print(f"交叉形态: {analysis['KDJ']['cross_pattern']}")
    print(f"背离情况: {analysis['KDJ']['divergence']}")
    print(f"指标强度: {analysis['KDJ']['strength']}")
    print(f"形态特征: {analysis['KDJ']['pattern']}")
    print(f"综合信号: {analysis['KDJ']['signal']}")
    
    print("\nRSI分析:")
    print(f"RSI指标值:")
    print(f"  - RSI6: {analysis['RSI']['RSI6']:.2f}")
    print(f"  - RSI12: {analysis['RSI']['RSI12']:.2f}")
    print(f"  - RSI24: {analysis['RSI']['RSI24']:.2f}")
    print(f"\n趋势分析:")
    print(f"  - 长期趋势: {analysis['RSI']['long_term_trend']}")
    print(f"  - 中期趋势: {analysis['RSI']['medium_term_trend']}")
    print(f"  - 短期信号: {analysis['RSI']['short_term_signal']}")
    print(f"\n形态分析:")
    print(f"  - RSI形态: {analysis['RSI']['pattern']}")
    print(f"  - 背离情况: {analysis['RSI']['divergence']}")
    print(f"  - 指标强度: {analysis['RSI']['strength']}")
    print(f"\n综合判断:")
    print(f"  - {analysis['RSI']['signal']}")
    
    print("\nBOLL分析:")
    print(f"布林带指标值:")
    print(f"  - 上轨: {analysis['BOLL']['UPPER']:.2f}")
    print(f"  - 中轨: {analysis['BOLL']['MID']:.2f}")
    print(f"  - 下轨: {analysis['BOLL']['LOWER']:.2f}")
    print(f"\n趋势分析:")
    print(f"  - 长期趋势: {analysis['BOLL']['long_term_trend']}")
    print(f"  - 中期趋势: {analysis['BOLL']['medium_term_trend']}")
    print(f"  - 短期信号: {analysis['BOLL']['short_term_signal']}")
    print(f"\n形态分析:")
    print(f"  - 带宽状态: {analysis['BOLL']['bandwidth']}")
    print(f"  - 形态特征: {analysis['BOLL']['pattern']}")
    print(f"  - 指标强度: {analysis['BOLL']['strength']}")
    print(f"\n综合判断:")
    print(f"  - {analysis['BOLL']['signal']}")
    
    # 绘制图表
    stock_name = stocks[stocks['ts_code'] == ts_code]['name'].values[0]
    visualizer = TechnicalVisualizer()
    fig = visualizer.plot_indicators(df, stock_name)
    
    # 获取最新价格和变化
    latest_price = df['close'].iloc[-1]
    price_change = (df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2] * 100
    vol_change = (df['vol'].iloc[-1] - df['vol'].iloc[-2]) / df['vol'].iloc[-2] * 100
    
    # 生成分析报告
    print("\n正在生成AI分析报告...")
    report_generator = ReportGenerator()
    
    # 生成综合分析报告
    report = report_generator.generate_report(stock_name, analysis, df)
    
    # 生成各个技术指标的独立报告
    indicators = ['MACD', 'KDJ', 'RSI', 'BOLL']
    for indicator in indicators:
        print(f"\n正在生成{indicator}指标分析报告...")
        indicator_report = report_generator.generate_indicator_report(
            stock_name=stock_name,
            indicator_name=indicator,
            latest_price=latest_price,
            price_change=price_change,
            vol_change=vol_change,
            analysis=analysis
        )
        report_file = report_generator.save_indicator_report(
            stock_name=stock_name,
            indicator_name=indicator,
            report_content=indicator_report
        )
        print(f"{indicator}指标分析报告已保存至: {report_file}")
    
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