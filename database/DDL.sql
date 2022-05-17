-- CS340 - Group 20 - Concerts Unlimited
-- Data Definition Queries

-- -----------------------------------------------------
-- Schema
-- -----------------------------------------------------

-- CREATE SCHEMA IF NOT EXISTS `concertsDB` DEFAULT CHARACTER SET utf8 ; # Commented out to avoid error
-- USE `concertsDB`; # Commented out to avoid error

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Drop existing tables if exists
-- -----------------------------------------------------
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Ticketholders`;
DROP TABLE IF EXISTS `Venues`;
DROP TABLE IF EXISTS `Concerts`;
DROP TABLE IF EXISTS `Tickets`;
DROP TABLE IF EXISTS `Record Labels`;
DROP TABLE IF EXISTS `Artists`;
DROP TABLE IF EXISTS `Concert_Artists`;
SET FOREIGN_KEY_CHECKS = 1;

-- -----------------------------------------------------
-- Table `Ticketholders`
-- -----------------------------------------------------

CREATE TABLE `Ticketholders` (
  `ticketholderID` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(32) NOT NULL DEFAULT 0000000000,
  PRIMARY KEY (`ticketholderID`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Venues`
-- -----------------------------------------------------

CREATE TABLE `Venues` (
  `venueID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `state` CHAR(2) NOT NULL,
  `capacity` INT NOT NULL,
  PRIMARY KEY (`venueID`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Concerts`
-- -----------------------------------------------------

CREATE TABLE `Concerts` (
  `concertID` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `venueID` INT NOT NULL,
  PRIMARY KEY (`concertID`),
  FOREIGN KEY (`venueID`)
    REFERENCES `Venues` (`venueID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Tickets`
-- -----------------------------------------------------

CREATE TABLE `Tickets` (
  `ticketID` INT NOT NULL AUTO_INCREMENT,
  `ticketholderID` INT NOT NULL,
  `concertID` INT NOT NULL,
  `scanned` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`ticketID`),
  FOREIGN KEY (`ticketholderID`)
    REFERENCES `Ticketholders` (`ticketholderID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`concertID`)
    REFERENCES `Concerts` (`concertID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Record Labels`
-- -----------------------------------------------------

CREATE TABLE `Record Labels` (
  `recordLabelID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`recordLabelID`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Artists`
-- -----------------------------------------------------

CREATE TABLE `Artists` (
  `artistID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `recordLabelID` INT,
  PRIMARY KEY (`artistID`),
  FOREIGN KEY (`recordLabelID`)
    REFERENCES `Record Labels` (`recordLabelID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Concert_Artists`
-- -----------------------------------------------------

CREATE TABLE `Concert_Artists` (
  `concert_artistID` INT NOT NULL AUTO_INCREMENT,
  `concertID` INT NOT NULL,
  `artistID` INT NOT NULL,
  PRIMARY KEY (`concert_artistID`),
  FOREIGN KEY (`concertID`)
    REFERENCES `Concerts` (`concertID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`artistID`)
    REFERENCES `Artists` (`artistID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Insert Data into Table `Venues`
-- -----------------------------------------------------
INSERT into Venues(venueID, name, address, city, state, capacity)
VALUES(1, 'Red Rocks', '18300 W Alameda Pkwy', 'Morrison', 'CO', 9545),
(2, 'Ryman Auditorium', '116 5th Ave N', 'Nashville', 'TN', 2362),
(3, 'Stubbs', '801 Red River Street', 'Austin', 'TX', 2100),
(4, '930 Club', '815 V St NW', 'Washington', 'DC', 27500);

-- -----------------------------------------------------
-- Insert Data into Table `Concerts`
-- -----------------------------------------------------
INSERT into Concerts(concertID, date, venueID)
VALUES(1, '2023-04-08', 3),
(2, '2023-05-10', 2),
(3, '2023-06-24', 4),
(4, '2023-07-14', 1);

-- -----------------------------------------------------
-- Insert Data into Table `Record Labels`
-- -----------------------------------------------------
INSERT into `Record Labels`(recordLabelID, name)
VALUES(1, 'Foreign Family Collective'),
(2, 'Geffen Records'),
(3, 'Kidinakorner'),
(4, 'Interscope Records');

-- -----------------------------------------------------
-- Insert Data into Table `Artists`
-- -----------------------------------------------------
INSERT into Artists(artistID, name, recordLabelID)
VALUES(1, 'Billie Eilish', '4'),
(2, 'Olivia Rodrigo', '2'),
(3, 'Imagine Dragons', '3'),
(4, 'ODESZA', NULL);

-- -----------------------------------------------------
-- Insert Data into Table `Ticketholders`
-- -----------------------------------------------------
INSERT into Ticketholders(ticketholderID, firstName, lastName, email, phone)
VALUES(1, 'Kyle', 'Smith', 'ksmith@gmail.com', '454-333-6795'),
(2, 'Cara', 'Whenske', 'cwhenske@comcast.net', '678-439-8899'),
(3, 'Timothy', 'Rosale', 'timrosale@outlook.com', '243-444-9807'),
(4, 'Jennifer', 'Watkins', 'jenwatkins@gmail.com', '213-762-9850');

-- -----------------------------------------------------
-- Insert Data into Table `Tickets`
-- -----------------------------------------------------
INSERT into Tickets(ticketholderID, concertID)
VALUES(1, 4),
(4, 2),
(4, 3),
(2, 1);

-- -----------------------------------------------------
-- Insert Data into Table `Concert_Artists`
-- -----------------------------------------------------
INSERT into Concert_Artists(concertID, artistID)
VALUES(1, 3),
(2, 2),
(3, 4),
(4, 3);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;