import json
import requests
from requests.auth import HTTPBasicAuth

def send_api_request_gitlab(url, password):

   try:
       headers = {"PRIVATE-TOKEN": password}
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

def fetch_params_gitlab(provider, password, hash, project_id):

    if provider == "gitlab":
      url = f"{base_url}/api/v4/projects/{project_id}/merge_requests"
      pull_requests = send_api_request(url, password)
      if pull_requests:
        for pr in pull_requests:
          pull_request_id = pr['id']
          url = f"{base_url}/api/v4/projects/{project_id}/merge_requests/{pull_request_id}/commits"
          commits = send_api_request(url, password)
          if commits:
            for commit in commits:
              print(f"Commit SHA: {commit['id']}")
              if commit['id'] == hash:
                print(f"Found hash in PR {pull_request_id}")
                found = True
                break
