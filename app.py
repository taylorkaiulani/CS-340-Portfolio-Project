from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import os

# Configuration
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_homant'
app.config['MYSQL_PASSWORD'] = '5093'
app.config['MYSQL_DB'] = 'cs340_homant'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 
@app.route('/')
def root():
    return ("Hello world!")

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2896))
    app.run(port=port, debug=True)