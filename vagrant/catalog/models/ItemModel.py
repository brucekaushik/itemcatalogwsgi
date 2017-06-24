from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, exc
from sqlalchemy.orm import scoped_session
from catalog.dbsetup import Base, User, Catalog, Category, Item
from catalog.models import CatalogModel
from flask import session as appsession
from catalog import catalogvars

# Connect to Database and create database session
engine = create_engine('postgresql://itemcatalog:itemcatalog@localhost/itemcatalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)


def get_item(item_name, category_id):
	catalog_id = CatalogModel.get_catalog_id()
	item = session.query(Item).filter_by(name=item_name, 
				catalog_id=catalog_id,
				category_id=category_id).first()
	return item

def get_item_by_id(item_id):
	item_id = int(item_id)
	item = session.query(Item).filter_by(id=item_id).first()
	return item

def get_lastest_items():
	catalog_id = CatalogModel.get_catalog_id()
	items = session.query(Item).filter_by(catalog_id=catalog_id).order_by(Item.id.desc()).limit(5)
	return items

def get_user_items(user_id):
	user_id = int(user_id)
	catalog_id = CatalogModel.get_catalog_id()
	items = session.query(Item).filter_by(catalog_id=catalog_id, user_id=user_id).all()
	return items


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


def edit_item(item_id, item_name, item_description, category_id):
	item = get_item_by_id(item_id)
	if not item:
		return False

	item.name = item_name
	item.description = item_description
	item.category_id = item.category_id

	try:
		session.commit()
	except:
		session.rollback()
		return False

	return item

def delete_item(item_id):
	item = get_item_by_id(item_id)
	if not item:
		return False

	session.delete(item)

	try:
		session.commit()
	except:
		session.rollback()
		return False

	return item
