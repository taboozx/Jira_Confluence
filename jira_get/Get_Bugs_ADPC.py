from datetime import datetime
from collections import defaultdict
import re
import requests
from Config.config import auth

URL = 'https://jira.aip.ooo/rest/api/2/search'
HEADERS = {'Content-Type': 'application/json'}


def create_issues(response, bug_type):
    fresh_issues = []
    for issue in response['issues']:
        issue_key = issue['key']
        issue_updated_raw = issue['fields']['updated']
        issue_updated = datetime.strptime(issue_updated_raw, '%Y-%m-%dT%H:%M:%S.%f+0300')
        # put data in to list
        if bug_type == 'all bugs':
            delta = datetime.today() - issue_updated
            if delta.total_seconds() < 4209600:
                fresh_issues.append(issue_key)
        else:
            if issue_updated > get_reinstall_date():
                fresh_issues.append(issue_key)

    return fresh_issues


def create_tasks_dictionary(response):
    fresh_tasks_dictionary = []
    for issue in response['issues']:
        issue_key = issue['key']
        issue_name = issue['fields']['summary']
        issue_assignee = issue['fields']['assignee']['name']
        # issue_status = issue['fields']['status']['name']
        issue_updated_raw = issue['fields']['updated']
        issue_resolved_raw = issue['fields']['resolutiondate']

        issue_resolved = datetime.strptime(issue_resolved_raw, '%Y-%m-%dT%H:%M:%S.%f+0300')
        issue_updated = datetime.strptime(issue_updated_raw, "%Y-%m-%dT%H:%M:%S.%f+0300")

        # if date is ok, put data in to dictionary
        delta = datetime.today() - issue_resolved
        if delta.total_seconds() < 2209600:
            if re.search('Reinstall ADPC', issue_name):
                fresh_tasks_dictionary.append({
                    'issue_key': issue_key,
                    'issue_name': issue_name,
                    'issue_assignee': issue_assignee,
                    'issue_resolved': issue_resolved,
                    'issue_updated': issue_updated
                })

    return fresh_tasks_dictionary


def jira_get_bugs(data, bug_type='all bugs'):
    response = requests.post(URL, json=data, auth=auth, headers=HEADERS).json()
    return create_issues(response, bug_type)


def jira_get_ReinstallADPC_tasks():
    data = {
        "jql": "project = 'DEVOPS' AND "
               "type = Story AND 'Epic Link' = DEVOPS-458 AND "
               "summary ~ 'Reinstall' AND status in (Resolved) AND "
               "created > -4w ORDER BY created DESC"
    }
    response = requests.post(URL, json=data, auth=auth, headers=HEADERS).json()
    return create_tasks_dictionary(response)


print(jira_get_ReinstallADPC_tasks())


# Get ReInstallation data ADPC stand
def get_reinstall_date():
    json = jira_get_ReinstallADPC_tasks()[0]
    reinstall_date = json['issue_resolved']
    return reinstall_date


def get_reinstall_data():
    task = jira_get_ReinstallADPC_tasks()
    json = task[0]
    reinstall_date = str(json['issue_updated']).split(' ', maxsplit=1)[0]
    reinstall_name = json['issue_name']
    reinstall_assignee = json['issue_assignee']

    return [json, reinstall_name, reinstall_assignee, reinstall_date]
