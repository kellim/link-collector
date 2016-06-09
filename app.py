from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, abort)
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Collection, Category, Link

import secret

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
    if categories.count() > 1:
        links = session.query(Link).filter_by(cat_id=selected_category.cat_id)
    else:
        links = None
    return render_template('links.html', categories=categories, collection=collection,
                           links=links, selected_category=selected_category)


@app.route('/links/<collection>/edit/', methods=['GET', 'POST'])
def edit_collection(collection):
    """Edit a Link Collection"""
    selected_coll = session.query(Collection).filter_by(path=collection).one()
    if request.method == 'POST':
        if 'cancel-btn' in request.form:
            flash('Edit Collection cancelled!')
        else:
            coll_name = request.form['coll-name']
            coll_desc = request.form['coll-desc']
            if (selected_coll.name != coll_name
                or selected_coll.description != coll_desc):
                if selected_coll.name != coll_name:
                    selected_coll.name = coll_name
                if selected_coll.description != coll_desc:
                    selected_coll.description = coll_desc
                session.add(selected_coll)
                session.commit()
                flash('Collection has been edited!')
            else:
                flash('No change was made to collection!')
        return redirect(url_for('index'))
    else:
        return render_template('collectionedit.html', collection=selected_coll)


@app.route('/links/<collection>/delete/', methods=['GET', 'POST'])
def delete_collection(collection):
    """Delete a Link Collection"""
    selected_coll = session.query(Collection).filter_by(path=collection).one()
    cats = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
    if request.method == 'POST':
        if 'cancel-btn' in request.form:
            flash('Delete Collection cancelled!')
        else:
            if selected_coll != []:
                # Delete the Collection's categories and associated links first.
                for cat in cats:
                    links = session.query(Link).filter_by(cat_id=cat.cat_id)
                    for link in links:
                        session.delete(link)
                        session.commit()

                    session.delete(cat)
                    session.commit()

                session.delete(selected_coll)
                session.commit()
                flash('Collection has been deleted!')
        return redirect(url_for('index'))
    else:
        return render_template('collectiondelete.html', collection=selected_coll, cats=cats)


@app.route('/links/collection/new', methods=['GET', 'POST'])
def new_collection():
    if request.method == 'POST':
        new_coll = Collection(name = request.form['coll-name'],
                              description = request.form['coll-desc'],
                              path = request.form['coll-path'])
        if 'cancel-btn' in request.form:
            flash('Adding new Collection cancelled!')
        else:
            session.add(new_coll)
            session.commit()
            flash("New collection created!")
        return redirect(url_for('index'))
    else:
        return render_template('collectionnew.html')

@app.route('/links/<collection>/<category>/edit/')
def edit_category(collection, category):
    """Edit a Category"""
    return render_template('categoryedit.html', collection=collection, category=category)


@app.route('/links/<collection>/<category>/delete/')
def delete_category(collection, category):
    """Delete a Category"""
    return render_template('categorydelete.html', collection=collection, category=category)


@app.route('/links/<collection>/<category>/<link>/edit/')
def edit_link(collection, category, link):
    """Edit a Link"""
    return render_template('linkedit.html', collection=collection, category=category, link=link)


@app.route('/links/<collection>/<category>/<link>/delete/')
def delete_link(collection, category, link):
    """Delete a Link"""
    return render_template('linkdelete.html', collection=collection, category=category, link=link)


if __name__ == '__main__':
    app.secret_key = secret.SECRET_KEY
    app.debug = True
    app.run(host='0.0.0.0', port=5000)