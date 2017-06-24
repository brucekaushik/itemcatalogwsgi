from . import routes
from catalog.helpers import Oauth
from catalog.helpers import Catalog as CatalogHelper
from catalog.models import *
from flask import render_template,\
    session as appsession,\
    request,\
    redirect,\
    make_response,\
    flash
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import requests
from catalog import catalogvars


@routes.route('/user')
def User():
    '''
    user page
    '''

    # fetch all categories
    categories = CategoryModel.get_categories()

    # fetch latest items
    items = ItemModel.get_user_items(appsession['user_id'])

    # fetch user info from google
    userinfo = Oauth.google_get_userinfo(appsession['access_token'])

    return render_template('user.html',
                           categories=categories,
                           items=items,
                           appsession=appsession,
                           userinfo=userinfo)


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
                catalogvars.client_secrets_json, scope='')
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
        state_token = CatalogHelper.generate_state_token()

        # store state token in session
        appsession['state'] = state_token

        # render login template
        return render_template('login.html',
                               STATE=state_token,
                               appsession=appsession)


@routes.route('/logout')
def Logout():
    '''
    logout
    '''

    access_token = appsession.get('access_token')

    # check token validity
    # If there was an error in the token info, logout & redirect.
    tokeninfo = Oauth.google_get_tokeninfo(access_token)
    if tokeninfo.get('error') is not None:
        # delete session variables
        del appsession['user_id']
        del appsession['access_token']
        del appsession['google_id']

        flash('logout successful')
        return redirect('/')

    # check if access token exists
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # make request to google to revoke the user access token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # delete session variables
        del appsession['user_id']
        del appsession['access_token']
        del appsession['google_id']

        flash('logout successful')
        return redirect('/')

    else:
        # show failure
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
