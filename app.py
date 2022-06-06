# Adapted from CS340 Flask Starter App

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

        query2 = ("SELECT venueID, name FROM Venues ORDER BY name")
        cur = db.execute_query(db_connection=db_connection, query=query2)
        venues = cur.fetchall()

        return render_template('Concerts.j2', data=data, venues=venues)
    
    elif request.method == 'POST':
        date = request.form["date"]
        venueID = request.form["venueID"]

        query = "INSERT INTO Concerts (date, venueID) VALUES (%s, %s)"
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(date, venueID))

        return redirect("/Concerts")

@app.route('/EditConcert/<int:id>', methods = ['GET', 'POST'])
def EditConcert(id):
    if request.method == 'GET':
        # Get concert info to display
        query1 = ("SELECT date AS `Date`, Venues.name AS `Venue`, concertID FROM Concerts "
        + "JOIN Venues ON Venues.venueID = Concerts.venueID "
        + "WHERE concertID = %s") % (id)
        cur = db.execute_query(db_connection=db_connection, query=query1)
        data = cur.fetchall()

        # Get venue info for drop down
        query2 = "SELECT venueID, name FROM Venues"
        cur = db.execute_query(db_connection=db_connection, query=query2)
        venues = cur.fetchall()

        return render_template('EditConcerts.j2', data=data, venues=venues)

    elif request.method == 'POST':
        # Get form inputs
        date = request.form['date']
        venueID = request.form['venueID']
        concertID = request.form['concertID']

        # Update the database
        query = "UPDATE Concerts SET date = %s, venueID = %s WHERE concertID = %s"
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(date, venueID, concertID))

        return redirect('/Concerts')

@app.route('/DeleteConcert/<int:id>')
def DeleteConcert(id):
    query = "DELETE FROM Concerts WHERE concertID = %s" % (id)
    db.execute_query(db_connection=db_connection, query=query)

    return redirect('/Concerts')


# route for ArtistPerformances page
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
            # redirect back to ArtistPerformances page
            return redirect("/ArtistPerformances")

    # Grab ArtistPerformances data so we send it to our template to display
    if request.method == "GET":
        if request.args.get("Search_ArtistPerformance"):
            print('search')
            # grab user form inputs
            artist = request.args["artist"]
            date = request.args["date"]
            venue = request.args["venue"]
            # concert = request.args["concert"]
            # mySQL query to grab search criteria for Artist Performances in the Concert_Artists table
            query = "SELECT concert_artistID AS `ID`, Artists.name AS `Artist`, Concerts.date AS Date, Venues.name AS `Venue` FROM Concert_Artists JOIN Artists ON Artists.artistID = Concert_Artists.artistID JOIN Concerts ON Concerts.concertID = Concert_Artists.concertID JOIN Venues ON Venues.venueID = Concerts.venueID WHERE Artists.name LIKE %s AND Concerts.date LIKE %s AND Venues.name LIKE %s"
            print(artist,date,venue)
            cur = db.execute_query(db_connection=db_connection, query=query, query_params=('%'+artist+'%', '%'+date+'%', '%'+venue+'%'))
            data = cur.fetchall()
            # render page passing our query data
            return render_template("ArtistPerformances.j2", data=data)
        elif not request.args.get("Search_ArtistPerformance"):
            # mySQL query to grab all the Artist Performances in the Concert_Artists table
            query = "SELECT concert_artistID AS `ID`, Artists.name AS `Artist`, Concerts.date AS Date, Venues.name AS `Venue` FROM Concert_Artists JOIN Artists ON Artists.artistID = Concert_Artists.artistID JOIN Concerts ON Concerts.concertID = Concert_Artists.concertID JOIN Venues ON Venues.venueID = Concerts.venueID ORDER BY concert_artistID"
            cur = db.execute_query(db_connection=db_connection, query=query)
            data = cur.fetchall()
            # mySQL query to grab artist data for our dropdown
            query2 = "SELECT artistID, name FROM Artists ORDER BY name"
            cur = db.execute_query(db_connection=db_connection, query=query2)
            artists = cur.fetchall()
            # Get concert info for drop down
            query3 = "SELECT concertID, date AS `date`, Venues.name AS `venue` FROM Concerts JOIN Venues ON Venues.venueID = Concerts.venueID  ORDER BY date"
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

        return redirect('/ArtistPerformances')

@app.route('/DeletePerformance/<int:id>')
def DeleteArtistPerformance(id):
    query = "DELETE FROM Concert_Artists WHERE concert_artistID = %s" % (id)
    db.execute_query(db_connection=db_connection, query=query)

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

            # redirect back to venues page
            return redirect("/Venues")

    # Grab Venues data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the venues in Venues
        query = "SELECT venueID AS `ID`, name AS `Venue`, address AS `Address`, city AS `City`, state AS `State`, FORMAT(capacity, 'N0') AS `Capacity` FROM Venues"
        cur = db.execute_query(db_connection=db_connection, query=query)
        data = cur.fetchall()

        # render page passing our query data
        return render_template("Venues.j2", data=data)

