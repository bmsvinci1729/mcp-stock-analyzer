import sqlite3
stocks = ['AAPL','AMZN','GOOGL','META','MSFT','NVDA','TSLA']
conn = sqlite3.connect('database/stocks.db')
c = conn.cursor()
out = []
for s in stocks:
    c.execute('SELECT price, timestamp FROM real_stock_data WHERE symbol=? ORDER BY timestamp DESC LIMIT 2', (s,))
    rows = c.fetchall()
    if len(rows)==2:
        out.append({'symbol':s,'current':rows[0][0],'current_time':rows[0][1],'prev':rows[1][0],'prev_time':rows[1][1]})
print(out)
conn.close()
