import sys
from requests.auth import HTTPBasicAuth

_, login, password = list(sys.argv)

auth = HTTPBasicAuth(login, password)
