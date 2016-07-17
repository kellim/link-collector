import os
import sys
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        Boolean, create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    provider = Column(String(8), nullable=False)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    is_admin = Column(Boolean, nullable=False)


class Collection(Base):
    __tablename__ = 'collection'

    coll_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(130))
    submit_date = Column(DateTime, default=func.now())
    path = Column(String(50), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name':         self.name,
            'description':  self.description,
            'path':         self.path
        }


class Category(Base):
    __tablename__ = 'category'

    cat_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200))
    submit_date = Column(DateTime, default=func.now())
    path = Column(String(50), nullable=False)
    coll_id = Column(Integer, ForeignKey('collection.coll_id'))
    collection = relationship(Collection)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name':          self.name,
            'description':   self.description,
            'path':          self.path
        }


class Link(Base):
    __tablename__ = 'link'

    link_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(200), nullable=False)
    description = Column(String(300))
    submit_date = Column(DateTime, default=func.now())
    cat_id = Column(Integer, ForeignKey('category.cat_id'))
    category = relationship(Category)
    coll_id = Column(Integer, ForeignKey('collection.coll_id'))
    collection = relationship(Collection)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id':           self.link_id,
            'name':         self.name,
            'url':          self.url,
            'description':  self.description,
        }


engine = create_engine('postgresql:///links')

Base.metadata.create_all(engine)
