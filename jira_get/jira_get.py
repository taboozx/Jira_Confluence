import requests

import json
from Config.config import auth

url = "https://jira.aip.ooo/rest/api/latest/issue/ADLP-14"
headers = {'Content-Type': "application/json"}

response = requests.get(url, auth=auth, headers=headers)
print(response)


pretty_json = json.loads(response.text)
issue_name = (pretty_json['fields']['issuetype']['description'])
issue_status = (pretty_json['fields']['status']['name'])
issue_priority = (pretty_json['fields']['priority']['name'])
issue_description = (pretty_json['fields']['description'])
issue_reporter = (pretty_json['fields']['reporter']['name'])
issue_created = (pretty_json['fields']['created'])
issue_updated = (pretty_json['fields']['updated'])

print('Name: ' + issue_name)
print('Status: ' + issue_status)
print('Priority: ' + issue_priority)
print('Reporter: ' + issue_reporter)
print('Created: ' + issue_created)
print('Updated: ' + issue_updated)

# print('Description: ' + issue_description)

# print(json.dumps(pretty_json, indent=2))
