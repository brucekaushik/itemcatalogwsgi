from . import routes

@routes.route('/helloworld')
def HelloWorld():
	'''
	hello world controller
	'''
	return 'hello world'