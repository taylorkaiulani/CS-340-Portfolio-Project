# CS340 Portfolio Project

This website was created by Taylor Homan and Derrick Priebe as a final project for OSU's CS340 - Introduction to Databases. The assignment was to build an administrator website for a theoretical company, using a relational database to store company metrics and operational data. The website was created using Flask, and the database was created with MySQL/MariaDB.

To run the site locally, you must:

- Create a new database (the site's original DB was hosted on school servers and is no longer available)
- Initialize the tables and sample data using the DDL.sql file included in this repository
- Clone the repository to your machine
- In your local repository, create a .env file with the following variables:
  - 340DBHOST: This is the host name for your database
  - 340DBUSER: This is the username associated with your database
  - 340DBPW: This is the password for your database credentials
  - 340DB: This is your database name
- Make sure you're in the same directory as your repository
- Run the command:
```
python3 app.py
```

Excerpts of the final write up for the project, including the database schema and screenshots of the site's UI, are included below.

## Project Report
### Overview
Concerts Unlimited is a company that manages concert events across the United States. The company operates over 100 events each year and grosses around $50M. Featured artists vary from up-and-coming indie musicians to international sensations, drawing a wide variety of fans across the country. The company needs to leverage a comprehensive database to help with the basic logistics of creating and managing concert events throughout the event lifecycle to help in preparation, execution, and retrospective analysis.

This database will track the following:
- Organizational data
  - Event dates & locations
  - Artists
  - Venues
- Event attendance
- Customer information
  - Name and contact information
  - Purchased tickets
  - To be used for promotional purposes in the future

The following assumptions are made in this draft for simplicity:
- Ticketholder and concert relationship (reflected in Tickets table) represents an individual ticket purchase
- One ticketholder is associated with every individual concert ticket

### Database Schema
![ER Diagram - Draft 06](https://user-images.githubusercontent.com/86279867/174934714-c69874bd-238e-4ea7-bae5-eafa79024bef.png)

### UI Screen Captures
#### Homepage
![Homepage](https://user-images.githubusercontent.com/86279867/174935587-7dd7579a-94bc-44fc-a6a7-0e66b62a16b6.png)
Index page for the rest of the site; nav functionality only.

#### Concerts Page
![Concerts](https://user-images.githubusercontent.com/86279867/174935640-c8535549-2922-466f-8582-4915af898b1a.png)
Represents the Concerts entity. Functionality: Create, Read, Update, Delete

#### Artists Page
![Artists](https://user-images.githubusercontent.com/86279867/174935669-6a9f1498-0931-4d20-b94c-7335233cc59d.png)
Represents the Artists entity. Functionality: Create, Read, Delete

#### Artist Performances Page
![Artist Performances](https://user-images.githubusercontent.com/86279867/174935735-986c1b3d-d3c4-467e-a7bd-e13f15d02190.png)
Represents the intermediary table between Concerts and Artists. Functionality: Create, Read, Update, Delete

#### Venues Page
![Venues](https://user-images.githubusercontent.com/86279867/174935769-63b9f272-60a9-4fec-a63c-775763258ea7.png)
Represents the Venues entity. Functionality: Create, Read, Delete

#### Record Labels Page
![Record Labels](https://user-images.githubusercontent.com/86279867/174935800-15c0905d-7b1d-4899-a60c-d29820fc314b.png)
Represents the Record Labels entity. Functionality: Create, Read, Delete

#### Ticketholders Page
![Ticketholders](https://user-images.githubusercontent.com/86279867/174935839-c96daad9-d2db-41ca-82c5-7a012a42f51a.png)
Represents the Ticketholders entity. Functionality: Create, Read, Update, Delete

#### Tickets Page
![Tickets](https://user-images.githubusercontent.com/86279867/174935862-4f2d7f8d-6d2b-4b20-8463-485983ed9c05.png)
Represents the intermediary table between Concerts and Ticketholders. Functionality: Create, Read, Update, Delete
