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
    return redirect("/Index")

@app.route("/Index")
def Main():
    return render_template("Index.j2")


# routes for Concerts page
@app.route("/Concerts", methods=['GET', 'POST'])
def Concerts():
    if request.method == 'GET':
        query1 = ("SELECT concertID AS `Concert ID`, date AS `Date`, Venues.name AS `Venue` "
            + "FROM Concerts JOIN Venues ON Concerts.venueID = Venues.venueID "
            + "ORDER BY concertID ASC")
        cur = db.execute_query(db_connection=db_connection, query=query1)
        data = cur.fetchall()

        query2 = ("SELECT venueID, name FROM Venues")
        cur = db.execute_query(db_connection=db_connection, query=query2)
        venues = cur.fetchall()

        return render_template('Concerts.j2', data=data, venues=venues)
    
    elif request.method == 'POST':
        date = request.form["date"]
        venueID = request.form["venueID"]

        query = "INSERT INTO Concerts (date, venueID) VALUES (%s, %s)"
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(date, venueID))
        db_connection.commit()

        return redirect("/Concerts")


# routes for ArtistPerformances page
@app.route("/ArtistPerformances", methods=["POST", "GET"])
def ArtistPerformances():
    # Separate out the request methods, in this case this is for a POST
    # insert an artist into the Concert_Artists table
    if request.method == "POST":
        # fire off if user presses the Add Artist Performance button
        if request.form.get("Add_ArtistPerformance"):
            # grab user form inputs
            concertID = request.form["concertID"]
            artistID = request.form["artistID"]
            query = "INSERT INTO Concert_Artists (concertID, artistID) VALUES (%s, %s)"
            # Update the database with new entry
            cur = db.execute_query(db_connection=db_connection, query=query, query_params=(concertID, artistID))
            db_connection.commit()

            # redirect back to ArtistPerformances page
            return redirect("/ArtistPerformances")

    # Grab ArtistPerformances data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the Artist Performances in the Concert_Artists table
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
def DeleteArtistPerformance(id):
    query = "DELETE FROM Concert_Artists WHERE concert_artistID = %s" % (id)
    cur = db.execute_query(db_connection=db_connection, query=query)
    db_connection.commit()

    return redirect('/ArtistPerformances')


# route for Venues page
@app.route("/Venues", methods=["POST", "GET"])
def Venues():
    # Separate out the request methods, in this case this is for a POST
    # insert a venue into the Venues entity
    if request.method == "POST":
        # fire off if user presses the Add Venue button
        if request.form.get("Add_Venue"):
            # grab user form inputs
            venue = request.form["venue"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"]
            capacity = request.form["capacity"]
            query = "INSERT INTO Venues(name, address, city, state, capacity) VALUES (%s, %s, %s, %s, %s);"
            # Update the database with new entry
            cur = db.execute_query(db_connection=db_connection, query=query, query_params=(venue, address, city, state, capacity))
            db_connection.commit()

            # redirect back to people page
            return redirect("/Venues")

    # Grab ArtistPerformances data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT venueID AS `ID`, name AS `Venue`, address AS `Address`, city AS `City`, state AS `State`, FORMAT(capacity, 'N0') AS `Capacity` FROM Venues"
        cur = db.execute_query(db_connection=db_connection, query=query)
        data = cur.fetchall()

        # render page passing our query data
        return render_template("Venues.j2", data=data)

# Venue table deletePerformance ID
@app.route('/DeleteVenue/<int:id>')
def delete_venues(id):
    query = "DELETE FROM Venues WHERE venueID = %s" % (id)
    cur = db.execute_query(db_connection=db_connection, query=query)
    db_connection.commit()

    return redirect('/Venues')


# routes for Ticketholders page
@app.route('/Ticketholders', methods=['GET', 'POST'])
def Ticketholders():
    if request.method == 'GET':
        query = ("SELECT ticketholderID AS `Ticketholder ID`, firstName AS `First Name`, "
        + "lastName AS `Last Name`, email AS `Email`, phone AS `Phone Number` "
        + "FROM Ticketholders ORDER BY ticketholderID ASC")
        cur = db.execute_query(db_connection=db_connection, query=query)
        data = cur.fetchall()

        return render_template("Ticketholders.j2", data=data)
    
    elif request.method == 'POST':
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        phone = request.form["phone"]

        query = "INSERT INTO Ticketholders(firstName, lastName, email, phone) VALUES (%s, %s, %s, %s)"
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(firstName, lastName, email, phone))
        db_connection.commit()

        return redirect('/Ticketholders')


# routes for Tickets page
@app.route('/Tickets', methods=['GET', 'POST'])
def Tickets():
    if request.method == 'GET':
        query1 = ("SELECT ticketID AS `Ticket ID`, Venues.name AS `Venue`, Concerts.date AS `Date`, "
            + "CONCAT(Ticketholders.firstName, Ticketholders.lastName) AS `Ticketholder Name`, "
            + "scanned AS `Scanned?`, (COUNT * FROM Tickets) AS `Tickets Sold` FROM Tickets "
            + "JOIN Concerts ON Tickets.concertID = Concerts.concertID "
            + "JOIN Venues ON Concerts.venueID = Venues.venueID "
            + "JOIN Ticketholders ON Tickets.ticketholderID = Ticketholders.ticketholderID")
        cur = db.execute_query(db_connection=db_connection, query=query1)
        data = cur.fetchall()

        query2 = ("SELECT concertID, date, Venues.name FROM Concerts JOIN Venues ON Concerts.venueID = Venues.venueID")
        cur = db.execute_query(db_connection=db_connection, query=query2)
        concerts = cur.fetchall()

        query3 = ("SELECT ticketholderID, CONCAT(firstName, lastName) AS `name` FROM Ticketholders")
        cur = db.execute_query(db_connection=db_connection, query=query3)
        ticketholders = cur.fetchall()

        query4 = ("SELECT COUNT(scanned) AS `Attendance` FROM Tickets WHERE scanned = 1")
        cur = db.execute_query(db_connection=db_connection, query=query4)
        attendance = cur.fetchall()

        return render_template("Tickets.j2", data=data, concerts=concerts, ticketholders=ticketholders, attendance=attendance)

    elif request.method == 'POST':
        concertID = request.form["concertID"]
        ticketholderID = request.form["ticketholderID"]
        scanned = request.form["scanned"]

        query = ("INSERT INTO Tickets(ticketholderID, concertID, scanned) VALUES (%s, %s, %s)")
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(ticketholderID, concertID, scanned))
        db_connection.commit()
        
        return redirect('/Tickets')


# Listener
if __name__ == "__main__":
    app.run(port=31669, debug=True)