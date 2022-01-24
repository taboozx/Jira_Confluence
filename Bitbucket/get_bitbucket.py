import re

import requests
# from Confluence.confluence_bug_report import auth
from Config.config import auth


# Get data from bitbucket
def get_bitbucket(url):
    headers = {'Content-Type': "application/json"}
    response = requests.get(url, auth=auth, headers=headers).json()
    return response['lines']


def format_bitbucket_data():
    arr2 = []
    for i in get_bitbucket("https://git.aip.ooo/rest/api/1.0/projects/ABCINF/repos/msp-scm/browse/builds/ADPC21.06/release-builds.yml"):
        arr2.append(list(i.values())[0].strip())

    r = re.compile(".*platform.chart")
    newlist = list(filter(r.match, arr2))

    arr3 = []
    for i in newlist:
        arr3.append(i.split(' ')[1])

    return arr3[0], arr3[1]


def format_inventory():
    arr2 = []
    for i in get_bitbucket(
            "https://git.aip.ooo/rest/api/1.0/projects/DCOINF/repos/production-deployment-environments/browse/inventories/production/ru3-cloud"):
        arr2.append(list(i.values())[0].strip())

    r = re.compile(".*ru3-cloud-platform-fw-vm01")
    return list(filter(r.match, arr2))[0].split('=')[1]


