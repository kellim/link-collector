from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Collection, Category, Link

engine = create_engine('sqlite:///links.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

coll1 = Collection(title="Python", description="Resources for learning Python and related technologies", path="python")
session.add(coll1)
session.commit()

coll2 = Collection(title="JavaScript", description="Resources for learning JavaScript and related technologies", path="javascript")
session.add(coll2)
session.commit()

print("Added items to the database!")