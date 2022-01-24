import json
import requests
from Config.config import auth
from Confluence.confluence_ops import delete_page
from jira_get.Get_Bugs_ADPC import (
    jira_get_bugs,
    get_reinstall_data
)
from Consul.get_consul_kv import (
    services_version_dictionary,
    consul2html
)

PARENT_PAGE_ID = 41124783
SPACE_KEY = 'ADP'

# Request URL - API for creating a new page as a child of another page
URL = 'https://adn.aip.ooo/rest/api/content/'

# Request Headers
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Set the title and content of the page to create
# Getting Bugs from Jira
closed_events = jira_get_bugs(
    {"jql": "project = 'Acronis Data Protection Cloud' AND type = Bug AND "
            "fixVersion = 21.06 and status in (Closed, Tested)"},
    bug_type='closed bugs'
)
opened_events = jira_get_bugs(
    {"jql": "project = 'Acronis Data Protection Cloud' AND type = Bug AND "
            "fixVersion = 21.06 AND status not in (Closed, Reopened, Canceled, Tested)"}
)
reopened_events = jira_get_bugs(
    {"jql": "project = 'Acronis Data Protection Cloud' AND "
            "type = Bug AND fixVersion = 21.06 AND status in (Reopened)"}
)
# reinstall date
reinstall_date = get_reinstall_data()[3]
reinstall_data = get_reinstall_data()

html_reinstall_ADPCv2 = (
    f"<table border='1'>"
    f"<tr><th>Task</th>"
    f"<td><ac:structured-macro ac:name='jira'>"
    f"<ac:parameter ac:name='key'>{reinstall_data[0]['issue_key']}</ac:parameter></ac:structured-macro>"
    f"</td></tr>"
    f"<tr><th>Done by</th>"
    f"<td>{reinstall_data[2]}</td></tr> "
    f"<tr><th>Mode</th>"
    f"<td>{reinstall_data[1]}</td></tr>"
    f"<tr><th>Date</th><td>{reinstall_data[3]}</td></tr></table> "
)

print(html_reinstall_ADPCv2)


# function put variables int to confluence macros
def json_to_html_tbz(events):
    html_table = []
    for html_issue in events:
        html_table.append(
            f'<tr><th><ac:structured-macro ac:name="jira"><ac:parameter ac:name="key">{html_issue}'
            f'</ac:parameter></ac:structured-macro></th><td></td></tr>')
    html_string = ''.join(html_table)
    return f"<table border='1'>{html_string}</table>"


page_title = f'Auto ADPC 21.06 {reinstall_date}'
page_html = (
    f'<p><small>Page data created automatically!</small></p>'
    f'<p><b>installed by task</b></p>'
    f'{html_reinstall_ADPCv2}<br></br>'
    f'<p><h2><b>Closed bugs</b></h2></p>'
    f'{json_to_html_tbz(closed_events)}<br></br>'
    f'<h2><b>Opened bugs</b></h2>'
    f'{json_to_html_tbz(opened_events)}<br></br>'
    f'<h2><b>Reopened bugs</b></h2>'
    f'{json_to_html_tbz(reopened_events)}<br></br>'
    f'<h2><b>Version of components</b></h2>'
    f'{consul2html(services_version_dictionary)}'
)


def get_request_data():
    return {
        'type': 'page',
        'title': page_title,
        'ancestors': [{'id': PARENT_PAGE_ID}],
        'space': {'key': SPACE_KEY},
        'body': {
            'storage': {
                'value': page_html,
                'representation': 'storage',
            }
        }
    }


# We're ready to call the api
delete_page()
try:
    response = requests.post(URL, auth=auth, headers=HEADERS, data=json.dumps(get_request_data()))
    print(response)
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
else:
    print('Status code ' + str(response.status_code))
