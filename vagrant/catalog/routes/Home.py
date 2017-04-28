from . import routes

@routes.route('/')
def Home():
	'''
	home page: display category list & latest items added (10)
	'''
	return 'home page'