# Venue table entry deletion
@app.route('/DeleteVenue/<int:id>')
def delete_venues(id):
    query = "DELETE FROM Venues WHERE venueID = %s" % (id)
    db.execute_query(db_connection=db_connection, query=query)

    return redirect('/Venues')


# route for Artists page
@app.route("/Artists", methods=["POST", "GET"])
def Artists():
    # Separate out the request methods, in this case this is for a POST
    # insert an artist into the Artists entity
    if request.method == "POST":
        # fire off if user presses the Add Artist button
        if request.form.get("Add_Artist") and request.form["recordLabelID"] == "":
            # grab user form inputs
            artist = request.form["artist"]
            recordLabelID = request.form["recordLabelID"]
            query = "INSERT INTO Artists(name) VALUES (%s)"
            # Update the database with new entry
            db.execute_query(db_connection=db_connection, query=query, query_params=(artist,))
            # redirect back to artists page
            return redirect("/Artists")
        else:
            # grab user form inputs
            artist = request.form["artist"]
            recordLabelID = request.form["recordLabelID"]
            query = "INSERT INTO Artists(name, recordLabelID) VALUES (%s, %s)"
            # Update the database with new entry
            db.execute_query(db_connection=db_connection, query=query, query_params=(artist, recordLabelID))
            # redirect back to artists page
            return redirect("/Artists")

    # Grab Artists data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the artists in Artists
        query = "SELECT artistID AS `ID`, Artists.name as Artist, `Record Labels`.name AS `Record Label` FROM Artists LEFT JOIN `Record Labels` ON `Record Labels`.recordLabelID = Artists.recordLabelID ORDER BY artistID"
        cur = db.execute_query(db_connection=db_connection, query=query)
        data = cur.fetchall()

        # mySQL query to grab record labels data for our dropdown
        query2 = "SELECT recordLabelID, name FROM `Record Labels` ORDER BY name"
        cur = db.execute_query(db_connection=db_connection, query=query2)
        recordlabels = cur.fetchall()

        # render page passing our query data
        return render_template("Artists.j2", data=data, RecordLabels=recordlabels)

# Artist table entry deletion
@app.route('/DeleteArtist/<int:id>')
def delete_artists(id):
    query = "DELETE FROM Artists WHERE artistID = %s" % (id)
    db.execute_query(db_connection=db_connection, query=query)

    return redirect('/Artists')


# route for RecordLabels page
@app.route("/RecordLabels", methods=["POST", "GET"])
def RecordLabels():
    # Separate out the request methods, in this case this is for a POST
    # insert an record label into the Record Labels entity
    if request.method == "POST":
        # fire off if user presses the Add Record Label button
        if request.form.get("Add_RecordLabel"):
            # grab user form inputs
            recordlabel = request.form["recordlabel"]
            query = "INSERT INTO `Record Labels`(name) VALUES (%s);"
            # Update the database with new entry
            db.execute_query(db_connection=db_connection, query=query, query_params=(recordlabel,))
 
            # redirect back to Record Labels page
            return redirect("/RecordLabels")

    # Grab Record Labels data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the record labels in Record Labels
        query = "SELECT recordLabelID AS 'ID', name AS 'Record Label' FROM `Record Labels`"
        cur = db.execute_query(db_connection=db_connection, query=query)
        data = cur.fetchall()

        # render page passing our query data
        return render_template("RecordLabels.j2", data=data)

# Record Labels table entry deletion
@app.route('/DeleteRecordLabel/<int:id>')
def delete_recordlabels(id):
    query = "DELETE FROM `Record Labels` WHERE recordLabelID = %s" % (id)
    db.execute_query(db_connection=db_connection, query=query)

    return redirect('/RecordLabels')


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


        return redirect('/Ticketholders')

@app.route('/EditTicketholder/<int:id>', methods = ['GET', 'POST'])
def EditTicketholder(id):
    if request.method == 'GET':
        query = ("SELECT ticketholderID, firstName AS `First Name`, lastName AS `Last Name`, email AS `Email`, phone AS `Phone` "
        + "FROM Ticketholders WHERE ticketholderID = %s") % (id)
        cur = db.execute_query(db_connection=db_connection, query=query)
        data = cur.fetchall()

        return render_template('EditTicketholders.j2', data=data)

    elif request.method == 'POST':
        # Get form inputs
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']
        ticketholderID = request.form['ticketholderID']

        # Update the database
        query = "UPDATE Ticketholders SET firstName = %s, lastName = %s, email = %s, phone = %s WHERE ticketholderID = %s"
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(firstName, lastName, email, phone, ticketholderID))

        return redirect('/Ticketholders')

@app.route('/DeleteTicketholder/<int:id>')
def DeleteTicketholder(id):
    query = "DELETE FROM Ticketholders WHERE ticketholderID = %s" % (id)
    db.execute_query(db_connection=db_connection, query=query)

    return redirect('/Ticketholders')


