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


def get_user(email):
    '''
    get user using email
    '''
    user = session.query(User).filter_by(email=email).first()
    return user


def register_user(userinfo):
    '''
    register user in database
    '''
    user = get_user(userinfo['email'])

    if user:
        return user

    reguser = User(name=userinfo['name'], email=userinfo[
        'email'], picture=userinfo['picture'])
    session.add(reguser)

    try:
        session.commit()
    except:
        session.rollback()
        return False

    return reguser
