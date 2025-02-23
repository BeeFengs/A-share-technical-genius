"""
这是一个简单的 Tushare API 测试文件，专门用于测试 daily 和 stk_factor_pro 接口
"""

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import signal
from contextlib import contextmanager
import time

class TimeoutException(Exception):
    pass

@contextmanager
def timeout(seconds):
    def timeout_handler(signum, frame):
        raise TimeoutException("操作超时")

    # 设置信号处理器
    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)

def test_tushare_api():
    """测试Tushare API连接和数据获取"""
    try:
        # 加载环境变量
        load_dotenv()
        
        # 获取 token
        token = os.getenv('TUSHARE_TOKEN')
        if not token:
            print("错误：未找到 TUSHARE_TOKEN 环境变量")
            print("请在 .env 文件中设置 TUSHARE_TOKEN=你的token")
            return
            
        print(f"使用的 token: {token[:8]}...")  # 只显示前8位
        
        # 设置 token 并初始化 API
        ts.set_token(token)
        pro = ts.pro_api()
        
        # 测试基础连接
        print("\n测试API连接...")
        try:
            with timeout(5):  # 设置5秒超时
                start_time = time.time()
                df_test = pro.query('stock_basic', limit=1)
                end_time = time.time()
                print(f"API连接成功！耗时: {end_time - start_time:.2f}秒")
        except TimeoutException:
            print("API连接超时（5秒）")
            return
        except Exception as e:
            print(f"API连接测试失败: {str(e)}")
            return
        
        # 设置测试参数
        stock_code = '000001.SZ'  # 平安银行
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=5)).strftime('%Y%m%d')
        
        print(f"\n1. 测试 daily 接口（以平安银行为例）：")
        print(f"获取日期范围: {start_date} 到 {end_date}")
        
        # 添加超时设置和错误处理
        try:
            with timeout(5):  # 设置5秒超时
                df = pro.daily(ts_code=stock_code, 
                             start_date=start_date,
                             end_date=end_date)
                
                if df is not None and not df.empty:
                    print("\n获取数据成功！数据预览：")
                    print(df.head())
                else:
                    print("\n未获取到数据")
        except TimeoutException:
            print("获取数据超时（5秒）")
            return
            
        # 测试获取专业版因子数据
        print("\n2. 测试 stk_factor_pro 接口：")
        try:
            df_factor = pro.stk_factor_pro(
                ts_code='000001.SZ',
                start_date=start_date,
                end_date=end_date,
                fields='ts_code,trade_date,macd_dif_qfq,macd_dea_qfq,macd_qfq,kdj_k_qfq,kdj_d_qfq,kdj_j_qfq,rsi_6_qfq,rsi_12_qfq,rsi_24_qfq,boll_upper_qfq,boll_mid_qfq,boll_lower_qfq,cci_qfq,atr_qfq,psy_qfq,vr_qfq,trix_qfq,obv_qfq,wr_qfq,mtm_qfq,dmi_pdi_qfq,dmi_mdi_qfq,dmi_adx_qfq,cr_qfq,cr_ma1_qfq,cr_ma2_qfq,cr_ma3_qfq,emv_qfq,emv_ma_qfq'
            )
            if df_factor is not None and not df_factor.empty:
                print(f"成功获取从 {start_date} 到 {end_date} 的专业版因子数据：")
                print(df_factor.head())
                print("\n专业版因子数据列名：")
                print(df_factor.columns.tolist())
                
                # 检查KDJ指标是否存在
                kdj_columns = [col for col in df_factor.columns if 'kdj' in col.lower()]
                print("\nKDJ相关列：")
                print(kdj_columns)
                
                # 检查MACD指标是否存在
                macd_columns = [col for col in df_factor.columns if 'macd' in col.lower()]
                print("\nMACD相关列：")
                print(macd_columns)
            else:
                print("专业版因子数据获取失败或为空")
        except Exception as e:
            print(f"专业版因子数据获取出错：{str(e)}")
            print("可能原因：")
            print("1. 没有专业版接口的权限")
            print("2. 接口名称或参数不正确")
            print("3. 服务器响应超时")
        
        print("\nTushare API 测试完成！")
        
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        print("\n请检查：")
        print("1. Token 是否正确")
        print("2. 网络连接是否正常")
        print("3. 是否有对应的接口权限")

if __name__ == "__main__":
    test_tushare_api() 