# routes for Tickets page
@app.route('/Tickets', methods=['GET', 'POST'])
def Tickets():
    if request.method == 'GET':
        query1 = ("SELECT ticketID AS `Ticket ID`, Concerts.date AS `Date`,Venues.name AS `Venue`, "
            + "CONCAT(Ticketholders.firstName, ' ', Ticketholders.lastName) AS `Ticketholder Name`, "
            + "scanned AS `Scanned?` FROM Tickets "
            + "JOIN Concerts ON Tickets.concertID = Concerts.concertID "
            + "JOIN Venues ON Concerts.venueID = Venues.venueID "
            + "JOIN Ticketholders ON Tickets.ticketholderID = Ticketholders.ticketholderID "
            + "ORDER BY Date ASC")
        cur = db.execute_query(db_connection=db_connection, query=query1)
        data = cur.fetchall()

        query2 = ("SELECT concertID, date, Venues.name AS `Venue` FROM Concerts JOIN Venues ON Concerts.venueID = Venues.venueID ORDER BY date")
        cur = db.execute_query(db_connection=db_connection, query=query2)
        concerts = cur.fetchall()

        query3 = ("SELECT ticketholderID, CONCAT(firstName, ' ', lastName) AS `name` FROM Ticketholders ORDER BY firstName")
        cur = db.execute_query(db_connection=db_connection, query=query3)
        ticketholders = cur.fetchall()

        query4 = ("SELECT COUNT(*) AS `Tickets Sold`, COUNT(IF(scanned=1,1,null)) AS `Attendance`, " 
            + "CONCAT(Venues.name, ', ', Concerts.date) AS `Concert` FROM Tickets "
            + "JOIN Concerts ON Tickets.concertID = Concerts.concertID "
            + "JOIN Venues ON Concerts.venueID = Venues.venueID GROUP BY Tickets.concertID")
        cur = db.execute_query(db_connection=db_connection, query=query4)
        ticketSales = cur.fetchall()

        return render_template("Tickets.j2", data=data, concerts=concerts, ticketholders=ticketholders, ticketSales=ticketSales)

    elif request.method == 'POST':
        concertID = request.form["concertID"]
        ticketholderID = request.form["ticketholderID"]
        scanned = request.form["scanned"]

        query = ("INSERT INTO Tickets(ticketholderID, concertID, scanned) VALUES (%s, %s, %s)")
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(ticketholderID, concertID, scanned))

        return redirect('/Tickets')

@app.route('/EditTicket/<int:id>', methods = ['GET', 'POST'])
def EditTicket(id):
    if request.method == 'GET':
        # Get performance info to display
        query1 = ("SELECT CONCAT(Ticketholders.firstName, ' ', Ticketholders.lastName) AS `Ticketholder`, "
            + "CONCAT(Venues.name, ', ', Concerts.date) AS `Concert`, scanned AS `Scanned?`, ticketID, Ticketholders.ticketholderID, Concerts.concertID "
            + "FROM Tickets "
            + "JOIN Concerts ON Tickets.concertID = Concerts.concertID "
            + "JOIN Venues ON Venues.venueID = Concerts.venueID "
            + "JOIN Ticketholders ON Tickets.ticketholderID = Ticketholders.ticketholderID "
            + "WHERE ticketID = %s") % (id)
        cur = db.execute_query(db_connection=db_connection, query=query1)
        data = cur.fetchall()

        # Get artist info for drop down
        query2 = ("SELECT ticketholderID, CONCAT(firstName, ' ', lastName) AS `name` FROM Ticketholders")
        cur = db.execute_query(db_connection=db_connection, query=query2)
        ticketholders = cur.fetchall()

        # Get concert info for drop down
        query3 = "SELECT concertID, date AS `date`, Venues.name AS `venue` FROM Concerts JOIN Venues ON Venues.venueID = Concerts.venueID ORDER BY DATE"
        cur = db.execute_query(db_connection=db_connection, query=query3)
        concerts = cur.fetchall()

        return render_template('EditTickets.j2', data=data, ticketholders=ticketholders, concerts=concerts)

    elif request.method == 'POST':
        # Get form inputs
        ticketID = request.form['ticketID']
        concertID = request.form['concertID']
        ticketholderID = request.form['ticketholderID']
        scanned = request.form['scanned']

        # Update the database
        query = "UPDATE Tickets SET concertID = %s, ticketholderID = %s, scanned = %s WHERE ticketID = %s"
        cur = db.execute_query(db_connection=db_connection, query=query, query_params=(concertID, ticketholderID, scanned, ticketID))

        return redirect('/Tickets')

@app.route('/DeleteTicket/<int:id>')
def DeleteTicket(id):
    query = "DELETE FROM Tickets WHERE ticketID = %s" % (id)
    db.execute_query(db_connection=db_connection, query=query)

    return redirect('/Tickets')


# Listener
if __name__ == "__main__":
    app.run(port=12702, debug=True)
