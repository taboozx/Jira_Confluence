from datetime import datetime
from collections import defaultdict
from Config.config import auth
import requests

from jira_get.Get_Bugs_ADPC import get_reinstall_date


def jira_get_events():
    url = "https://jira.aip.ooo/rest/api/2/search"
    headers = {'Content-Type': "application/json"}
    data = {"jql": "project = ADLP AND 'Epic Link' = ADLP-38 and status not in (Tested)"}
    response = requests.post(url, json=data, auth=auth, headers=headers).json()
    fresh_issue_dictionary = defaultdict(dict)
    total_issues = response['total']
    for issue in response['issues']:
        issue_key = issue['key']
        issue_name = issue['fields']['summary']
        issue_status = issue['fields']['status']['name']
        issue_priority = issue['fields']['priority']['name']
        issue_description = issue['fields']['description']
        issue_reporter = issue['fields']['reporter']['name']
        issue_type = issue['fields']['issuetype']['name']
        issue_created_raw = issue['fields']['created']
        issue_updated_raw = issue['fields']['updated']

        issue_updated = datetime.strptime(issue_updated_raw, "%Y-%m-%dT%H:%M:%S.%f+0300")
        issue_created = datetime.strptime(issue_created_raw, "%Y-%m-%dT%H:%M:%S.%f+0300")

        # написать логику если issue_updated() меньше текущего времени на ххх то
        # заносим данные по дефекту в dictionary
        delta = datetime.today() - issue_updated
        if delta.total_seconds() < 1209600:
            print(delta)
            fresh_issue_dictionary[issue_key].update({
                'issue_name': issue_name,
                'issue_status': issue_status,
                'issue_priority': issue_priority,
                'issue_reporter': issue_reporter,
                'issue_type': issue_type,
                'issue_created': issue_created,
                'issue_updated': issue_updated
            })

    return fresh_issue_dictionary, total_issues


issues, total = jira_get_events()
print(total)
print(issues)

for issue in issues:
    print(f'Key: {issue} \n'
          + 'Name: ' + issues[issue]['issue_name'] + '\n'
          + 'Status: ' + issues[issue]['issue_status'] + '\n'
          + 'Priority: ' + issues[issue]['issue_priority'] + '\n'
          + 'Reporter: ' + issues[issue]['issue_reporter'] + '\n'
          + 'Issue_type: ' + issues[issue]['issue_type'] + '\n'
          + f"Created:  {issues[issue]['issue_created']}" + '\n'
          + f"Updated:  {issues[issue]['issue_updated']}" + '\n\n')
