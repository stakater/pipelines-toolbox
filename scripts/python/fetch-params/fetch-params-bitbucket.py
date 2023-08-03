import json
from requests.auth import HTTPBasicAuth
# data = '''
# {
#   "values": [
#     {
#       "id": 1,
#       "source": {
#          "commit": {
#            "hash": "abcd"
#          }
#        }},
#       {
#       "id": 2,
#       "source": {
#          "commit": {
#            "hash": "defg"
#          }
#        }
#     }
#   ]
# }
# '''
#
# # Parse the JSON data
# parsed_data = json.loads(data)
#
# id_related_to_abcd = None
# for item in parsed_data['values']:
#     if item['source']['commit']['hash'] == 'abcd':
#         id_related_to_abcd = item['id']
#         break
#
# print("The id related to the hash 'abcd' is:", id_related_to_abcd)

import requests

def send_api_request():

    provider = "bitbucket"
    if provider == "bitbucket":


       username = "asfamumtaz"
       password = "ATBBsvFHFwZmFuEkCXYMp9eAczAh6FDF9827"

       workspace = "rabbitmqwebhook"
       repository = "rabbitmq-test"
       hash = "test"
       url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pullrequests"


    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            print("API Response:")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")

        parsed_data = json.loads(response.text)

       url = f"https://api.bitbucket.org/2.0/repositories/{owner}/{repo}/pullrequests/{pull_request_id}/commits"
       commits = get_all_commits_in_pull_request(owner, repo, pull_request_id, username, password)

        id_related_to_hash = None
        for pull_request in parsed_data['values']:
            pull_request_id = pull_request['id']
            commits = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pullrequests/{pull_request_id}/commits"
        if commits:
          for commit in commits['values']:
            print(f"Commit ID: {commit['hash']}, Author: {commit['author']['raw']}, Message: {commit['message']}")


#             print(item['source']['commit']['hash'])
#             if item['source']['commit']['hash'] == hash:
#                 id_related_to_hash = item['id']
#                 break

        print("The id related to the hash {hash} is:", id_related_to_hash)

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the API request: {e}")

if __name__ == "__main__":
#     api_url = "https://api.bitbucket.org/2.0/repositories/rabbitmqwebhook/rabbitmq-test/refs/branches"

    send_api_request()