from db_config import *

DB = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
SKIP_SECTIONS = 'Navigation', 'Project links'  # sections we decided to skip and not scarp information
PAGE = 'https://pypi.org/classifiers/'
CLASSIFIER_INDEX = 1
HOME_PAGE = "https://pypi.org"
START_PAGE = pypi_url = "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3"
NUMBER_OF_SEP_CHARS = 100  # When printing the info for a package - will use a separator char between each pack.
SNIPPET_PAGES = 5  # 20 packages per page so 50 pages is for scraping a 1000 packages.
PACKAGE_SEPARATORS_CHARS = 100  # Used to decide the length of a line that separates each package when printing