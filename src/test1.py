import tushare as ts
import asyncio
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 设置Tushare Token
ts.set_token('10baf45534f5fe68faa3023ac9cf9a667f29e5c732ba3c3dffdecf9c')
pro = ts.pro_api()

# MySQL数据库配置
DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/quant'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

# 定义SQLAlchemy的数据表模型
class StockData(Base):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(10))
    trade_date = Column(String(8))
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    pre_close = Column(Float)
    change = Column(Float)
    pct_chg = Column(Float)
    vol = Column(Float)
    amount = Column(Float)

# 获取A股的股票代码列表（深交所、上交所、创业板）
async def get_stock_codes():
    stock_codes = []
    try:
        logger.info("Fetching stock codes...")
        # 获取深交所和上交所的A股股票代码
        stock_codes = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')
        
        logger.info(f"Fetched {len(stock_codes)} stock codes.")
    except Exception as e:
        logger.error(f"Error fetching stock codes: {e}")
    return stock_codes

# 异步获取股票的日线数据
async def fetch_data(ts_code, start_date, end_date):
    try:
        logger.info(f"Fetching data for {ts_code} from {start_date} to {end_date}...")
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df.empty:
            logger.warning(f"No data found for {ts_code} in the given date range.")
        return df
    except Exception as e:
        logger.error(f"Error fetching data for {ts_code}: {e}")
        return None

# 异步将数据插入到MySQL数据库
async def insert_data(df):
    if df is None or df.empty:
        return
    try:
        logger.info("Inserting data into MySQL...")
        Session = sessionmaker(bind=engine)
        session = Session()

        for _, row in df.iterrows():
            stock_data = StockData(
                ts_code=row['ts_code'],
                trade_date=row['trade_date'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                pre_close=row['pre_close'],
                change=row['change'],
                pct_chg=row['pct_chg'],
                vol=row['vol'],
                amount=row['amount']
            )
            session.add(stock_data)

        session.commit()
        session.close()
        logger.info("Data inserted successfully.")
    except Exception as e:
        logger.error(f"Error inserting data into MySQL: {e}")

# 异步主函数
async def main():
    start_date = '20230101'  # 数据开始日期
    end_date = '20230331'    # 数据结束日期

    try:
        logger.info("Starting data processing...")
        # 获取所有A股股票代码（深交所、上交所、创业板）
        stock_codes = await get_stock_codes()

        # 获取日线数据并插入数据库
        tasks = []
        for ts_code in stock_codes:
            tasks.append(fetch_data(ts_code, start_date, end_date))

        # 执行所有异步任务
        results = await asyncio.gather(*tasks)

        # 将所有股票数据插入数据库
        for df in results:
            if df is not None and not df.empty:
                await insert_data(df)

        logger.info("Data processing completed.")
    except Exception as e:
        logger.error(f"Error in main process: {e}")

# 运行异步主程序
if __name__ == "__main__":
    # 创建数据库表（如果尚未创建）
    Base.metadata.create_all(engine)

    # 运行程序
    asyncio.run(main())
