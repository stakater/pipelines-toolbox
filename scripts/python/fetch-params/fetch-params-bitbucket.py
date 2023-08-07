import json
import requests
from requests.auth import HTTPBasicAuth
import argparse

def send_api_request(url, username, password):
   try:
       response = requests.get(url, auth=HTTPBasicAuth(username, password))
       if response.status_code == 200:
           parsed_data = json.loads(response.text)
           return parsed_data
       else:
           print(f"Request failed with status code: {response.status_code}")
           print(f"Response content: {response.text}")
           return None
   except requests.exceptions.RequestException as e:
     print(f"Error occurred during the API request: {e}")
     return None

def fetch_params_bitbucket(provider, username, password, hash, workspace, repository):

    print(f"provider: {provider}")
    print(f"provider: {username}")
    print(f"provider: {password}")
    print(f"provider: {hash}")
    print(f"provider: {workspace}")
    print(f"provider: {hash}")
    print(f"provider: {repository}")
    if provider == "bitbucket":

      url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pullrequests"

      response = send_api_request(url, username, password)
      found = False
      for pull_request in response['values']:
        if found == True:
          break
        pull_request_id = pull_request['id']
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pullrequests/{pull_request_id}/commits"
        commits = send_api_request(url, username, password)

        if commits:
          for commit in commits['values']:
            print(f"Commit ID: {commit['hash']}, Author: {commit['author']['raw']}, Message: {commit['message']}")
            if commit['hash'] == hash:
              print(f"Found hash in PR {pull_request_id}")
              found = True
              break
# def main(args):
#     provider = args.provider
#     username = args.username
#     password = args.password
#     hash = args.hash
#     workspace = args.workspace
#     repository = args.repository
#     fetch_params_bitbucket(provider, username, password, hash, workspace, repository)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("provider", help="The number for which to calculate square and cube.")
    parser.add_argument("username", help="The number for which to calculate square and cube.")
    parser.add_argument("password", help="The number for which to calculate square and cube.")
    parser.add_argument("hash", help="The number for which to calculate square and cube.")
    parser.add_argument("workspace", help="The number for which to calculate square and cube.")
    parser.add_argument("repository",  help="The number for which to calculate square and cube.")
    args = parser.parse_args()
    fetch_params_bitbucket(args.provider, args.username, args.password, args.hash, args.workspace, args.repository)
#     main(args)