import httplib2
import json
import requests
from flask import request,\
    make_response


def google_get_client_id():
    '''
    read google+ client id from client_secrets.json
    return client id
    '''

    return json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']


def google_get_tokeninfo(access_token):
    '''
    Check that the access token is valid,
    by making a call to google+ api
    we should get a json response containing token info like:
            who the token is issued to
            user_id
            email
            expires etc..
    '''

    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)  # try in browser
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    return result


def google_get_userinfo(access_token):
    '''
    # Get user info (from google)
    '''
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    userdata = requests.get(userinfo_url, params=params)

    data = userdata.json()

    return data
