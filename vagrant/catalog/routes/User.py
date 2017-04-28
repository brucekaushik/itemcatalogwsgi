from . import routes


@routes.route('/user/<int:user_id>')
def User(user_id):
	'''
	user page
	'''
	return 'user page'