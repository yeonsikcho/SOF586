import pandas as pd
import psycopg2
# import MySQLdb as sql
df = pd.read_excel("menu_prices.xlsx")
con = psycopg2.connect(host = 'hostinger.eric-cho.com', database = 'postgres', user = 'postgres', password = '0501cho', port = '5432')
# con = sql.connect(host = 'analytiq.co.kr', user = 'sof586', database = 'sof586', charset = 'utf8')
cursor = con.cursor()
for i,d in df.iterrows():
    cursor.execute("insert into sof586.menu_items values (%s,%s,%s) on duplicate key update menu_name = %s, price = %s"
    ,[d['id'], d['menu'], d['price'], d['menu'], d['price']])
con.commit()