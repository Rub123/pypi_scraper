import os
import requests
from private_passwords import GITHUB_TOKEN


token = os.getenv('GITHUB_TOKEN', GITHUB_TOKEN)


def parse_github_url(github_url: str) -> tuple:
    """
    given a github url, extract repo_owner, repo_name
    :param github_url: url to github from the scaper
    :return: tuple with repo_owner, repo_name extracted from the url
    """
    repo_owner, repo_name = github_url.split('/')[-2:]
    return repo_owner, repo_name


def get_contributors_query(repo_owner, repo_name) -> str:
    """
    given repo_owner and repo_name create an api query to get contributors list from github api
    :param repo_owner: str
    :param repo_name: str
    :return: link to api query
    """
    return f'https://api.github.com/repos/{repo_owner}/{repo_name}/contributors'


def get_github_query_results(query, token_=token):
    """
    given query and api token, get query results
    :param query: str
    :param token_: str
    :return: query result
    """
    headers = {'Authorization': f'token {token_}'}
    git_request = requests.get(query, headers=headers)
    return git_request.json()


def get_contributors_number(repo_owner, repo_name, token_=token):
    """
    given repo_owner, repo_name and api token_ get amount of contributors
    :param repo_owner: str
    :param repo_name: str
    :param token_: str
    :return: number of contributors
    """
    return len(get_github_query_results(get_contributors_query(repo_owner, repo_name), token_))
