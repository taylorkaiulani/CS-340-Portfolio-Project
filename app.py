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

@app.route('/artist-performances', methods = ['GET', 'POST'])
def concert_artists():
    if request.method == 'GET':
        pass
    
    elif request.method == 'POST':
        pass

@app.route('/edit-performance/<int:id>', methods = ['GET', 'POST'])
def edit_concert_artists(id):
    if request.method == 'GET':
        # Get performance info to display
        query1 = "SELECT artistID AS `Artist`, concertID AS `Performance` FROM Concert_Artists WHERE concert_artistID = '%s';" % (id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # Get artist info for drop down
        query2 = "SELECT artistID, name FROM Artists"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        artists = cursor.fetchall()

        # Get concert info for drop down
        query3 = "SELECT Concerts.concertID AS `concertID`, date AS `date`, Venues.name AS `venue` FROM Concerts JOIN Venues ON Venues.venueID = Concerts.venueID;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        concerts = cursor.fetchall()

        return render_template('EditArtistPerformances.j2', data=data, artists=Artists, Concerts=concerts)
    
    elif request.method == 'POST':
        # Get form inputs
        concert_artistID = request.form['concert_artistID']
        concertID = request.form['concertID']
        artistID = request.form['artistID']

        # Update the database
        query = "UPDATE Concert_Artists SET concertID = '%s', artistID = '%s' WHERE concert_artistID = '%s';"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (concertID, artistID, concert_artistID))
        mysql.connection.commit()

        return redirect('/artist-performances')


@app.route('/delete-performance/<int:id>')
def delete_concert_artist(id):
    query = "DELETE FROM Concert_Artists WHERE concert_artistID = '%s';"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (id,))
    mysql.connection.commit()

    return redirect('/artist-performances')


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2896))
    app.run(port=port, debug=True)