from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import database.db_connector as db
import os

# Configuration
app = Flask(__name__)
db_connection = db.connect_to_database()
mysql = MySQL(app)
db_connection.ping(True)

# Routes
# have homepage route to /people by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return redirect("/Home")

@app.route("/Home")
def Main():
    return render_template("Home.j2")

# route for ArtistPerformances page
@app.route("/ArtistPerformances", methods=["POST", "GET"])
def ArtistPerformances():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_ArtistPerformance"):
            # grab user form inputs
            concertID = request.form["concertID"]
            artistID = request.form["artistID"]
            query = "INSERT INTO Concert_Artists (concertID, artistID) VALUES (%s, %s)"
            # Update the database with new entry
            cur = db.execute_query(db_connection=db_connection, query=query, query_params=(concertID, artistID))
            db_connection.commit()

            # redirect back to people page
            return redirect("/ArtistPerformances")

    # Grab ArtistPerformances data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT concert_artistID AS `Performance ID`, Artists.name AS `Artist`, Concerts.date AS Date, Venues.name AS `Venue` FROM Concert_Artists JOIN Artists ON Artists.artistID = Concert_Artists.artistID JOIN Concerts ON Concerts.concertID = Concert_Artists.concertID JOIN Venues ON Venues.venueID = Concerts.venueID ORDER BY concert_artistID"
        cur = db.execute_query(db_connection=db_connection, query=query)
        data = cur.fetchall()

        # mySQL query to grab artist data for our dropdown
        query2 = "SELECT artistID, name FROM Artists"
        cur = db.execute_query(db_connection=db_connection, query=query2)
        artists = cur.fetchall()

        # Get concert info for drop down
        query3 = "SELECT concertID, date AS `date`, Venues.name AS `venue` FROM Concerts JOIN Venues ON Venues.venueID = Concerts.venueID"
        cur = db.execute_query(db_connection=db_connection, query=query3)
        concerts = cur.fetchall()

        # render page passing our query data
        return render_template("ArtistPerformances.j2", data=data, Artists=artists, Concerts=concerts)

@app.route('/EditPerformance/<int:id>', methods = ['GET', 'POST'])
def EditArtistPerformance(id):
    if request.method == 'GET':
        # Get performance info to display
        query1 = ("SELECT Artists.name AS `Artist`, Venues.name AS `Venue`, Concerts.date AS `Date`, concert_artistID FROM Concert_Artists JOIN Concerts ON Concert_Artists.concertID = Concerts.concertID "
        + "JOIN Venues ON Venues.venueID = Concerts.venueID "
        + "JOIN Artists ON Concert_Artists.artistID = Artists.artistID "
        + "WHERE concert_artistID = %s") % (id)
        cur = db.execute_query(db_connection=db_connection, query=query1)
        data = cur.fetchall()

        # Get artist info for drop down
        query2 = "SELECT artistID, name FROM Artists"
        cur = db.execute_query(db_connection=db_connection, query=query2)
        artists = cur.fetchall()

        # Get concert info for drop down
        query3 = "SELECT concertID, date AS `date`, Venues.name AS `venue` FROM Concerts JOIN Venues ON Venues.venueID = Concerts.venueID"
        cur = db.execute_query(db_connection=db_connection, query=query3)
        concerts = cur.fetchall()

        return render_template('EditArtistPerformances.j2', data=data, Artists=artists, Concerts=concerts)

    elif request.method == 'POST':
        # Get form inputs
        concert_artistID = request.form['concert_artistID']
        concertID = request.form['concertID']
        artistID = request.form['artistID']

        # Update the database
        query = "UPDATE Concert_Artists SET concertID = %s, artistID = %s WHERE concert_artistID = %s"
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(concertID, artistID, concert_artistID))
        db_connection.commit()

        return redirect('/ArtistPerformances')

@app.route('/DeletePerformance/<int:id>')
def delete_concert_artist(id):
    query = "DELETE FROM Concert_Artists WHERE concert_artistID = %s" % (id)
    cur = db.execute_query(db_connection=db_connection, query=query)
    db_connection.commit()

    return redirect('/ArtistPerformances')

# Listener
if __name__ == "__main__":
    app.run(port=31669, debug=True)