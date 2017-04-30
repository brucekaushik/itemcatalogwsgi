from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, User, Catalog, Category, Item

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_user(email):
    user = session.query(User).filter_by(email=email).first()
    return user


def register_user(userinfo):
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
