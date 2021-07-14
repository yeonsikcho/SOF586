import pandas as pd
import MySQLdb as sql
df = pd.read_excel("menu_prices.xlsx")
con = sql.connect(host = 'analytiq.co.kr', user = 'sof586', database = 'sof586', charset = 'utf8')
cursor = con.cursor()
for i,d in df.iterrows():
    cursor.execute("insert into menu_items values (%s,%s,%s) on duplicate key update menu_name = %s, price = %s"
    ,[d['id'], d['menu'], d['price'], d['menu'], d['price']])
con.commit()