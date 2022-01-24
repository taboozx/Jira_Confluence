import requests
from Config.config import auth
from requests import HTTPError

HEADERS = {'Content-Type': 'application/json'}


# Get id page by name
def confluence_get_report_id():
    URL = f'https://adn.aip.ooo/rest/api/content?spaceKey=ADP&title=Auto+ADPC+21.06+2022-01-11&expand=version'

    try:
        response = requests.get(URL, auth=auth, headers=HEADERS).json()
        return response['results'][0]['id']
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except IndexError as idx_err:
        print(idx_err)
    except Exception as err:
        print(f'Other error occurred: {err}')


# Delete Page by Id
def delete_page():
    URL = f'https://adn.aip.ooo/rest/api/content/{confluence_get_report_id()}'

    try:
        return requests.delete(URL, auth=auth, headers=HEADERS)
        print('page deleted')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        print(f'Other error occurred: {err}')
        return f'Consul doesnt respond'


