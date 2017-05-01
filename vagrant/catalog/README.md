ITEM CATALOG UDACITY PROJECT
=======================================

Code for item catalog udacity project

### Technologies Used

* [vagrant] - enables users to create and configure lightweight, reproducible, and portable development environments
* [VirutalBox] - create virtual machines
* [python] - Programming Language
* [SQLite] - DBMS
* [SQLAlchemy] - ORM
* [HTML & CSS] - for markup & styles
* [Javascript & jQuery] - for scripting & ajax requests


### Usage (on Ubuntu, or other GNU/Linux based Operating Systems)


* make sure virtualbox and vagrant are installed on your machine
* enter "git clone https://github.com/brucekaushik/ItemCatalog.git [path]/[directory-name]" to clone this project
* cd [cloned directory path]/vagrant
* enter "vagrant up" in the terminal (this sets up the vm, wait for the vm to be downloaded and setup for you)
* enter "vagrant ssh" in the terminal (ssh into the machine)
* enter "cd /vagrant/catalog" in the terminal (the project files are located here)
* enter "python dbsetup.py" in the terminal (this will setup the sqlite database, you can see itemcatalog.db)
* enter "python populatedb.py" in the terminal (this will populate the database with initial set of records, this is MANDATORY, otherwise it will lead to errors)
* enter "pip install requests" in the terminal (this will install requests library)
* enter "python app.py" (the app should start after issuing this command)
* browse to "http://localhost:5000" to see the catalog app!

### NOTE:

* There is no way to add catalog id to the database using the gui user interface, therefore it must be done using populatedb.py file. Also, note that we are not doing any error check if the catalog id exits in the project files because of this reason.

* You need to install requests library, as its not included in the vm by default.