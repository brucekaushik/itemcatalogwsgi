from . import routes
from flask import render_template,\
	session as appsession
from models import CategoryModel

@routes.route('/')
def Home():
	'''
	home page: display category list & latest items added (10)
	'''

	# fetch all categories
	categories = CategoryModel.get_categories()

	return render_template('home.html', categories=categories, appsession=appsession)