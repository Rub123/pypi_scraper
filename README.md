# pypi_scraper

pypi_scraper can be used to scrape information of python packages from https://pypi.org/

## Description

This script can be used to scrape information from pypi website.
The information types available on this website are very vast and every package has different combinations of information
types that are available. 
An example result for one package:

    Package: sphinxcontrib-towncrier, Version 0.1.0a1:

        Short description: An RST directive for injecting a Towncrier-generated changelog draft containing fragments for the unreleased (next) project version
        
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
        topic:['Documentation :: Sphinx', 'Software Development :: Documentation', 'System :: Software Distribution', 'Utilities']

## Installations

All required installation can be found in requirements.txt
to install - 

    pip install -r requirements.txt

## Scripts and constants

### scrap_package_snippet.py

This script defines the functions that are used to scarp information from the search page of the website.
Each page holds info of 20 packages that includes - Name, version, link to detailed page of the package,
release date, short description of the package

HOME_PAGE -
Do not change this as this script is not compatible with other websites

START_PAGE -
In this version we take 
https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3

This page orders the results by last updated and takes only results that are compatible with python 3.
You can take any other order / filters you want to get your desired result.

NUMBER_OF_SEP_CHARS -
When printing the information directly from this script (not from print_data), each package information is 
separated by a line of "-" this constant defines the number of dash lines used to separate each package information.

### scarp_package_page

this script defines the functions that are used in order to scarp information from the detailed pages of each package.
The information is taken from the side bar of the page that includes different combinations of optional information
such as:
'Navigation', 'Project links', 'Statistics', 'Meta', 'Maintainers' and 'Classifiers'
'Navigation', 'Project links' are ignored in this version as well as the full description that can be found in the
main area of the page.


SKIP_SECTIONS -
The script scarp information from the side bar of each package page.
The script ignores the sections defined in this constant. Do not remove  'Navigation' or 'Project links'
as the script is not compatible with scarping this information. If you wish to ignore other sections from the side bar
such as 'Statistics', 'Meta', 'Maintainers', 'Classifiers' add them to this constant


### pypi_classifiers

This script is used to scrap all the different types of information that can be found in the Classifiers section
of the side bar of a package page.
Do not change any of the constants in this page.

PAGE
link to the classifiers page of pypi 

CLASSIFIER_INDEX
index to where information of the classifiers can be found after splitting the data string

### print_data.py
This is the main script for the user. It is used to print the data and also optional to save it to a text file.
In order to save to a text file please define a path for the text file to be saved.
in future versions we will fix this to be more user friendly :)

SNIPPET_PAGES - amount of pages to scrape from the search page. Each page has 20 packages. Change this constant
to get more / less results
PACKAGE_SEPARATORS_CHARS - When printing the information dor saving to a text file, each package information is 
separated by a line of "-" this constant defines the number of dash lines used to separate each package information.


## Authors and acknowledgment

Adam Rubins and Or Granot as part of ITC data science course under the guidance of Yoni Mayzel

## support

Please reach us via email
adamrubins@gmail.com
orkin2@gmail.com