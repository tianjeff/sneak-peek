import sqlite3
from flask import (
    abort, redirect, url_for, session)
from flask import (
    Flask, flash, render_template, send_from_directory, request)

import os
from werkzeug.utils import secure_filename

import string
import re
import json

DEFAULT_URL = 'https://st3.depositphotos.com/23594922/31822/v/600/depositphotos_318221368-stock-illustration-missing-picture-page-for-website.jpg'

with open('sku_to_image.json') as infile:
    sku_to_img_dict = json.load(infile)

# app is a single object used by all the code modules in this package
app = Flask(__name__)  # pylint: disable=invalid-name
app.secret_key = b'T\xd0\x19a9=\xdb$L\x94\xedo\x08mw\xa4\\5m\xcc\xa1\xffn\x13'

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
    for (snkrid, snkrname, sku, size, price) in old_results:
        if sku not in sku_dict:
            sku_dict[sku] = []
            snkr_list.append((snkrname, sku, sku_to_img_dict[sku]))
        sku_dict[sku].append((size, price))

    results = {'snkr_list': snkr_list, 'sku_dict': sku_dict}
    print(results)

    return render_template('index.html', **results)

@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        form_data = request.form

        search_val = form_data['search']

        if not search_val:
            return redirect('/')

        print("searched for: ", search_val)

        conn = get_db_connection()
        old_results = conn.execute('SELECT * FROM sneakers ORDER BY size ASC').fetchall()
        conn.close()

        snkr_list = []
        sku_dict = {}
        for (snkrid, snkrname, sku, size, price) in old_results:
            if search_val.lower() not in snkrname.lower() and search_val.lower() not in sku.lower():
                continue
            if sku not in sku_dict:
                sku_dict[sku] = []
                snkr_list.append((snkrname, sku, sku_to_img_dict[sku]))
            sku_dict[sku].append((size, price))

        results = {'snkr_list': snkr_list, 'sku_dict': sku_dict}
        print(results)

        return render_template('index.html', **results)


@app.route('/create')
def create():
    return render_template('create.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def dump_sku_to_image_dict():
    outfile = open('sku_to_image.json', 'w')
    json.dump(sku_to_img_dict, outfile)
    outfile.close()

@app.route('/create', methods = ['POST'])
def add():
    if request.method == 'POST':

        # this part isn't working

        conn = get_db_connection()

        snkrname = request.form['snkrname'].strip()
        sku = request.form['sku'].strip()
        size = request.form['size'].strip()
        price = str(request.form['price']).strip()
        img_url = request.form['image'].strip()

        if not snkrname or not sku or not size or not price:
            flash('missing parameters')
            return redirect('/')

        snkrname = string.capwords(snkrname)

        sku = sku.replace(' ', '-')

        price = re.sub("[^0-9]", "", price)

        if img_url: # create new url or replace current url
            sku_to_img_dict[sku] = img_url
            dump_sku_to_image_dict()
        elif sku not in sku_to_img_dict:
            sku_to_img_dict[sku] = DEFAULT_URL
            dump_sku_to_image_dict()

        new_snkrid = conn.execute('SELECT COUNT(*) FROM sneakers').fetchone()['COUNT(*)'] + 1
        results = conn.execute('INSERT INTO sneakers (snkrid, snkrname, sku, size, price) '
                    'VALUES (?, ?, ?, ?, ?)', (new_snkrid, snkrname, sku, size, price, )             
                )

        conn.commit()
        results = conn.execute('SELECT * FROM sneakers ORDER BY size ASC').fetchall()
        conn.close()

        return redirect('/')