"""
这是一个简单的 Tushare API 测试文件，专门用于测试 daily 和 stk_factor 接口
"""

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

def test_tushare_api():
    # 加载环境变量
    load_dotenv()
    
    # 获取 token
    token = os.getenv('TUSHARE_TOKEN')
    if not token:
        print("错误：未找到 TUSHARE_TOKEN 环境变量")
        return
    
    # 设置 token
    ts.set_token(token)
    
    # 初始化 pro 接口
    pro = ts.pro_api()
    
    try:
        # 测试获取日线数据
        print("\n1. 测试 daily 接口（以平安银行为例）：")
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=10)).strftime('%Y%m%d')
        
        df_daily = pro.daily(ts_code='000001.SZ', 
                           start_date=start_date,
                           end_date=end_date)
        if df_daily is not None and not df_daily.empty:
            print(f"成功获取从 {start_date} 到 {end_date} 的日线数据：")
            print(df_daily)
        else:
            print("日线数据获取失败或为空")
        
        # 测试获取因子数据
        print("\n2. 测试 stk_factor 接口：")
        df_factor = pro.stk_factor(ts_code='000001.SZ',
                                 start_date=start_date,
                                 end_date=end_date)
        if df_factor is not None and not df_factor.empty:
            print(f"成功获取从 {start_date} 到 {end_date} 的因子数据：")
            print(df_factor)
        else:
            print("因子数据获取失败或为空")
        
        print("\nTushare API 测试完成！")
        
    except Exception as e:
        print(f"\n错误：API 调用出现异常：{str(e)}")
        print("请检查：")
        print("1. Token 是否正确")
        print("2. 网络连接是否正常")
        print("3. 是否有对应的接口权限")

if __name__ == "__main__":
    test_tushare_api() 