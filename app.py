from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, abort)

from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Collection, Category, Link

import secret
import forms

app = Flask(__name__)
Bootstrap(app)

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


@app.route('/links/collection/select/', methods=['GET', 'POST'])
def select_collection():
    """Redirect to show_category_links based on collection selected
        in dropwdown"""
    selected_coll_path = request.form['select-coll']
    print "in select_collection " + selected_coll_path
    return redirect(url_for('show_category_links',
                             collection=selected_coll_path))


@app.route('/links/<collection>/')
@app.route('/links/<collection>/<category>/')
def show_category_links(collection, category=''):
    """Render the links page for selected collection and category"""
    try:
        selected_coll = session.query(Collection).filter_by(path = collection).one()
    except:
        abort(404)
    # Get the selected category or set a default category if no category in path.
    if len(category) > 0:
        try:
            selected_cat = session.query(Category).filter_by(path=category, coll_id=selected_coll.coll_id).one()
        except:
            abort(404)
    else:
        selected_cat = session.query(Category).filter_by(coll_id=selected_coll.coll_id).order_by(Category.cat_id).first()
    categories = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
    if categories.count() >= 1:
        links = session.query(Link).filter_by(cat_id=selected_cat.cat_id)
    else:
        links = None
    collections = session.query(Collection) # Needed for sidebar
    return render_template('links.html', categories=categories,
                                         collection=collection,
                                         links=links,
                                         selected_coll=selected_coll,
                                         selected_cat=selected_cat,
                                         collections=collections)


@app.route('/links/<collection>/edit/', methods=['GET', 'POST'])
def edit_collection(collection):
    """Edit a Link Collection"""
    form = forms.EditCollectionForm()
    collections = session.query(Collection) # Needed for sidebar
    try:
        selected_coll = session.query(Collection).filter_by(path=collection).one()
    except:
        abort(404)
    if request.method == 'POST':
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
            return redirect(url_for('index'))
        else:
            return render_template('collectionedit.html',
                                    selected_coll=selected_coll,
                                    form=form,
                                    collections=collections)
    else:
        # Populate description field from database when method is GET.
        # Description gets updated here since it is a TextArea; name is updated
        # in the template.
        form.description.data = selected_coll.description
        return render_template('collectionedit.html',
                                selected_coll=selected_coll,
                                collections=collections,
                                form=form)


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
        collections = session.query(Collection) # Needed for sidebar
        return render_template('collectiondelete.html',
                                collection=selected_coll,
                                cats=cats,
                                collections=collections)


@app.route('/links/collection/new/', methods=['GET', 'POST'])
def new_collection():
    """Add a New Collection"""
    form = forms.NewCollectionForm()
    if request.method == 'POST':
        new_coll = Collection(name = request.form['name'],
                              description = request.form['description'],
                              path = request.form['path'])
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
                form.path.errors.append("Path must be unique!")
    collections = session.query(Collection) # Needed for sidebar
    return render_template('collectionnew.html',
                            form=form,
                            collections=collections)


@app.route('/links/<collection>/<category>/edit/', methods=['GET', 'POST'])
def edit_category(collection, category):
    """Edit a Category"""
    form = forms.EditCategoryForm()
    try:
        selected_coll = session.query(Collection).filter_by(path=collection).one()
        selected_cat = (
            session.query(Category).filter_by(
                                        path=category,
                                        coll_id=selected_coll.coll_id).one())
    except:
        abort(404)
    if request.method == 'POST':
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
            return redirect(url_for('show_category_links', collection=collection, category=category))
    else:
        # Populate description field from database when method is GET.
        # Description gets updated here since it is a TextArea; name is updated
        # in the template.
        form.description.data = selected_cat.description
    # Both collections and categories are needed for sidebar
    categories = (
        session.query(Category).filter_by(coll_id=selected_coll.coll_id))
    collections = session.query(Collection)
    return render_template('categoryedit.html', selected_coll=selected_coll,
                                                selected_cat=selected_cat,
                                                categories=categories,
                                                collections=collections,
                                                form=form)


@app.route('/links/<collection>/<category>/delete/', methods=['GET', 'POST'])
def delete_category(collection, category):
    """Delete a Category"""
    try:
        selected_coll = session.query(Collection).filter_by(path=collection).one()
        selected_cat = (
            session.query(Category).filter_by(
                                        path=category,
                                        coll_id=selected_coll.coll_id).one())
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
    # Both categories and collections are needed for sidebar
    categories = session.query(Category).filter_by(
                                            coll_id=selected_coll.coll_id)
    collections = session.query(Collection)
    return render_template('categorydelete.html', selected_coll=selected_coll,
                                                  selected_cat=selected_cat,
                                                  categories=categories,
                                                  links=links,
                                                  collections=collections)


