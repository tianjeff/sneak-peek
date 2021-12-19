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
    results = conn.execute('SELECT * FROM sneakers').fetchall()
    conn.close()
    return render_template('index.html', results=results)