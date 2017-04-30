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


def get_item(item_name, category_id):
	catalog_id = CatalogModel.get_catalog_id()
	item = session.query(Item).filter_by(name=item_name, 
				catalog_id=catalog_id,
				category_id=category_id).first()
	return item


def add_item(item_name, item_description, category_id):
	catalog_id = CatalogModel.get_catalog_id()

	item = get_item(item_name, category_id)
	if item:
		return False

	newitem = Item(name=item_name,
				description=item_description,
				category_id=category_id,
				catalog_id=catalog_id,
				user_id=appsession['user_id'])
	session.add(newitem)

	try:
		session.commit()
	except:
		session.rollback()
		return False

	return newitem

