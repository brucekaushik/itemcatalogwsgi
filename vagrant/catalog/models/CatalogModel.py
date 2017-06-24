from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from catalog.dbsetup import Base, User, Catalog, Category, Item
from catalog import catalogvars

# Connect to Database and create database session
engine = create_engine('sqlite:///' + catalogvars.database)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)


def get_catalog_id(catalog_name='default'):
    '''
    get catalog id
    '''

    catalog = session.query(Catalog).filter_by(name=catalog_name).first()
    return catalog.id