@app.route('/links/<collection>/category/new/', methods=['GET', 'POST'])
def new_category(collection, previous_cat=''):
    """Add a New Category"""
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

        if form.validate_on_submit():
            # Check if the path already exists here instead of forms.py
            # to simplify forms.py by not having database logic in it.
            try:
                db_cat = (
                    session.query(Category).filter_by(
                                    path=new_cat.path,
                                    coll_id=selected_coll.coll_id).one())
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
                form.path.errors.append("Path must be unique!")
    # Both categories and collections are needed for sidebar
    categories = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
    collections = session.query(Collection)
    return render_template('categorynew.html',
                                selected_coll=selected_coll,
                                previous_cat=previous_cat,
                                selected_cat=previous_cat,
                                categories=categories,
                                collections=collections,
                                form=form)


@app.route('/links/<collection>/<category>/<link_id>/edit/', methods=['GET', 'POST'])
def edit_link(collection, category, link_id):
    """Edit a Link"""
    form = forms.EditLinkForm()
    try:
        selected_coll = session.query(Collection).filter_by(
                                                    path=collection).one()
        selected_cat = (
            session.query(Category).filter_by(
                                        path=category,
                                        coll_id=selected_coll.coll_id).one())
        selected_link = (
            session.query(Link).filter_by(link_id=link_id,
                                          cat_id=selected_cat.cat_id).one())
    except:
        abort(404)
    if request.method == 'POST':
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
            return redirect(url_for('show_category_links', collection=collection, category=category))
    else:
        # Populate description field from database when method is GET.
        # Description gets updated here since it is a TextArea;
        # name and url are updated in the template.
        form.description.data = selected_link.description
    # Both categories and collections are needed for sidebar
    categories = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
    collections = session.query(Collection)
    return render_template('linkedit.html', selected_link=selected_link,
                                            selected_cat=selected_cat,
                                            selected_coll=selected_coll,
                                            categories=categories,
                                            collections=collections,
                                            form=form)


@app.route('/links/<collection>/<category>/<link_id>/delete/', methods=['GET', 'POST'])
def delete_link(collection, category, link_id):
    """Delete a Link"""
    try:
        selected_coll = session.query(Collection).filter_by(
                                                    path=collection).one()
        selected_cat = (
            session.query(Category).filter_by(
                                       path=category,
                                       coll_id=selected_coll.coll_id).one())
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
        return redirect(url_for('show_category_links', collection=collection,
                                                       category=category))
    # Both categories and collections are needed for sidebar
    categories = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
    collections = session.query(Collection)
    return render_template('linkdelete.html', selected_coll=selected_coll,
                                              selected_cat=selected_cat,
                                              selected_link=selected_link,
                                              categories=categories,
                                              collections=collections)


@app.route('/links/<collection>/<category>/link/new/', methods=['GET', 'POST'])
def new_link(collection, category):
    """Add a New Link"""
    form = forms.NewLinkForm()
    try:
        selected_coll = session.query(Collection).filter_by(
                                                    path=collection).one()
        selected_cat = (
            session.query(Category).filter_by(
                                        path=category,
                                        coll_id = selected_coll.coll_id).one())
    except:
        abort(404)
    if request.method == 'POST':
        new_link= Link(name = request.form['name'],
                       url = request.form['url'],
                       description = request.form['description'],
                       submitter = 'example@example.com', # WILL CHANGE WHEN AUTH IMPLEMENTED
                       cat_id = selected_cat.cat_id,
                       coll_id = selected_coll.coll_id)
        if form.validate_on_submit():
            session.add(new_link)
            session.commit()
            flash("New link added!")
            return redirect(url_for('show_category_links',
                                      collection=collection,
                                      category=category))
    # Both categories and collections are needed for sidebar
    categories = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
    collections = session.query(Collection)
    return render_template('linknew.html',
                            collection=collection,
                            category=category,
                            selected_coll=selected_coll,
                            selected_cat=selected_cat,
                            categories=categories,
                            collections=collections,
                            form=form)


if __name__ == '__main__':
    app.secret_key = secret.SECRET_KEY
    app.debug = True
    app.run(host='0.0.0.0', port=5000)