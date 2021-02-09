from logging import error
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import time
from flask import render_template, current_app
from flask_login import current_user
from app import db
from app.models import User, Domain

class ApiResult():
    def __init__(self, html='', status_code='', error_message=''):
        self.html = html
        self.status_code = status_code
        self.error_message = error_message


class IOC():
    def __init__(self, iocDomain='', iocBlackListId='', iocType='', iocValue='', description='',
                 emailDirection='', remediationAction='', status='', expiryDate=''):
        self.iocDomain = iocDomain,
        self.iocBlackListId = iocBlackListId
        self.iocType = iocType
        self.iocValue = iocValue
        self.description = description
        self.emailDirection = emailDirection
        self.remediationAction = remediationAction
        self.status = status
        self.expiryDate = expiryDate


def DownloadIOC(domain='global'):
    result = ApiResult()
    headers = {'content-type': 'application/json',
               'accept': 'application/json'}
    base_url = current_app.config['ECAPI_URL']
    url = base_url + 'domains/' + domain + '/iocs/download'
    r = requests.get(url,
                     auth=HTTPBasicAuth(current_user.clientnet_user,
                                        current_user.clientnet_password),
                     headers=headers)
    result.status_code = r.status_code

    if result.status_code == 200:
        iocs = json.loads(r.content)
        result.html = render_template('_iocs.html', iocs=iocs, domainname=domain)
    else:
        if result.status_code == 202:
            result.error_message = json.loads(r.content)[0]['failureReason']
        elif result.status_code == 401:
            result.error_message = 'Unauthorized access. Username or password incorrect'
        elif result.status_code == 403:
            result.error_message = 'Access denied. User has no access to this API'
        else:
            result.html = 'Error ' + str(r.status_code)
    return result


def UpdateIOC(ioc, action='D'):
    result = ApiResult()
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    base_url = current_app.config['ECAPI_URL']
    url = base_url + 'domains/' + ioc.iocDomain[0] + '/iocs/upload'
    params = {'api-list-action': 'IOC'}

    data = [{'APIRowAction': action,
             'iocBlackListId': ioc.iocBlackListId,
             'iocType': ioc.iocType,
             'iocValue': ioc.iocValue,
             'description': ioc.description,
             'emailDirection': ioc.emailDirection,
             'remediationAction': ioc.remediationAction
             }]

    r = requests.post(url, json=data,
                      auth=HTTPBasicAuth(current_user.clientnet_user,
                                         current_user.clientnet_password),
                      params=params,
                      headers=headers)
    result.status_code = r.status_code

    if result.status_code == 200:
        return result
    else:
        if result.status_code == 202:
            result.error_message = json.loads(r.content)[0]['failureReason']
        elif result.status_code == 401:
            result.error_message = 'Unauthorized access. Username or password incorrect'
        elif result.status_code == 403:
            result.error_message = 'Access denied. User has no access to this API'
        else:
            result.error_message = 'Unknown error'
            
        return result
