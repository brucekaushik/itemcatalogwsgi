from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, User, Catalog, Category, Item

# Connect to Database and create database session
engine = create_engine('postgresql://itemcatalog:itemcatalog@localhost/itemcatalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# delete all users
session.query(User).delete()
session.commit()

# delete all catalogs
session.query(Catalog).delete()
session.commit()

# delete all Categories
session.query(Category).delete()
session.commit()

# delete all items
session.query(Item).delete()
session.commit()

# add a catalog
catalog = Catalog(id=1, name='default')
session.add(catalog)
session.commit()

# add a user
user = User(id=1, name='admin', email='kaushik@qbeck.com')
session.add(user)
session.commit()

# add category
category1 = Category(id=1, name='Martial Arts', catalog_id=1, user_id=1)
session.add(category1)
session.commit()

# add category
category2 = Category(id=2, name='Magic', catalog_id=1, user_id=1)
session.add(category2)
session.commit()

# add category
category3 = Category(id=3, name='Origami', catalog_id=1, user_id=1)
session.add(category3)
session.commit()

# add category
category4 = Category(id=4, name='Dance', catalog_id=1, user_id=1)
session.add(category4)
session.commit()

# add category
category5 = Category(id=5, name='Adventure Sports', catalog_id=1, user_id=1)
session.add(category5)
session.commit()

# add item
item1 = Item(name="Boxing Gloves",
             description="These look stylish for sure!",
             category_id=1,
             catalog_id=1,
             user_id=1)
session.add(item1)
session.commit()

# add item
item2 = Item(name="Puching Bag",
             description="You cant hit people, but you can hit these!!",
             category_id=1,
             catalog_id=1,
             user_id=1)
session.add(item2)
session.commit()

# add item
item3 = Item(name="Head Gear",
             description="Use this or go dizzy",
             category_id=1,
             catalog_id=1,
             user_id=1)
session.add(item3)
session.commit()

# add item
item4 = Item(name="Hand Wrap",
             description="Use this or break your joints!",
             category_id=1,
             catalog_id=1,
             user_id=1)
session.add(item4)
session.commit()

# add item
item5 = Item(name="Mouth Guard",
             description="Do you think you look good without the front teeth?",
             category_id=1,
             catalog_id=1,
             user_id=1)
session.add(item5)
session.commit()

# add item
item6 = Item(name="Speed Bag",
             description="This does not move speedly, you should make it!",
             category_id=1,
             catalog_id=1,
             user_id=1)
session.add(item6)
session.commit()
