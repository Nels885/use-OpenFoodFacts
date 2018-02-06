# use-OpenFootFacts

This program was created for the company Pure Beurre to perform a food search in the Open Food Facts database to find an equivalent.

## Start guide

### Dependencies

* [Python 3.5 or more](https://www.python.org) is required.
* [PostGreSQL](https://www.postgresql.org/download/)

### Installation instructions

* install Python 3.x
* install PostgreSQL


    $ git clone https://github.com/Nels885/use-OpenFootFacts.git
    $ cd use-OpenFoodFacts


Create the database with the script found in the repo

    script_create_DB.sql
    
Then run the python script below to retrieve the OpenFoodFacts data for embedding in the database.

    $ python3 script.py

## How to use the program

Run the program in the terminal.

This one will ask you two different questions in French which are:

    1 - Quel aliment souhaitez-vous remplacer ? 
    2 - Retrouver mes aliments substitués.

* Select one with the numeric keypad and confirm with the "enter" key.

* Then it will offer you several choices of categories, select in one thanks to the corresponding numeric key and validate.

* You will then have a list of foods that matches the categories, select as before.

* It will offer you a substitute with different information such as the store or buy it.

The program also allows you to save the result in the database.

