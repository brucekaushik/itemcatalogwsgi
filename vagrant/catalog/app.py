from flask import Flask

app = Flask(__name__)


@app.route('/helloworld')
def HelloWorld():
	'''
	hello world controller
	'''
	return 'hello world'

@app.route('/')
def Home():
	'''
	home page: display category list & latest items added (10)
	'''
	return 'home page'


@app.route('/category/<string:category_name>/<int:category_id>')
def Category(category_name, category_id):
	'''
	category page: display category list & items in category
	'''
	return 'category page'


@app.route('/category/add')
def AddCategory():
	'''
	add category
	'''
	return 'add category page'


@app.route('/category/<int:category_id>/edit')
def EditCategory(category_id):
	'''
	edit category
	'''
	return 'edit category page'


@app.route('/category/<int:category_id>/delete')
def DeleteCategory(category_id):
	'''
	delete category
	'''
	return 'delete category page'


@app.route('/item/<string:item_name>/<int:item_id>')
def Item(item_name, item_id):
	'''
	Item page: 
	'''
	return 'item page'


@app.route('/item/add')
def AddItem():
	'''
	add item
	'''
	return 'add item page'


@app.route('/item/<int:item_id>/edit')
def EditItem(item_id):
	'''
	edit item
	'''
	return 'edit item page'


@app.route('/item/<int:item_id>/delete')
def DeleteItem(item_id):
	'''
	delete item
	'''
	return 'delete item page'


@app.route('/user/<int:user_id>')
def User(user_id):
	'''
	user page
	'''
	return 'user page'


if __name__ == '__main__':
  app.secret_key = 'ItemCatalogUdacity'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)