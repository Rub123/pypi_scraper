import argparse
import configparser
from scraper.scrap_package_snippet import PackageSnippet
from scraper.scrap_package import get_data_dict
from orchestrator import insert_or_update_date, get_github_info
from pathlib import Path
import logging

logging.basicConfig(filename='pypi_scraper.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

config = configparser.ConfigParser(interpolation=None)
config.read(Path('cli_config.ini').absolute())

START_DICT = {}
for section in config.sections():
    START_DICT[section] = {}
    for option in config.options(section):
        START_DICT[section][option] = config.get(section, option)

SNIPPET_PAGES = int(START_DICT['other']['snippet_pages'])
PACKAGE_SEPARATORS_CHARS = int(START_DICT['other']['package_separators_chars'])


def print_data(start_link: str, n_pages: int = SNIPPET_PAGES, save_to_db=False) -> None:
    """ Prints the scraped data to the screen. If save_to_db will also save the information to database.
    :param start_link: link to start scraping from
    :param n_pages: int, number of pages
    :param save_to_db: An argument to save the scraped data to database.
    """

    for index, data in enumerate(get_data_dict(n_pages=n_pages, start_page=start_link), start=1):
        data = get_github_info(data)
        if save_to_db:
            insert_or_update_date(data)

        for pack_snip, pack_info in data.items():
            pack_snip: PackageSnippet
            msg = f"""Package: {str(pack_snip.name)}, Version {str(pack_snip.version)}:

    Short description: {str(pack_snip.description)}

    More Info:"""

            info_msg = '\n'.join('\t' + key + ':' + str(value) for key, value in pack_info.items())

            print(msg)
            print(info_msg)
            print('-' * PACKAGE_SEPARATORS_CHARS)

    print(f'Scraped {index} packages!')  # the last index form the enumerate loop above.


def main():
    """
    user chooses what to scrape from a list of options.
    Default - programming language python, 5 pages and print to screen (not saving to local db)
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--topic', choices=[1, 2, 3, 4, 5], type=int,
                       help="choose topic to scrape. 1-Communications, 2-Database, \
                        3-Games/Entertainment, 4-Internet, 5-Scientific/Engineering")

    group.add_argument('-o', '--op', choices=[1, 2, 3], type=int,
                       help="choose OP to scrape. 1-MacOS, 2-Windows, 3-unix")

    group.add_argument('-f', '--framework', choices=[1, 2], type=int,
                       help="choose topic to scrape. 1-django, 2-plone")

    group.add_argument('-p', '--programming', choices=[1, 2, 3], default=1, type=int,
                       help="choose programming language to scrape. 1-python (default), \
                        2-SQL, 3-C++")

    parser.add_argument('-n', '--number', default=5, type=int,
                        help="number of pages to scarp. 20 packages per page. default - 5")

    parser.add_argument('-s', '--save', action="store_true",
                        help="save data to file or print only. Default False")

    args = parser.parse_args()

    if args.topic is not None:
        print_data(START_DICT['topic'][str(args.topic)], args.number, args.save)

    elif args.op is not None:
        print_data(START_DICT['op'][str(args.op)], args.number, args.save)

    elif args.framework is not None:
        print_data(START_DICT['framework'][str(args.framework)], args.number, args.save)

    elif args.programming is not None:
        print_data(START_DICT['programming'][str(args.programming)], args.number, args.save)

    else:
        print_data(START_DICT['programming'][str(args.programming)], args.number, args.save)


if __name__ == '__main__':
    main()
