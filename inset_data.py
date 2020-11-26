from scrap_package_page import scrap_side_bars
from scrap_package_snippet import PackageSnippet, get_soup, get_n_pages_of_packages_snippets, get_package_details_url
from scrap_package_snippet import START_PAGE

# name = Column(String(128), nullable=False)
# version = Column(String(50), nullable=False)
# description = Column(String(255))
# package_license = Column(String(128))
# release_date = Column(DateTime)
# github_stars = Column(Integer)
# github_forks = Column(Integer)
# github_open_issues = Column(Integer)

# start_dict = {'name': None,
#               'version': None,
#               'description': None,
#               'package_license': None,
#               'release_date': None,
#               'github_stars': None,
#               'github_forks': None,
#               'github_open_issues': None}

# A named tuple class to hold the package snippet info.
# PackageSnippet = namedtuple('PackageSnippet',
#                             'name version link released description')


def get_package_data(data_dict: dict):
    start_dict = {'name': None,
                  'version': None,
                  'description': None,
                  'package_license': None,
                  'release_date': None,
                  'github_stars': None,
                  'github_forks': None,
                  'github_open_issues': None}

    package_snippet = data_dict.keys()[0]

    start_dict['name'] = package_snippet.name
    start_dict['version'] = package_snippet.version
    start_dict['release_date'] = package_snippet.released
    start_dict['description'] = package_snippet.description

    data = data_dict.values()

    # for key, value in data:
    #     if key not in ['stars', 'forks', 'open_issues']




