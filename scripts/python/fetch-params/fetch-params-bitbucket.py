import json

data = '''
{
  "values": [
    {
      "id": 1,
      "source": {
         "commit": {
           "hash": "abcd"
         }
       }},
      {
      "id": 2,
      "source": {
         "commit": {
           "hash": "defg"
         }
       }
    }
  ]
}
'''

# Parse the JSON data
parsed_data = json.loads(data)

id_related_to_abcd = None
for item in parsed_data['values']:
    if item['source']['commit']['hash'] == 'abcd':
        id_related_to_abcd = item['id']
        break

print("The id related to the hash 'abcd' is:", id_related_to_abcd)

import requests

def send_api_request(url):

    if provider == "bitbucket":

       username = "asfamumtaz"
       password = "ATBBsvFHFwZmFuEkCXYMp9eAczAh6FDF9827"
       provider = "bitbucket"
       workspace = "rabbbitmqwebhook"
       repository = "rabbitmq-test"
       hash = "43ec2e8e5342568f52c44c0987e79bd321cbb22a"
       url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/refs/branches"


    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            print("API Response:")
            print(response.json())
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the API request: {e}")

if __name__ == "__main__":
    api_url = "https://api.bitbucket.org/2.0/repositories/rabbitmqwebhook/rabbitmq-test/refs/branches"

    send_api_request(api_url)