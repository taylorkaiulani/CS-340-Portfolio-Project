-- Group 20 - Concerts Unlimited
-- Data Manipulation Queries

-- USE `concertsDB`; # Commented out to avoid error

-- -----------------------------------------------------
-- Dropdowns
-- -----------------------------------------------------
-- Artist ID dropdown
SELECT artistID FROM Artists;

-- Concert ID dropdown
SELECT concertID FROM Concerts;

-- Vanue ID dropdown
SELECT venueID FROM Venues;

-- Ticketholder ID dropdown
SELECT ticketholderID FROM Ticketholders;

-- Record label dropdown (with NULL)
(SELECT name FROM Artists
ORDER BY name ASC) 
UNION ALL 
SELECT NULL;

-- Venue dropdown
SELECT name FROM Venues;

-- -----------------------------------------------------
-- Artist page
-- -----------------------------------------------------
-- Get list of artists
SELECT artistID AS `ID`, Artists.name as Artist,  `Record Labels`.name AS `Record Label` FROM Artists
INNER JOIN `Record Labels` ON `Record Labels`.recordLabelID = Artists.recordLabelID;

-- Add artist
INSERT INTO Artists (`Artists`.name, recordLabelID) 
VALUES (:artistIName_input, :recordLabelID_input);

-- Update artist
UPDATE Artists
SET `Artists`.name = :artistIName_input, recordLabelID= :recordLabelID_input
WHERE artistID = :artistID_input;

-- Delete artist
DELETE FROM Artists 
WHERE artistID = :artistID_input;

-- -----------------------------------------------------
-- Concert_Artists page
-- -----------------------------------------------------
-- Get list of Concert_Artists
SELECT concert_artistID AS `Concert_Artist ID`, Concert_Artists.concertID AS `Concert ID`, 
Concerts.date AS Date, Concert_Artists.artistID AS `Artist ID`, Artists.name AS `Artist` FROM Concert_Artists
JOIN Artists ON Artists.artistID = Concert_Artists.artistID
JOIN Concerts ON Concerts.concertID = Concert_Artists.concertID;

-- Add Concert_Artist
INSERT INTO Concert_Artists (concertID, artistID) 
VALUES (:concertID_input, :artistID_input);

-- Update Concert_Artist
UPDATE Concert_Artists 
SET concertID = :concertID_input, artistID = :artistID_input
WHERE concert_artistID = :concert_artistID_input;

-- Delete Concert_Artist
DELETE FROM Concert_Artists 
WHERE concert_artistID = :concert_artistID_input;

-- -----------------------------------------------------
-- Concerts page
-- -----------------------------------------------------
-- Get list of concerts
SELECT Concerts.concertID AS `ID`, date AS `Date`, Venues.name AS `Venue` FROM Concerts
JOIN Venues ON Venues.venueID = Concerts.venueID;

-- Add concert
INSERT INTO Concerts (date, venueID) 
VALUES (:date_input, :venueID_input);

-- Update concert
UPDATE Concerts  
SET date = :date_input, venueID = :venueID_input
WHERE concertID = :concertID_input;

-- Delete concert
DELETE FROM Concerts 
WHERE concertID = :concertID_input;

-- -----------------------------------------------------
-- Record Labels page
-- -----------------------------------------------------
-- Get list of record labels
SELECT recordLabelID AS 'ID', name AS 'Record Label'  FROM `Record Labels`;

-- Add a record label
INSERT INTO `Record Labels`(name) 
VALUES (:recordLabelName_input);

-- Update record label
UPDATE  `Record Labels`
SET `Record Labels`.name = :recordLabelName_input
WHERE recordLabelID = :recordLabelID_input;

-- Delete  record label
DELETE FROM `Record Labels` 
WHERE recordLabelID = :recordLabelID_input;

-- -----------------------------------------------------
-- Ticketholders page
-- -----------------------------------------------------
-- Get list of venues
SELECT ticketholderID AS `ID`, firstName AS `First Name`, lastName AS `Last Name`, email AS `Email`, 
phone AS `Phone` FROM Ticketholders;

-- Add venue
INSERT INTO Ticketholders(firstName, lastName, email, phone) 
VALUES (:firstName_input, :lastName_input, :email_input, :phone_input);

-- Update venue
UPDATE  Ticketholders
SET firstName = :firstName_input, lastName = :lastName_input, email = :email_input, phone = :phone_input
WHERE ticketholderID = :ticketholderID_input;

-- Delete venue
DELETE FROM Ticketholders
WHERE ticketholderID = :ticketholderID_input;

-- -----------------------------------------------------
-- Tickets page
-- -----------------------------------------------------
-- Get list of tickets
SELECT ticketID AS `Ticket ID`, email AS `Ticketholder Email`, Concerts.date AS `Date`, scanned as `Scanned` FROM Tickets
JOIN Ticketholders ON Ticketholders.ticketholderID = Tickets.ticketholderID
JOIN Concerts ON Concerts.concertID = Tickets.concertID;

-- Add ticket
INSERT INTO Tickets(ticketholderID, concertID, scanned) 
VALUES (:ticketholderID_input, :concertID_input, scanned_input);

-- Update ticket
UPDATE  Tickets
SET :ticketholderID = :ticketholderID_input, concertID = :concertID_input, scanned = :scanned_input
WHERE ticketID = :ticketID_input;

-- Delete ticket
DELETE FROM Tickets 
WHERE ticketID = :ticketID_input;

-- -----------------------------------------------------
-- Venues page
-- -----------------------------------------------------
-- Get list of venues
SELECT venueID AS `ID`, name AS `Venue`, address AS `Address`, city AS `City`, state AS `State`, capacity AS `Capacity` FROM Venues;

-- Add venue
INSERT INTO Venues(name, address, city, state, capacity) 
VALUES (:venueName_input, :address_input, :city_input, :state_input, :capacity_input);

-- Update venue
UPDATE  Venues
SET name = :recordLabelName_input, address = :address_input, city = :city_input, state = :state_input, capacity = :capacity_input
WHERE venueID = :venueID_input;

-- Delete venue
DELETE FROM Venues 
WHERE venueID = :venueID_input;
