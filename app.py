from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, abort)
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Collection, Category, Link

engine = create_engine('sqlite:///links.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    """Render the index page"""
    collections = session.query(Collection)
    return render_template('index.html', collections=collections)


@app.route('/links/<collection>/')
@app.route('/links/<collection>/<category>/')
def show_category_links(collection, category=""):
    """Render the links page for selected collection and category"""
    selected_collection = session.query(Collection).filter_by(path = collection).one()
    # Get the selected category or set a default category if no category in path.
    if len(category) > 0:
        selected_category = session.query(Category).filter_by(path = category, coll_id=selected_collection.coll_id).one()
    else:
        selected_category = session.query(Category).filter_by(coll_id=selected_collection.coll_id).order_by(Category.cat_id).first()
    categories = session.query(Category).filter_by(coll_id=selected_collection.coll_id)
    links = session.query(Link).filter_by(cat_id=selected_category.cat_id)
    return render_template('links.html', categories=categories, collection=collection,
                           links=links, selected_category=selected_category)


@app.route('/links/<collection>/edit')
def edit_collection(collection):
    """Edit a Link Collection"""
    return render_template('collectionedit.html', collection=collection)


@app.route('/links/<collection>/delete')
def delete_collection(collection):
    """Delete a Link Collection"""
    return render_template('collectiondelete.html', collection=collection)



@app.route('/links/<collection>/<category>/edit')
def edit_category(collection, category):
    """Edit a Category"""
    return render_template('categoryedit.html', collection=collection, category=category)


@app.route('/links/<collection>/<category>/delete')
def delete_category(collection, category):
    """Delete a Category"""
    return render_template('categorydelete.html', collection=collection, category=category)


@app.route('/links/<collection>/<category>/<link>/edit')
def edit_link(collection, category, link):
    """Edit a Link"""
    return render_template('linkedit.html', collection=collection, category=category, link=link)


@app.route('/links/<collection>/<category>/<link>/delete')
def delete_link(collection, category, link):
    """Delete a Link"""
    return render_template('linkdelete.html', collection=collection, category=category, link=link)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)