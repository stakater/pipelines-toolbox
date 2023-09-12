import json
import requests
from requests.auth import HTTPBasicAuth

def send_api_request_github(url, password):

   try:
       headers = {"Authorization": f"token {password}"}
       response = requests.get(url, headers=headers)
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

def fetch_params_github(provider, username, password, hash, workspace, repository):

    if provider == "github":
      url = f"https://api.github.com/repos/{workspace}/{repository}/pulls"
      print(url)
      pull_requests =  send_api_request_github(url, password)
      found = False
      if pull_requests:
        for pr in pull_requests:
          if found == True:
          break 
          pull_request_id = pr['number']
          url = f"https://api.github.com/repos/{workspace}/{repository}/pulls/{pull_request_id}/commits"
          commits = send_api_request_github(url, password)
          if commits:
            for commit in commits:
              print(f"Commit SHA: {commit['sha']}")
              if commit['sha'] == hash:
                print(f"Found hash in PR {pull_request_id}")
                found = True
                return pull_request_id
                break
          else:
             return None
      else:
         return None
