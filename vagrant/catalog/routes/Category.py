from . import routes
from flask import request,\
    render_template,\
    session as appsession,\
    make_response,\
    flash,\
    redirect
from helpers import Catalog
from models import CategoryModel,\
    ItemModel
import json


@routes.route('/category/<string:category_name>/<int:category_id>')
def Category(category_name, category_id):
    '''
    category page: display category list & items in category
    '''

    # fetch all categories
    categories = CategoryModel.get_categories()

    # fetch category items
    items = ItemModel.get_category_items(category_id)

    return render_template('category.html',
                           category_name=category_name,
                           categories=categories, items=items,
                           appsession=appsession)


@routes.route('/category/add', methods=['GET', 'POST'])
def AddCategory():
    '''
    add category
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

        # add category
        category_name = request.form.get('name').strip()
        result = CategoryModel.add_category(category_name)
        if result:
            flash('category added successfully')
        else:
            flash('failed to add category, it might already exists')

        return redirect('/')

    else:
        state_token = Catalog.generate_state_token()

        # store state token in session
        appsession['state'] = state_token

        return render_template('add_category.html',
                               STATE=state_token,
                               appsession=appsession)


@routes.route('/category/<int:category_id>/edit')
def EditCategory(category_id):
    '''
    edit category
    '''
    return 'edit category page'


@routes.route('/category/<int:category_id>/delete')
def DeleteCategory(category_id):
    '''
    delete category
    '''
    return 'delete category page'
