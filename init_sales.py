import sqlite3

connection = sqlite3.connect('sales.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO sales (snkrid, snkrname, sku, size, bought, sold, profit) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (0, 'Jordan 1 Shadow 2018', '555088-013', 12, 500, 600, 100)
            )

connection.commit()
connection.close()