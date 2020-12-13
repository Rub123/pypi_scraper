# pypi_scraper

pypi_scraper can be used to scrape information of python packages from https://pypi.org/

## Description

This script can be used to scrape information from pypi website.
The information types available on this website are very vast and every package has 
different combinations of information types that are available. 
An example result for one package:

    Package: sphinxcontrib-towncrier, Version 0.1.0a1:

        Short description: An RST directive for injecting a Towncrier-generated changelog draft containing fragments 
        for the unreleased (next) project version
        
        More Info:
        stars:8
        forks:4
        open_issues:3
        author:[('Sviatoslav Sydorenko', 'mailto:wk+pypi/sphinxcontrib-towncrier@sydorenko.org.ua')]
        maintainers:[('slsh1o', '/user/slsh1o/'), ('webknjaz', '/user/webknjaz/')]
        development_status:['3 - Alpha']
        framework:['Sphinx', 'Sphinx :: Extension']
        intended_audience:['Developers']
        license:['OSI Approved :: BSD License']
        operating_system:['OS Independent']
        programming_language:['Python :: 3.6', 'Python :: 3.7', 'Python :: 3.8', 'Python :: 3.9']
        topic:['Documentation :: Sphinx', 'Software Development :: Documentation', 'System :: Software Distribution',
        'Utilities']

## Installations

All required installation can be found in requirements.txt
to install - 

    pip install -r requirements.txt

## Scripts and config files

### db

This folder contains all scripts related to updating and creating the db.
In order for the scripts in this folder to run you need to set up your SQL information in db_config
(see more info below), and create a git ignor py file named
private_db.py
that has one variable - your password in this form 
PASSWORD = 'your_password'

#### create_db.py
This script has to be used separately to create a local instance of the db on your own computer.

#### db_functions.py
this script has all the functions used to update your db with new data if this option was selected 
when runnin the CLI

### scraper

contains all scripts related to scrapping data from the website.
In order for the scripts in this folder to run you need to set up your GIT API token
in a git ignore py file named
private_passwords.py
that has one variable - your password in this form 
GITHUB_TOKEN = 'your_token'

#### scrap_package_snippet.py

This script defines the functions that are used to scarp information from the search page of the website.
Each page holds info of 20 packages that includes - Name, version, link to detailed page of the package,
release date, short description of the package

#### scarp_package_page.py and scarp_package.py

this script defines the functions that are used in order to scarp information from the detailed pages of each package.
The information is taken from the side bar of the page that includes different combinations of optional information
such as:
'Navigation', 'Project links', 'Statistics', 'Meta', 'Maintainers' and 'Classifiers'
'Navigation', 'Project links' are ignored in this version as well as the full description that can be found in the
main area of the page.

#### pypi_classifiers.py
This script is used to scrape all the different types of information that can be found in the Classifiers section
of the side bar of a package page.

#### github_api.py
This scripts enriches the data from information gathered from Github API

### main folder

#### cli_pypi.py
This is the main script for the user. It is a command line tool that helps the user decide what data 
he wants to scrap and whether to print it or create a local db.

command line arguments 

 -t --topic

scrape data by topic. Can choose one topic at a time from: 
1. Communications 
2. Database
3. Games/Entertainment
4. Internet
5. Scientific/Engineering

-o --op

scrape data by operating system Can choose one OP at a time from:
1. MacOS
2. Windows
3. unix

-f --framework

scrape data by framework system Can choose one framework at a time from:
1. django
2. plone

-p --programming

scrape data by programming language/ Can choose one programming language at a time from:
1. python (default)
2. SQL
3. C++

-n --number

how many pages to scrape from, Defualt is 5 and can be change from config file.

-s --save

Default False, if chosen will create a local DB with the scraped data.

###config.ini

Most of the constants used in this script

[logger] <br>
constant related to the logging script

[classifiers]<br>
PAGE : link to pypi page where all the classifier information is help
CLASSIFIER_INDEX : Index to get a specific part of a split result of classifiers data 

[pypi]<br>
HOME_PAGE : link to pypi homepage
START_PAGE : Default value to start scraping from if no other value was given.

[requests]<br>
headers_key<br>
headers_val<br>
timeout<br>

First 2 constants are used to create a dict
all are used in order to scrap datawith less problems.
Make a request with a user agent fakes a browser visit to a particular webpage, timeout makes delays 
between actions.

[timeout]<br>
n_tries<br>
sleep<br>

Used in order to deal with timeout errors and retrial to scrap the data.
You can change this to have more trials if you have this issues

[scraper]<br>
SKIP_SECTIONS : sections from side bar we decided to skip and not take information from. 
Do not change without changing the code as it will fail.
Default value to start scraping from if no other value was given.
SNIPPET_PAGES : Default number of pages to scrap from, if no -n was given to the CLI. 
There are 20 packages per page so 5 pages is for scraping a 100 packages. 

### db_config.ini

the users personal info to create SQL db. Has default values. If you have different values this
should be changed to allow the script to create the DB. You can also name the DB here as DB_NAME.

DB_USER = 'root'<br>
DB_SERVER = 'localhost'<br>
DB_NAME = 'pypi'<br>

### cli_config.ini

this file has values used in cli_pypi. The reason they are in a different file was it was easier to implement it 
this way.
This file mainly constants all the start pages available to scrap from depending on the options chosen
in the CLI command. <br>
and also 2 more constants 

SNIPPET_PAGES : Default number of pages to scrap from, if no -n was given to the CLI. 
There are 20 packages per page so 5 pages is for scraping a 100 packages. 
PACKAGE_SEPARATORS_CHARS : When printing the info will use n times separator char between 
each pack.

#### orchestrator.py
a file that helps us connect between all the different functions in the different scripts.


## Authors and acknowledgment

Adam Rubins and Or Granot as part of ITC data science course under the guidance of Yoni Mayzel

## support

Please reach us via email<br>
adamrubins@gmail.com<br>
orkin2@gmail.com