from . import routes


@routes.route('/item/<string:item_name>/<int:item_id>')
def Item(item_name, item_id):
	'''
	Item page: 
	'''
	return 'item page'


@routes.route('/item/add')
def AddItem():
	'''
	add item
	'''
	return 'add item page'


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