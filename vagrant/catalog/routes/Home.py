from . import routes
from flask import render_template,\
    session as appsession
from catalog.models import CategoryModel,\
    ItemModel


@routes.route('/')
def Home():
    '''
    home page: display category list & latest items added (10)
    '''

    # fetch all categories
    categories = CategoryModel.get_categories()

    # fetch latest items
    items = ItemModel.get_lastest_items()

    return render_template('home.html',
                           categories=categories,
                           items=items,
                           appsession=appsession)
