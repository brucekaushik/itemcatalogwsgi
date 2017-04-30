from . import routes
from flask import request,\
    render_template,\
    session as appsession,\
    make_response,\
    flash,\
    redirect
from helpers import Catalog
from models import CategoryModel,\
	ItemModel,\
	CatalogModel
import json

@routes.route('/item/<string:item_name>/<int:item_id>')
def Item(item_name, item_id):
	'''
	Item page: 
	'''
	return 'item page'


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

	if request.method == 'POST':
		# verify state (csrf attack protection)
		if request.form.get('state') != appsession['state']:
			response = make_response(json.dumps(
			    {'response': 'invalid state parameter'}), 401)
			response.headers['Content-Type'] = 'application/json'
			return response

		item_name = request.form.get('name').strip()
		item_description = request.form.get('description').strip()
		category_id = request.form.get('category_id')
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

		# get categories
		categories = CategoryModel.get_categories()

		return render_template('add_item.html',
				STATE=state_token,
				appsession=appsession,
				categories=categories)


@routes.route('/item/<int:item_id>/edit')
def EditItem(item_id):
	'''
	edit item
	'''
	return 'edit item page'


@routes.route('/item/<int:item_id>/delete')
def DeleteItem(item_id):
	'''
	delete item
	'''
	return 'delete item page'