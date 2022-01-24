import requests
import base64
import urllib3
from collections import defaultdict
from requests import HTTPError
from Bitbucket.get_bitbucket import format_bitbucket_data

urllib3.disable_warnings()

# get ip from inventory for consul (now we use hardcoded hostname)
# consul_ip = format_inventory()
consul_ip = 'ru3-cloud.dc.adc.aip.ooo'

services = [
    'appaccountsrv', 'accountsrv', 'api-gateway.chart', 
    'atp-grpm-addon.chart', 'reportingsrv', 'ui-core.chart',
    'mng_console'
]
services_version_dictionary = defaultdict(list)


def get_consul_versions(service):
    url = f'https://{consul_ip}:9999/v1/kv/msp_versions/{service}'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(url, headers=headers, verify=False).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        print(f'Other error occurred: {err}')
        return f'Consul doesnt respond'
    else:
        return str(base64.b64decode(response[0]['Value']))[1:]


def get_consul_builds(service):
    url = f'https://{consul_ip}:9999/v1/kv/msp_builds/{service}'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(url, headers=headers, verify=False).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        print(f'Other error occurred: {err}')
        return f'Consul doesnt respond'
    else:
        return str(base64.b64decode(response[0]['Value']))[1:]


for service_name in services:
    services_version_dictionary[service_name].extend([
        ('msp_version', get_consul_versions(service_name)),
        ('msp_build', get_consul_builds(service_name))
    ])

# Getting version from git
platform_chart_msp_version, platform_chart_msp_build = format_bitbucket_data()

services_version_dictionary['platform.chart'].extend([
    ('msp_version', platform_chart_msp_version),
    ('msp_build', platform_chart_msp_build)
])

print(services_version_dictionary)


def consul2html(d):
    html_consul = []
    for consul_service in d:
        html_consul.append(
            f'<tr><th>{consul_service}</th><td>'
            f'{": ".join(d[consul_service][0])}<br>'
            f'</br>{": ".join(d[consul_service][1])}</td></tr>')

    html_string = ''.join(html_consul)
    return f"<table border='1'>{html_string}</table>"
