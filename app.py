from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, abort, session as login_session, make_response)
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Collection, Category, Link

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import forms
import random
import string
import httplib2
import json
import requests

import secret

# See https://pythonhosted.org/Flask-WTF/csrf.html
# which mentions views need CSRF protection even
# if they don't have forms.
csrf = CsrfProtect()

app = Flask(__name__)
csrf.init_app(app)
Bootstrap(app)

CLIENT_ID = json.loads(
open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Link Collector"

engine = create_engine('sqlite:///links.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/_del-coll/<collection>')
def index(collection=''):
    """Render the index page"""
    collections = session.query(Collection)
    # If the delete link was clicked, get the selected collection
    # for the delete collection modal
    if len(collection) > 0:
        try:
            selected_coll = session.query(Collection).filter_by(path=collection).one()
        except:
            flash('Unable to delete this collection. Please contact the site admin for assistance.', 'danger')
            return redirect(url_for('index'))
        categories = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
        return render_template('index.html', collections=collections,
                                             selected_coll=selected_coll,
                                             cats=categories)
    return render_template('index.html', collections=collections)


@app.route('/links/')
def link_redirect():
    """Redirect to index page"""
    return redirect(url_for('index'))


@app.route('/about')
def about():
    """Render about page"""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Render contact page"""
    return render_template('contact.html')


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
@app.route('/links/<collection>/<category>/_del-link/<link_id>')
def show_category_links(collection, category='', link_id=0):
    """Render the links page for selected collection and category"""
    try:
        print('getting selected_coll')
        selected_coll = session.query(Collection).filter_by(path = collection).one()
    except:
        print('getting selected_coll abort')
        abort(404)
    # Get the selected category or set a default category if no category in path.
    if len(category) > 0:
        try:
            print('getting selected_cat')
            selected_cat = session.query(Category).filter_by(path=category, coll_id=selected_coll.coll_id).one()
        except:
            print('getting selected_cat abort')
            abort(404)
    else:
        selected_cat = session.query(Category).filter_by(coll_id=selected_coll.coll_id).order_by(Category.cat_id).first()
    # If the delete link was clicked, get the selected link
    # for the delete link modal
    if link_id > 0:
        try:
            print('getting selected_link')
            selected_link = (
                session.query(Link).filter_by(
                                        link_id=link_id,
                                        cat_id=selected_cat.cat_id).one())
        except:
            flash('Unable to delete this link. Please contact the site admin for assistance.', 'danger')
            return redirect(url_for('show_category_links'))
    else:
        selected_link = None
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
                                         selected_link = selected_link,
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
                flash('Collection has been edited!', 'success')
            else:
                flash('No change was made to collection!', 'warning')
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


@app.route('/links/<collection>/delete/', methods=['POST'])
def delete_collection(collection):
    """Delete a Link Collection"""
    try:
        selected_coll = session.query(Collection).filter_by(path=collection).one()
    except:
        flash('Unable to delete this collection. Please contact the site admin for assistance.', 'danger')
        return redirect(url_for('index'))
    cats = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
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
        flash('Collection has been deleted!', 'success')
    else:
        flash('An error has occurred deleting collection', 'danger')
    return redirect(url_for('index'))

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
                flash('New collection created!', 'success')
                return redirect(url_for('index'))
            else:
                form.path.errors.append('Path must be unique!')
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
                flash('Category has been edited!', 'success')
            else:
                flash('No change was made to Category!', 'warning')
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


@app.route('/links/<collection>/<category>/delete/', methods=['POST'])
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
    if selected_cat != []:
        # Delete the Category's associated links first.
        for link in links:
            session.delete(link)
            session.commit()
        session.delete(selected_cat)
        session.commit()
        flash('Category has been deleted!', 'success')
    else:
        flash('An error has occurred deleting category', 'danger')
    return redirect(url_for('show_category_links', collection=collection))


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
                flash('New category created!', 'success')
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
                flash('Link has been edited!', 'success')
            else:
                flash('No change was made to Link!', 'warning')
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
    session.delete(selected_link)
    session.commit()
    flash('Link has been deleted!', 'success')
    return redirect(url_for('show_category_links', collection=collection,
                                                    category=category))


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
            flash('New link added!', 'success')
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


@app.route('/login')
def login():
    """Render Login page"""
    state = ''.join(random.choice
                (string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', CLIENT_ID = CLIENT_ID)


@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Process Google+ account Login"""
    print 'in gconnect'
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h3>Welcome, '
    output += login_session['username']
    output += '!</h3>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'], 'success')
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Logout of Google+ Account"""
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = secret.SECRET_KEY
    app.debug = True
    app.run(host='0.0.0.0', port=5000)