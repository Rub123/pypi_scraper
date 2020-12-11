import os
import requests


token = os.getenv('GITHUB_TOKEN', '0119bfb608ccac9f07c1b7b32886a8ed0f33d1d7')


def parse_github_url(github_url: str) -> tuple:
    repo_owner, repo_name = github_url.split('/')[-2:]
    return repo_owner, repo_name


def get_contributors_query(repo_owner, repo_name) -> str:
    return f'https://api.github.com/repos/{repo_owner}/{repo_name}/contributors'


def get_github_query_results(query, token_=token):
    headers = {'Authorization': f'token {token}'}
    git_request = requests.get(query, headers=headers)
    return git_request.json()



def get_contributors_number(repo_owner, repo_name, token_=token):
    return len(get_github_query_results(get_contributors_query(repo_owner, repo_name), token_))






