from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import database.db_connector as db
import os

# Configuration
app = Flask(__name__)
db_connection = db.connect_to_database()
mysql = MySQL(app)

# Routes 
@app.route('/')
def root():
    return ("Hello world!")

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2896))
    app.run(port=port, debug=True)