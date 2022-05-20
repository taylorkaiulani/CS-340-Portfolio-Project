from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import database.db_connector as db
import os

# Configuration
app = Flask(__name__)
db_connection = db.connect_to_database()
mysql = MySQL(app)
# db_connection.ping(True)

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
        if request.form.get("insertArtistPerformance"):
            # grab user form inputs
            concert = request.form["concert"]
            artist = request.form["artist"]
            query = "INSERT INTO Concert_Artists (concert, artist) VALUES (%s, %s)"
            cur = db.execute_query(db_connection=db_connection, query=query)
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/ArtistPerformances")

    # Grab ArtistPerformances data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT concert_artistID AS `Performance ID`, Concerts.date AS Date, Artists.name AS `Artist` FROM Concert_Artists JOIN Artists ON Artists.artistID = Concert_Artists.artistID JOIN Concerts ON Concerts.concertID = Concert_Artists.concertID"
        cur = db.execute_query(db_connection=db_connection, query=query)
        data = cur.fetchall()

        # mySQL query to grab artist data for our dropdown
        query2 = "SELECT Artist from Artists"
        cur = db.execute_query(db_connection=db_connection, query=query)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("ArtistPerformances.j2", data=data, homeworlds=homeworld_data)


# Listener
if __name__ == "__main__":
    app.run(port=31669, debug=True)