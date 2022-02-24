import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO sneakers (snkrid, snkrname, sku, imgname, size, price) VALUES (?, ?, ?, ?, ?, ?)",
            (1, 'Jordan 1 Shadow 2018', '555088-013', 'https://cdn.flightclub.com/TEMPLATE/803598/1.jpg', 12, 500)
            )

connection.commit()
connection.close()