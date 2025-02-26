"""
测试数据获取模块 - 用于展示从Tushare获取的股票数据
"""
from data_fetcher import TushareDataFetcher
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

def fetch_and_save_data(stock_code, start_date, end_date):
    try:
        fetcher = TushareDataFetcher()
        df = fetcher.get_stock_data(stock_code, start_date=start_date, end_date=end_date)
        if df is not None:
            print("\n=== 数据基本信息 ===")
            print(f"数据形状: {df.shape}")
            print("\n=== 数据列名 ===")
            print(df.columns.tolist())
            print("\n=== 前5行数据预览 ===")
            print(df.head())
            return df
        else:
            print("获取数据失败")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def save_data_to_csv(df, stock_code):
    try:
        if not os.path.exists('../data'):
            os.makedirs('../data')
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'../data/stock_data_{stock_code.replace(".", "_")}_{current_time}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到文件: {filename}")
    except Exception as e:
        print(f"保存数据时发生错误: {e}")

def visualize_data(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['close'], label='收盘价', color='blue')
    plt.title('股票收盘价变化')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    stock_code = '000001.SZ'
    start_date = input('请输入开始日期 (格式: YYYYMMDD): ')
    end_date = input('请输入结束日期 (格式: YYYYMMDD): ')
    df = fetch_and_save_data(stock_code, start_date, end_date)
    if df is not None:
        save_data_to_csv(df, stock_code)
        visualize_data(df)

if __name__ == "__main__":
    main() 