from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv, find_dotenv
# import database.db_connector as db

# Configuration
app = Flask(__name__)

load_dotenv(find_dotenv())

# db_connection = db.connect_to_database()

app.config['MYSQL_HOST'] = os.environ.get("340DBHOST")
app.config['MYSQL_USER'] = os.environ.get("340DBUSER")
app.config['MYSQL_PASSWORD'] = os.environ.get("340DBPW")
app.config['MYSQL_DB'] = os.environ.get("340DB")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 
@app.route('/')
def root():
    # Test to make sure the app is connected to the database
    query = "SHOW TABLES;"

    cursor = mysql.connection.cursor()
    cursor.execute(query)
    results = json.dumps(cursor.fetchall())

    return results

@app.route('/artist-performances', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def concert_artists():
    if request.method == 'GET':
        pass
    
    elif request.method == 'POST':
        pass

    elif request.method == 'PUT':
        pass
    
    elif request.method == 'DELETE':
        pass

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2896))
    app.run(port=port, debug=True)