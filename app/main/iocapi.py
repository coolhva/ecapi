from logging import error
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import time
from flask import render_template, current_app
from flask_login import current_user
from app import db
from app.models import User

class IOCDownload():
    def __init__(self, html, status_code, error_message):
        self.html = html
        self.status_code = status_code
        self.error_message = error_message
        
def DownloadIOC():
    result = IOCDownload('','','')
    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    base_url = current_app.config['ECAPI_URL']
    url = base_url + 'domains/global/iocs/download'
    r = requests.get(url,
        auth=HTTPBasicAuth(current_user.clientnet_user, 
                           current_user.clientnet_password),
        headers = headers)
    result.status_code = r.status_code

    if result.status_code == 200:
        iocs = json.loads(r.content)
        result.html = render_template('_iocs.html', iocs=iocs)
    else:
        if result.status_code == 401:
            result.error_message = 'Unauthorized access. Username or password incorrect'
        elif result.status_code == 403:
            result.error_message = 'Access denied. User has no access to this API'
        else:
            result.html = 'Error ' + str(r.status_code)        
    return result
