# use-OpenFoodFacts

This program was created for the company Pure Beurre to perform a food search in the OpenFoodFacts database to find an equivalent.

## Start guide

### Dependencies

- [Python 3.5 or more](https://www.python.org) is required.
- [PostGreSQL](https://www.postgresql.org/download/)

### Installation instructions

- install Python 3.x
- install PostgreSQL

Create a database and a proprietary user account for this database.

Collect the use-OpenFoodFacts repo and install the dependencies as below:

    $ git clone https://github.com/Nels885/use-OpenFootFacts.git
    $ cd use-OpenFoodFacts
    $ pip3 install -r requirements.txt


Then run the python script below to retrieve the OpenFoodFacts data for embedding in the database.

    $ python3 update_db.py

![alt text](Pictures/update_db_config.png)

At the first launch it is necessary to indicate the information for the connection to the database as below.

- database name
- user
- password
- used port
- address database

Then you will find yourself on the menu below, if you do not make any mistake in the settings otherwise the program will ask you to start again.

![alt text](Pictures/update_db_menu.png)





## How to use the program

Run the program in the terminal.

    $ python3 purebeurre_client.py

![alt text](Pictures/purebeurre_client_menu.png)

This one will ask you two different questions in French which are:

    1 - Quel aliment souhaitez-vous remplacer ? 
    2 - Retrouver mes aliments substitués.

- Select one with the numeric keypad and confirm with the **enter** key.
- Then it will offer you several choices of categories, select in one thanks to the corresponding numeric key and validate.
- You will then have a list of foods that matches the categories, select as before.
- It will offer you a substitute with different information such as the store or buy it.

The program also allows you to save the result in the database.

