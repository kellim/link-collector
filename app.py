from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, abort)
app = Flask(__name__)
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Collection, Category, Link

import secret
import forms

engine = create_engine('sqlite:///links.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    """Render the index page"""
    collections = session.query(Collection)
    return render_template('index.html', collections=collections)

@app.route('/links/')
def link_redirect():
    """Redirect to index page"""
    return redirect(url_for('index'))

@app.route('/links/<collection>/')
@app.route('/links/<collection>/<category>/')
def show_category_links(collection, category=""):
    """Render the links page for selected collection and category"""
    try:
        selected_collection = session.query(Collection).filter_by(path = collection).one()
    except:
        abort(404)
    # Get the selected category or set a default category if no category in path.
    if len(category) > 0:
        try:
            selected_category = session.query(Category).filter_by(path = category, coll_id=selected_collection.coll_id).one()
        except:
            abort(404)
    else:
        selected_category = session.query(Category).filter_by(coll_id=selected_collection.coll_id).order_by(Category.cat_id).first()
    categories = session.query(Category).filter_by(coll_id=selected_collection.coll_id)
    if categories.count() >= 1:
        links = session.query(Link).filter_by(cat_id=selected_category.cat_id)
    else:
        links = None
    return render_template('links.html', categories=categories, collection=collection,
                           links=links, selected_category=selected_category)


@app.route('/links/<collection>/edit/', methods=['GET', 'POST'])
def edit_collection(collection):
    """Edit a Link Collection"""
    form = forms.EditCollectionForm()
    try:
        selected_coll = session.query(Collection).filter_by(path=collection).one()
    except:
        abort(404)
    if request.method == 'POST':
        if 'cancel-btn' in request.form:
            flash('Edit Collection cancelled!')
        else:
            if form.validate_on_submit():
                coll_name = request.form['name']
                coll_desc = request.form['description']
                # Make sure at least one field was changed before updating the
                # database. Also, don't update fields that were not changed.
                # This logic deals with multiple fields so did not add it
                # to forms.py
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
            else:
                # flash('Please fill out both fields.')
                form.description.data = selected_coll.description
                return render_template('collectionedit.html', collection=selected_coll, form=form)
        return redirect(url_for('index'))
    else:
        form.description.data = selected_coll.description
        return render_template('collectionedit.html', collection=selected_coll, form=form)


@app.route('/links/<collection>/delete/', methods=['GET', 'POST'])
def delete_collection(collection):
    """Delete a Link Collection"""
    try:
        selected_coll = session.query(Collection).filter_by(path=collection).one()
    except:
        abort(404)
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


@app.route('/links/collection/new/', methods=['GET', 'POST'])
def new_collection():
    path_unique = True
    form = forms.NewCollectionForm()
    if request.method == 'POST':
        new_coll = Collection(name = request.form['name'],
                              description = request.form['description'],
                              path = request.form['path'])
        if 'cancel-btn' in request.form:
            flash('Adding new Collection cancelled!')
            return redirect(url_for('index'))
        else:
            if form.validate_on_submit():
                # Check if the path already exists here instead of forms.py
                # to simplify forms.py by not having database logic in it.
                try:
                    db_coll = session.query(Collection).filter_by(path=new_coll.path).one()
                except:
                    path = None
                else:
                    path = db_coll.path

                if path != new_coll.path:
                    session.add(new_coll)
                    session.commit()
                    flash("New collection created!")
                    return redirect(url_for('index'))
                else:
                    path_unique = False
            return render_template('collectionnew.html', form=form, path_unique=path_unique)
    else:
        return render_template('collectionnew.html', form=form, path_unique=path_unique)


@app.route('/links/<collection>/<category>/edit/', methods=['GET', 'POST'])
def edit_category(collection, category):
    """Edit a Category"""
    form = forms.EditCategoryForm()
    try:
        coll = session.query(Collection).filter_by(path=collection).one()
        selected_cat = (
            session.query(Category).filter_by(path=category,
                                              coll_id=coll.coll_id).one())
    except:
        abort(404)
    if request.method == 'POST':
        if 'cancel-btn' in request.form:
            flash('Edit Category cancelled!')
        else:
            if form.validate_on_submit():
                cat_name = request.form['name']
                cat_desc = request.form['description']
                # Make sure at least one field was changed before updating the
                # database. Also, don't update fields that were not changed.
                # This logic deals with multiple fields so did not add it
                # to forms.py
                if (selected_cat.name != cat_name
                    or selected_cat.description != cat_desc):
                    if selected_cat.name != cat_name:
                        selected_cat.name = cat_name
                    if selected_cat.description != cat_desc:
                        selected_cat.description = cat_desc
                    session.add(selected_cat)
                    session.commit()
                    flash('Category has been edited!')
                else:
                    flash('No change was made to Category!')
            else:
                return render_template('categoryedit.html', collection=coll, category=selected_cat, form=form)
        return redirect(url_for('show_category_links', collection=collection, category=selected_cat.path))
    else:
        # Populate description field from database when method is GET.
        # Description gets updated here since it is a TextArea; name is updated
        # in the template.
        form.description.data = selected_cat.description
        return render_template('categoryedit.html', collection=coll, category=selected_cat, form=form)


@app.route('/links/<collection>/<category>/delete/', methods=['GET', 'POST'])
def delete_category(collection, category):
    """Delete a Category"""
    try:
        selected_coll = session.query(Collection).filter_by(path=collection).one()
        selected_cat = session.query(Category).filter_by(path=category, coll_id=selected_coll.coll_id).one()
    except:
        abort(404)
    links = session.query(Link).filter_by(cat_id=selected_cat.cat_id)
    if request.method == 'POST':
        if 'cancel-btn' in request.form:
            flash('Delete Category cancelled!')
        else:
            if selected_cat != []:
                # Delete the Category's associated links first.
                for link in links:
                    session.delete(link)
                    session.commit()

                session.delete(selected_cat)
                session.commit()

                flash('Category has been deleted!')
        return redirect(url_for('show_category_links', collection=collection))
    else:
        return render_template('categorydelete.html', collection=selected_coll, category=selected_cat, links=links)


@app.route('/links/<collection>/category/new/', methods=['GET', 'POST'])
def new_category(collection):
    """Add a New Category"""
    path_unique = True
    form = forms.NewCategoryForm()
    try:
        selected_coll = session.query(Collection).filter_by(path=collection).one()
    except:
        abort(404)
    if request.method == 'POST':
        new_cat= Category(name = request.form['name'],
                              description = request.form['description'],
                              path = request.form['path'].lower(),
                              coll_id = selected_coll.coll_id)
        if 'cancel-btn' in request.form:
            flash('Adding new Category cancelled!')
            return redirect(url_for('show_category_links', collection=collection))
        else:
            if form.validate_on_submit():
                try:
                    db_cat = session.query(Category).filter_by(path=new_cat.path, coll_id=selected_coll.coll_id).one()
                except:
                    path = None
                else:
                    path = db_cat.path
                if new_cat.path != path:
                    session.add(new_cat)
                    session.commit()
                    flash("New category created!")
                    return redirect(url_for('show_category_links',
                        collection=collection,
                        category=new_cat.path))
                else:
                    path_unique = False

    return render_template('categorynew.html',
                                collection=collection,
                                form=form,
                                path_unique=path_unique)


@app.route('/links/<collection>/<category>/<link_id>/edit/', methods=['GET', 'POST'])
def edit_link(collection, category, link_id):
    """Edit a Link"""
    form = forms.EditLinkForm()
    try:
        coll = session.query(Collection).filter_by(path=collection).one()
        cat = session.query(Category).filter_by(path=category,
                                                coll_id=coll.coll_id).one()
        selected_link = session.query(Link).filter_by(link_id=link_id, cat_id=cat.cat_id).one()
    except:
        abort(404)
    if request.method == 'POST':
        if 'cancel-btn' in request.form:
            flash('Edit Link cancelled!')
        else:
            if form.validate_on_submit():
                link_name = request.form['name']
                link_url = request.form['url']
                link_desc = request.form['description']
                # Make sure at least one field was changed before updating the
                # database. Also, don't update fields that were not changed.
                # This logic deals with multiple fields so did not add it
                # to forms.py
                if (selected_link.name != link_name
                    or selected_link.url != link_url
                    or selected_link.description != link_desc):
                    if selected_link.name != link_name:
                        selected_link.name = link_name
                    if selected_link.url != link_url:
                        selected_link.url = link_url
                    if selected_link.description != link_desc:
                        selected_link.description = link_desc
                    session.add(selected_link)
                    session.commit()
                    flash('Link has been edited!')
                else:
                    flash('No change was made to Link!')
            else:
                return render_template('linkedit.html', collection=collection, category=category, link=selected_link, form=form)
        return redirect(url_for('show_category_links', collection=collection, category=cat.path))
    else:
        # Populate description field from database when method is GET.
        # Description gets updated here since it is a TextArea; name is updated
        # in the template.
        form.description.data = selected_link.description
        return render_template('linkedit.html', collection=collection, category=category, link=selected_link, form=form)

@app.route('/links/<collection>/<category>/<link_id>/delete/', methods=['GET', 'POST'])
def delete_link(collection, category, link_id):
    """Delete a Link"""
    try:
        coll = session.query(Collection).filter_by(path=collection).one()
        cat = session.query(Category).filter_by(path=category, coll_id=coll.coll_id).one()
        selected_link = session.query(Link).filter_by(link_id=link_id).one()
    except:
        abort(404)
    if request.method == 'POST':
        if 'cancel-btn' in request.form:
            flash('Delete Link cancelled!')
        else:
            session.delete(selected_link)
            session.commit()
            flash('Link has been deleted!')
        return redirect(url_for('show_category_links', collection=collection, category=category))
    else:
        return render_template('linkdelete.html', collection=coll, category=cat, link=selected_link)


@app.route('/links/<collection>/<category>/link/new/', methods=['GET', 'POST'])
def new_link(collection, category):
    form = forms.NewLinkForm()
    try:
        coll = session.query(Collection).filter_by(path=collection).one()
        cat = session.query(Category).filter_by(path=category, coll_id = coll.coll_id).one()
    except:
        abort(404)
    if request.method == 'POST':
        new_link= Link(name = request.form['name'],
                       url = request.form['url'],
                       description = request.form['description'],
                       submitter = 'example@example.com', # WILL CHANGE WHEN AUTH IMPLEMENTED
                       cat_id = cat.cat_id,
                       coll_id = coll.coll_id)
        if 'cancel-btn' in request.form:
            flash('Add new Link cancelled!')
        else:
            if form.validate_on_submit():
                session.add(new_link)
                session.commit()
                flash("New link added!")
                return redirect(url_for('show_category_links',
                                          collection=collection,
                                          category=category))
    return render_template('linknew.html',
                            collection=collection,
                            category=category,
                            form=form)


if __name__ == '__main__':
    app.secret_key = secret.SECRET_KEY
    app.debug = True
    app.run(host='0.0.0.0', port=5000)