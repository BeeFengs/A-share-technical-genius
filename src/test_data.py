"""
测试数据获取模块 - 用于展示从Tushare获取的股票数据
"""
from data_fetcher import TushareDataFetcher
import pandas as pd
import os
from datetime import datetime

def main():
    # 初始化数据获取器
    fetcher = TushareDataFetcher()
    
    # 获取平安银行(000001.SZ)最近30天的数据作为示例
    stock_code = '000001.SZ'
    df = fetcher.get_stock_data(stock_code, start_date='20250101', end_date='20250220')
    
    if df is not None:
        print("\n=== 数据基本信息 ===")
        print(f"数据形状: {df.shape}")
        print("\n=== 数据列名 ===")
        print(df.columns.tolist())
        print("\n=== 前5行数据预览 ===")
        print(df.head())
        
        # 创建data目录（如果不存在）
        if not os.path.exists('../data'):
            os.makedirs('../data')
            
        # 生成文件名（包含股票代码和当前时间）
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'../data/stock_data_{stock_code.replace(".", "_")}_{current_time}.csv'
        
        # 保存为CSV文件
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到文件: {filename}")
        
        print("\n=== 数据统计信息 ===")
        print(df.describe())
    else:
        print("获取数据失败")

if __name__ == "__main__":
    main() 