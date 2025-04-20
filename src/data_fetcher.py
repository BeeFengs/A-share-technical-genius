"""
数据获取模块 - 负责从Tushare获取股票日线数据和技术指标
"""
import os
import tushare as ts
from dotenv import load_dotenv
import pandas as pd



class TushareDataFetcher:
    def __init__(self):
        load_dotenv()
        token = os.getenv('TUSHARE_TOKEN')

        print(f"Tushare Token: {token}")
        if not token:
            raise ValueError("请在.env文件中设置TUSHARE_TOKEN")
        
        # 初始化pro接口
        ts.set_token(token)
        self.pro = ts.pro_api()
        
    def get_stock_data(self, ts_code, start_date=None, end_date=None):
        """
        获取股票日线数据和技术指标
        
        参数:
            ts_code (str): 股票代码（如：000001.SZ）
            start_date (str): 开始日期（如：20230101）
            end_date (str): 结束日期（如：20240214）
            
        返回:
            pandas.DataFrame: 包含日线数据和技术指标的DataFrame
        """
        try:
            # 获取日线数据
            df_daily = self.pro.daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
            )
            
            if df_daily is None or df_daily.empty:
                

                print("获取日线数据失败")
                return None
            
            # 获取技术指标数据
            df_factor = self.pro.stk_factor(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                fields='ts_code,trade_date,macd_dif,macd_dea,macd,kdj_k,kdj_d,kdj_j,rsi_6,rsi_12,rsi_24,boll_upper,boll_mid,boll_lower'
            )
            
            # 获取MA均线数据
            df_ma = self.pro.stk_factor_pro(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                fields='ts_code,trade_date,ma_qfq_5,ma_qfq_10,ma_qfq_20,ma_qfq_30,ma_qfq_60,ma_qfq_90,ma_qfq_250'
            )
            
            if df_factor is None or df_factor.empty:
                print("获取技术指标数据失败")
                return None
                
            if df_ma is None or df_ma.empty:
                print("获取MA均线数据失败")
                return None
                
            # 合并所有数据
            df = pd.merge(df_daily, df_factor, on=['ts_code', 'trade_date'], how='left')
            df = pd.merge(df, df_ma, on=['ts_code', 'trade_date'], how='left')
            
            # 按日期升序排序
            df = df.sort_values('trade_date')
            
            # 重命名列
            df = df.rename(columns={'pct_chg': 'pct_change'})
            
            return df
            
        except Exception as e:
            #打印失败原因

            print(f"获取数据失败: {str(e)}")
            return None

    def get_stock_basic(self):
        """
        获取股票基础信息
        """
        try:
            return self.pro.stock_basic(
                exchange='',
                list_status='L',
                fields='ts_code,symbol,name,area,industry,list_date'
            )
        except Exception as e:
            print(f"获取股票基础信息失败: {str(e)}")
            return None 