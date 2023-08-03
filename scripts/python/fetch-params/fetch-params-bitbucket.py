import json
import requests
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":
    provider = "bitbucket"
    if provider == "bitbucket":
      username = "asfamumtaz"
      password = "ATBBsvFHFwZmFuEkCXYMp9eAczAh6FDF9827"

      workspace = "rabbitmqwebhook"
      repository = "rabbitmq-test"
      hash = "43ec2e8e5342568f52c44c0987e79bd321cbb22a"
      url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pullrequests"
      parsed_data = ""
      try:
          response = requests.get(url, auth=HTTPBasicAuth(username, password))
          if response.status_code == 200:
              print("API Response:")
              parsed_data = json.loads(response.text)
          else:
              print(f"Request failed with status code: {response.status_code}")
              print(f"Response content: {response.text}")
      except requests.exceptions.RequestException as e:
        print(f"Error occurred during the API request: {e}")


      for pull_request in parsed_data['values']:
        pull_request_id = pull_request['id']
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pullrequests/{pull_request_id}/commits"
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        commits = response.json()
        if commits:
          for commit in commits['values']:
            print(f"Commit ID: {commit['hash']}, Author: {commit['author']['raw']}, Message: {commit['message']}")
            if commit['hash'] == hash:
              print("Found hash in PR")
              print(pull_request_id)
              return