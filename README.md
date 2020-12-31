# pypi_scraper

pypi_scraper can be used to scrape information of python packages from https://pypi.org/

## Description

This script can be used to scrape information from pypi website.
The information types available on this website are very vast and every package has different combinations 
of information types that are available. 
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

## Scripts and constants

### scrap_package_snippet.py

This script defines the functions that are used to scarp information from the search page of the website.
Each page holds info of 20 packages that includes - Name, version, link to detailed page of the package,
release date, short description of the package

### scarp_package_page

this script defines the functions that are used in order to scarp information from the detailed pages of each package.
The information is taken from the side bar of the page that includes different combinations of optional information
such as:
'Navigation', 'Project links', 'Statistics', 'Meta', 'Maintainers' and 'Classifiers'
'Navigation', 'Project links' are ignored in this version as well as the full description that can be found in the
main area of the page.

### pypi_classifiers

This script is used to scrape all the different types of information that can be found in the Classifiers section
of the side bar of a package page.

### cli_pypi.py
This is the main script for the user. It is a command line tool that helps the user decide what data he wants to scrape
and whether to print it or create a local db.

command line arguments 
-t --topic
scrape data by topic. Can choose one topic at a time from: 
1-Communications 
2-Database
3-Games/Entertainment
4-Internet
5-Scientific/Engineering

-o --op
scrape data by operating system Can choose one OP at a time from:
1- MacOS
2- Windows
3- unix

-f --framework
scrape data by framework system Can choose one framework at a time from:
1-django
2-plone

-p --programming
scrape data by programming language/ Can choose one programming language at a time from:
1-python (default)
2-SQL
3-C++

-n --number
how many pages to scrape from, Defualt is 5 and can be change from config file.

-s --save
Default False, if chosen will create a local DB with the scraped data.

###config.py

All the constants used in this script

DB = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
url to the sqlalchemy framework to connect to DB (info taken from db_config.py)

SKIP_SECTIONS = 'Navigation', 'Project links'  
sections from side bar we decided to skip and not take information from. Do not change without changing the code as it
will fail.

PAGE = 'https://pypi.org/classifiers/'
link to pypi page where all the classifier information is help

CLASSIFIER_INDEX = 1
Index to get a specific part of a split result of classifiers data 

HOME_PAGE = "https://pypi.org"
link to pypi homepage

NUMBER_OF_SEP_CHARS = 100  
When printing the info for a package in cli_pypi - will use n times separator char between 
each pack.

SNIPPET_PAGES = 5  
Default number of pages to scrape from. there are 20 packages per page so 5 pages is for 
scraping a 100 packages.

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
Chrome/70.0.3538.77 Safari/537.36"}
parameter sent to requests in order to scrape data from git with less problems.
Making a request with a user agent fakes a browser visit to a particular webpage.

TIMEOUT = 10
parameter sent to requests in order to scrape data from git with less problems

START_DIC
dic that is used to define the link to start scraping from depends on the user choice in the cli tool.
If you wish to change the url's make sure they are urls to a search page of pypi and not any other
page of the website.

###db_config.py
the users personal info to create SQL db. 
Should be changed to allow the script to create the DB.

DB_USER = 'root'
DB_PASSWORD = 'password'
DB_SERVER = 'localhost'
DB_NAME = 'pypi'

## insert_data.py
This file insert data to the db if the save option was chosen from the cli_pypi file.

### db_config.py
A separate script you should run it to set up all the tables and relations of the SQL db.


## Authors and acknowledgment

Adam Rubins and Or Granot as part of ITC data science course under the guidance of Yoni Mayzel

## support

Please reach us via email
adamrubins@gmail.com
orkin2@gmail.com