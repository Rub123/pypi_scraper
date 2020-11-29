from config import START_DIC
import argparse

from scrap_package_page import scrap_side_bars
from scrap_package_snippet import PackageSnippet, get_soup, get_n_pages_of_packages_snippets, get_package_details_url
from scrap_package_snippet import START_PAGE

from config import SNIPPET_PAGES, PACKAGE_SEPARATORS_CHARS


def append_to_file(text: str, file: str) -> None:
    """Add 'text' to a file if exist (creating the file if it dose not).
    :param text: text to append to file
    :param file: path to file
    """
    with open(file, 'a', encoding='utf-8') as f:
        f.write(text)


def print_data(start_link: str, n_pages: int = 5, save_file=None) -> None:
    """ Prints the scraped data to the screen. If save_file will also save the information to a file
    :param start_link: link to start scraping from
    :param n_pages: int, number of pages
    :param save_file: An Optional file path to save the scraped data to.
    """
    packs_snips = get_n_pages_of_packages_snippets(n_pages, get_soup(start_link))
    packs_soups = (get_soup(get_package_details_url(pack)) for pack in packs_snips)
    data = (scrap_side_bars(soup, snip) for snip, soup in zip(packs_snips, packs_soups))

    for index, data_dict in enumerate(data, start=1):
        for pack_snip, pack_info in data_dict.items():
            pack_snip: PackageSnippet
            msg = f"""Package: {str(pack_snip.name)}, Version {str(pack_snip.version)}:

    Short description: {str(pack_snip.description)}

    More Info:"""

            info_msg = '\n'.join('\t' + key + ':' + str(value) for key, value in pack_info.items())

            print(msg)
            print(info_msg)
            print('-' * PACKAGE_SEPARATORS_CHARS)
            if save_file:
                append_to_file('\n'.join([msg, info_msg, ('-' * PACKAGE_SEPARATORS_CHARS), '\n']), save_file)
    print(f'Scraped {index} packages!')  # the last index form the enumerate loop above.


def main():
    """
    user chooses what to scape from a list of options.
    Default - programming language python
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
        print_data(START_DIC["topic"][args.topic], args.number, args.save)

    elif args.op is not None:
        print_data(START_DIC["op"][args.op], args.number, args.save)

    elif args.framework is not None:
        print_data(START_DIC["framework"][args.framework], args.number, args.save)

    elif args.programming is not None:
        print(args.programming)
        print_data(START_DIC["programming"][str(args.programming)], args.number, args.save)

    else:
        print_data(START_DIC["programming"][str(args.programming)], args.number, args.save)


if __name__ == '__main__':
    main()
