import sqlite3
from flask import (
    abort, redirect, url_for, session)
from flask import (
    Flask, render_template, send_from_directory, request)

# app is a single object used by all the code modules in this package
app = Flask(__name__)  # pylint: disable=invalid-name

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    old_results = conn.execute('SELECT * FROM sneakers ORDER BY size ASC').fetchall()
    conn.close()

    snkr_list = []
    sku_dict = {}
    for (snkrid, snkrname, sku, imgname, size, price) in old_results:
        if sku not in sku_dict:
            sku_dict[sku] = []
            snkr_list.append((snkrname, sku, imgname))
        sku_dict[sku].append((size, price))

    results = {'snkr_list': snkr_list, 'sku_dict': sku_dict}
    print(results)

    return render_template('index.html', **results)

@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        form_data = request.form

        search_val = form_data['search']

        print("searched for: ", search_val)

        conn = get_db_connection()
        old_results = conn.execute('SELECT * FROM sneakers ORDER BY size ASC').fetchall()
        conn.close()

        snkr_list = []
        sku_dict = {}
        for (snkrid, snkrname, sku, imgname, size, price) in old_results:
            if search_val.lower() not in snkrname.lower() and search_val.lower() not in sku.lower():
                continue
            if sku not in sku_dict:
                sku_dict[sku] = []
                snkr_list.append((snkrname, sku, imgname))
            sku_dict[sku].append((size, price))

        results = {'snkr_list': snkr_list, 'sku_dict': sku_dict}
        print(results)

        return render_template('index.html', **results)