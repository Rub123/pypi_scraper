
# DB = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
SKIP_SECTIONS = 'Navigation', 'Project links'  # sections we decided to skip and not scarp information
PAGE = 'https://pypi.org/classifiers/'
CLASSIFIER_INDEX = 1
HOME_PAGE = "https://pypi.org"
START_PAGE = pypi_url = "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3"
NUMBER_OF_SEP_CHARS = 100  # When printing the info for a package - will use a separator char between each pack.
SNIPPET_PAGES = 5  # 20 packages per page so 50 pages is for scraping a 1000 packages.
PACKAGE_SEPARATORS_CHARS = 100  # Used to decide the length of a line that separates each package when printing
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
TIMEOUT = 10


START_DIC = {
    "programming": {
        # 1: python
        # 2: SQL
        # 3: C++
        "1": "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3",
        "2": "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+SQL",
        "3": "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+C%2B%2B"
    },
    "op": {
        # 1- MacOS
        # 2- Microsoft
        # 3- unix
        "1": "https://pypi.org/search/?q=&o=-created&c=Operating+System+%3A%3A+MacOS",
        "2": "https://pypi.org/search/?q=&o=-created&c=Operating+System+%3A%3A+Microsoft",
        "3": "https://pypi.org/search/?q=&o=-created&c=Operating+System+%3A%3A+Unix",
    },
    "framework": {
        # 1-django
        # 2-plone
        "1": "https://pypi.org/search/?q=&o=-created&c=Framework+%3A%3A+Django",
        "2": "https://pypi.org/search/?q=&o=-created&c=Framework+%3A%3A+Plone",
    },
    "topic": {
        # 1-Communications
        # 2-Database
        # 3-Games/Entertainment
        # 4-Internet
        # 5-Scientific/Engineering
        "1": "https://pypi.org/search/?q=&o=-created&c=Topic+%3A%3A+Communications",
        "2": "https://pypi.org/search/?q=&o=-created&c=Topic+%3A%3A+Database",
        "3": "https://pypi.org/search/?q=&o=-created&c=Topic+%3A%3A+Games%2FEntertainment",
        "4": "https://pypi.org/search/?q=&o=-created&c=Topic+%3A%3A+Internet",
        "5": "https://pypi.org/search/?q=&o=-created&c=Topic+%3A%3A+Scientific%2FEngineering"
    }
}
