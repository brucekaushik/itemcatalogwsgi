from . import routes
from flask import request,\
    render_template,\
    session as appsession,\
    make_response,\
    flash,\
    redirect,\
    jsonify
from helpers import Catalog
from models import CategoryModel,\
    ItemModel,\
    CatalogModel
import json


@routes.route('/item/<string:item_name>/<int:item_id>')
def Item(item_name, item_id):
    '''
    Item page (view item)
    '''

    # get categories
    categories = CategoryModel.get_categories()

    # get item
    item = ItemModel.get_item_by_id(item_id)
    if not item:
        response = make_response(json.dumps(
            {'error': 'item not found'}), 404)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get item category name
    category = CategoryModel.get_category_by_id(item.category_id)
    category_name = category.name

    return render_template('view_item.html',
                           appsession=appsession,
                           categories=categories,
                           item=item,
                           category_name=category_name)


@routes.route('/itemjson/<string:item_name>/<int:item_id>')
def ItemJson(item_name, item_id):
    '''
    Item Json Endpoint
    '''

    # get item
    item = ItemModel.get_item_by_id(item_id)

    if not item:
        return jsonify({'error': 'item not found'})

    item = item.serialize
    return jsonify(item=item)


@routes.route('/item/add', methods=['GET', 'POST'])
def AddItem():
    '''
    add item
    '''

    # if not logged in, ask user to login
    # technically, this page should not be accessible unless logged in
    stored_credentials = appsession.get('access_token')
    stored_user_id = appsession.get('user_id')
    if stored_credentials is None and stored_user_id is None:
        response = make_response(json.dumps(
            {'response': 'please login first'}), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get categories
    categories = CategoryModel.get_categories()

    if request.method == 'POST':
        # verify state (csrf attack protection)
        if request.form.get('state') != appsession['state']:
            response = make_response(json.dumps(
                {'response': 'invalid state parameter'}), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # get form variables
        item_name = request.form.get('name').strip()
        item_description = request.form.get('description').strip()
        category_id = request.form.get('category_id')

        if not (item_name and item_description and category_id):
            flash('all fields mandatory, please fill')
            return render_template('add_item.html',
                                   STATE=request.form.get('state'),
                                   appsession=appsession,
                                   categories=categories)

        # add item
        result = ItemModel.add_item(item_name, item_description, category_id)
        if result:
            flash('item added successfully')
        else:
            flash('failed to add item, it might already exit in catalog')

        return redirect('/')

    else:
        state_token = Catalog.generate_state_token()

        # store state token in session
        appsession['state'] = state_token

        return render_template('add_item.html',
                               STATE=state_token,
                               appsession=appsession,
                               categories=categories)


@routes.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def EditItem(item_id):
    '''
    edit item
    '''

    # if not logged in, ask user to login
    # technically, this page should not be accessible unless logged in
    stored_credentials = appsession.get('access_token')
    stored_user_id = appsession.get('user_id')
    if stored_credentials is None and stored_user_id is None:
        response = make_response(json.dumps(
            {'response': 'please login first'}), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if request.method == 'POST':
        # verify state (csrf attack protection)
        if request.form.get('state') != appsession['state']:
            response = make_response(json.dumps(
                {'response': 'invalid state parameter'}), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # get form variables
        item_id = request.form.get('item_id').strip()
        item_name = request.form.get('name').strip()
        item_description = request.form.get('description').strip()
        category_id = request.form.get('category_id')

        # edit item
        result = ItemModel.edit_item(
            item_id, item_name, item_description, category_id)
        if result:
            flash('item updated successfully')
        else:
            flash('failed to update item')

        return redirect('/')

    else:
        state_token = Catalog.generate_state_token()

        # store state token in session
        appsession['state'] = state_token

        # get categories
        categories = CategoryModel.get_categories()

        # get item to edit
        item = ItemModel.get_item_by_id(item_id)
        if not item:
            response = make_response(json.dumps(
                {'error': 'item not found'}), 404)
            response.headers['Content-Type'] = 'application/json'
            return response

        # check if user id mismatch
        if item.user_id != appsession['user_id']:
            response = make_response(json.dumps(
                {'error': 'permission denied'}), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        return render_template('edit_item.html',
                               STATE=state_token,
                               appsession=appsession,
                               categories=categories, item=item)


@routes.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
def DeleteItem(item_id):
    '''
    delete item
    '''

    # if not logged in, ask user to login
    # technically, this page should not be accessible unless logged in
    stored_credentials = appsession.get('access_token')
    stored_user_id = appsession.get('user_id')
    if stored_credentials is None and stored_user_id is None:
        response = make_response(json.dumps(
            {'response': 'please login first'}), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if request.method == 'POST':
        # verify state (csrf attack protection)
        if request.form.get('state') != appsession['state']:
            response = make_response(json.dumps(
                {'response': 'invalid state parameter'}), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # get item id from from
        item_id = request.form.get('item_id').strip()

        # delete item
        result = ItemModel.delete_item(item_id)
        if result:
            flash('item deleted successfully')
        else:
            flash('failed to delete item')

        return redirect('/')

    else:
        state_token = Catalog.generate_state_token()

        # store state token in session
        appsession['state'] = state_token

        # get item to delete
        item = ItemModel.get_item_by_id(item_id)
        if not item:
            response = make_response(json.dumps(
                {'error': 'item not found'}), 404)
            response.headers['Content-Type'] = 'application/json'
            return response

        # get item category
        category = CategoryModel.get_category_by_id(item.category_id)

        # check for user id mismatch
        if item.user_id != appsession['user_id']:
            response = make_response(json.dumps(
                {'error': 'permission denied'}), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        return render_template('delete_item.html',
                               STATE=state_token,
                               appsession=appsession,
                               category=category,
                               item=item)
