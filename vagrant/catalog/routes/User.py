from . import routes
from helpers import Catalog,\
    Oauth
from models import UserModel
from flask import render_template,\
    session as appsession,\
    request,\
    make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2


@routes.route('/user/<int:user_id>')
def User(user_id):
    '''
    user page
    '''

    return 'user page'


@routes.route('/login', methods=['GET', 'POST'])
def Login():
    '''
    login
    '''

    if request.method == 'POST':
        # verify state (csrf attack protection)
        if request.args.get('state') != appsession['state']:
            response = make_response(json.dumps(
                'Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # if logged in already, return appropriate response
        stored_credentials = appsession.get('access_token')
        stored_user_id = appsession.get('user_id')
        if stored_credentials is not None and stored_user_id is not None:
            response = make_response(json.dumps(
                {'response': 'user logged in already'}), 200)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Obtain authorization code
        authcode = request.data

        # exchange the authorization code for credentials object
        try:
            oauth_flow = flow_from_clientsecrets(
                'client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(authcode)
        except FlowExchangeError:
            response = make_response(
                json.dumps('Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # check token validity
        # If there was an error in the token info, abort.
        tokeninfo = Oauth.google_get_tokeninfo(credentials.access_token)
        if tokeninfo.get('error') is not None:
            response = make_response(json.dumps(
                {"error": "invalid token"}), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        # check if the user id (google user id) is valid,
        # i.e, matches with credentials object
        if tokeninfo['user_id'] != credentials.id_token['sub']:
            response = make_response(json.dumps(
                {"error": "invalid user id"}), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is valid for this app.
        if tokeninfo['issued_to'] != Oauth.google_get_client_id():
            response = make_response(json.dumps(
                {"error": "invalid app token"}), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        # store credentials object (access token) in session
        # store google id in session
        appsession['access_token'] = credentials.access_token
        appsession['google_id'] = tokeninfo['user_id']

        # get user info from google
        userinfo = Oauth.google_get_userinfo(credentials.access_token)

        # register user
        user = UserModel.register_user(userinfo)

        # store user id in session
        appsession['user_id'] = user.id

        # send response to application
        response = make_response(json.dumps(
            {"response": "user logged in"}), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    else:
        state_token = Catalog.generate_state_token()

        # store state token in session
        appsession['state'] = state_token

        # render login template
        return render_template('login.html', STATE=state_token)


@routes.route('/logout')
def Logout():
    '''
    logout
    '''

    return 'logout page'
