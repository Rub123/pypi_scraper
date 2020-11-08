from scrap_package_page import scrap_side_bars
from scrap_package_snippet import PackageSnippet, get_soup, get_n_pages_of_packages_snippets, get_package_details_url
from scrap_package_snippet import START_PAGE

SNIPPET_PAGES = 50  # 20 packages per page so 50 pages is for scraping a 1000 packages.
PACKAGE_SEPARATORS_CHARS = 100  # used to decide the length of a line that separates each package when printing


def append_to_file(text: str, file: str) -> None:
    """
    Add information to an existing file
    :param text: text to append to file
    :param file: path to file
    """
    with open(file, 'a', encoding='utf-8') as f:
        f.write(text)


def print_data(n_pages: int = SNIPPET_PAGES, save_file=None) -> None:
    """ Prints the scraped data to the screen. If save_file will also save the information to a file

    :param n_pages: unt, number of pages
    :param save_file: Define this parameter to save information to that file path # todo check if file path exists
    """
    packs_snips = get_n_pages_of_packages_snippets(n_pages, get_soup(START_PAGE))
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


if __name__ == '__main__':
    print_data(SNIPPET_PAGES, 'pypi_packages.txt') # todo shouldn't pypi_packages be a constant? this looks lik
