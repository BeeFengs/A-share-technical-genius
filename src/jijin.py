import tushare as ts
import os
from dotenv import load_dotenv

load_dotenv()

pro = ts.pro_api(os.getenv('TUSHARE_TOKEN'))

df = pro.fund_basic(market='E')
# df.to_csv('fund_basic.csv', index=False, encoding='utf-8-sig')

# pro = ts.pro_api()

df1 = pro.fund_portfolio(ts_code='001753.OF')
print(df1)
df1.to_csv("test.csv",index=False)