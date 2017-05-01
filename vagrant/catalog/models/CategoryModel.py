from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, exc
from dbsetup import Base, User, Catalog, Category, Item
from models import CatalogModel
from flask import session as appsession

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_categories():
    '''
    get all categories
    '''
    catalog_id = CatalogModel.get_catalog_id()
    categories = session.query(Category).filter_by(catalog_id=catalog_id).all()
    return categories


def get_category(category_name):
    '''
    get category using category name
    '''
    catalog_id = CatalogModel.get_catalog_id()
    category = session.query(Category).filter_by(
        name=category_name, catalog_id=catalog_id).first()
    return category


def get_category_by_id(category_id):
    '''
    get category using category id
    '''
    category_id = int(category_id)
    category = session.query(Category).filter_by(id=category_id).first()
    return category


def add_category(category_name):
    '''
    add category to database
    '''
    catalog_id = CatalogModel.get_catalog_id()

    category = get_category(category_name)
    if category:
        return False

    newcat = Category(name=category_name, catalog_id=catalog_id,
                      user_id=appsession['user_id'])
    session.add(newcat)

    try:
        session.commit()
    except:
        session.rollback()
        return False

    return newcat
