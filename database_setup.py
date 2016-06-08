import os
import sys
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Collection(Base):
    __tablename__ = 'collection'

    coll_id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    submit_date = Column(DateTime, default=func.now())
    path = Column(String(20), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    cat_id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    submit_date = Column(DateTime, default=func.now())
    path = Column(String(20), nullable=False)
    coll_id = Column(Integer, ForeignKey('collection.coll_id'))
    collection = relationship(Collection)


class Link(Base):
    __tablename__ = 'link'

    link_id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    url = Column(String(250), nullable=False)
    description = Column(String(250))
    submitter = Column(String(250), nullable=False)
    submit_date = Column(DateTime, default=func.now())
    cat_id = Column(Integer, ForeignKey('category.cat_id'))
    category = relationship(Category)
    coll_id = Column(Integer, ForeignKey('collection.coll_id'))
    collection = relationship(Collection)


engine = create_engine('sqlite:///links.db')

Base.metadata.create_all(engine)