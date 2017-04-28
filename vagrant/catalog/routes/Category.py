from . import routes


@routes.route('/category/<string:category_name>/<int:category_id>')
def Category(category_name, category_id):
	'''
	category page: display category list & items in category
	'''
	return 'category page'


@routes.route('/category/add')
def AddCategory():
	'''
	add category
	'''
	return 'add category page'


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