import os
import requests
from pprint import pprint as pp


token = os.getenv('GITHUB_TOKEN', "here you put the token")
git_query = f'https://api.github.com/repos/numpy/numpy/contributors'
headers = {'Authorization': f'token {token}'}
git_request = requests.get(git_query, headers=headers)
pp(len(git_request.json()))


