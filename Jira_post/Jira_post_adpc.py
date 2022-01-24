import requests
from requests.exceptions import HTTPError
import json
from Config.config import auth

NAME = "Stanislav.Gubanov"
BUILD = ""


"""
Priority
"name": "LOW", "id": "9"
"name": "MED", "id": "8"

Sevirity
"customfield_10073": {
            "value": "normal",
            "id": "10093"
        }
"""

url = "https://jira.aip.ooo/rest/api/latest/issue/"

headers = {
    'Content-Type': "application/json",
    'Accept': 'application/json'
}

data = {
    "fields": {
        "project": {
            "id": "10102",
            "key": "ADPC",
            "name": "Acronis Data Protection Cloud"
        },
        # Epic nope
        "customfield_10101": "ADPC-25",
        # Sprint
        "customfield_10105": 366,
        # Story Point
        "customfield_10106": 1.0,
        # Affected Build
        "customfield_10416": 21671,
        "versions": [
            {
                "id": "10201",
                "name": "21.06"
            }
        ],
        "summary": "Jira API Test",
        "description": f"*Description*\r\n\r\n--\r\n\r\n*Steps to Reproduce:*\r\n\r\n \r\n\r\n # install AIP LIGHT "
                       f"\\\\buildstorage.aip.ooo\\builds\\devlock\\main_fre_rus\\feature_aip-lite\\18\r\n\r\n "
                       f"\r\n\r\n *Actual Results:*\r\n\r\n -- \r\n\r\n*Expected Results:*\r\n\r\n --"
                       f"\r\n\r\n*Environment/OS:*\r\n\r\n *Build:* {BUILD}\r\n *OS:* WIN10x64\r\n\r\n \r\n\r\n*Additional "
                       f"information:*\r\n\r\n*Stand*:\r\n\r\n [https://ru3-cloud.dc.adc.aip.ooo|https://ru3-cloud.dc.adc.aip.ooo/]\r\n\r\n",
        "issuetype": {
            "id": "10004",
            "name": "Bug"
        },
        "fixVersions": [
            {
                "id": "10201",
                "name": "21.06"
            }
        ],
        "assignee": {
            "self": f"https://pmc.acronis.com/rest/api/2/user?username={NAME}",
            "name": NAME
        },
        # "reporter": {
        #     "name": NAME,
        #     "key": "JIRAUSER42192"
        # },
        # QA Engineer
        "customfield_10413": {
            "self": f"https://pmc.acronis.com/rest/api/2/user?username={NAME}",
            "name": NAME
        },
        "priority": {
            "name": "Medium",
            "id": "3"
        },
        "components": [
        ],
    }
}

try:
    response = requests.post(url, auth=auth, headers=headers, data=json.dumps(data))
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
else:
    print("Status code " + str(response.status_code))

print(response)
print(response.text)
print(type(response.text))
# print(f'https://pmc.acronis.com/browse/{response.text["key"]}')
