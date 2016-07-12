from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, abort, session as login_session, make_response)
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base, Collection, Category, Link

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


# Helper Functions

def createUser(login_session):
    """Add logged in user to database"""
    # Adapted from Udacity's Authentication & Authorization: OAuth Course
    # www.udacity.com/course/authentication-authorization-oauth--ud330
    try:
        newUser = User(name=login_session['username'], provider=login_session['provider'], email=login_session[
           'email'], picture=login_session['picture'], is_admin=False)
        session.add(newUser)
        session.commit()
    except:
        return None
    user = session.query(User).filter_by(
                                email=login_session['email'],
                                provider=login_session['provider']).one()
    return user.user_id


def getUserInfo(user_id):
    """Look up user in database by user id and return record"""
    # Code from Udacity's Authentication & Authorization: OAuth Course
    # www.udacity.com/course/authentication-authorization-oauth--ud330
    user = session.query(User).filter_by(user_id=user_id).one()
    return user


def getUserID(email, provider):
    """Look up user in database by email and provider, then return record"""
    # Adapted from Udacity's Authentication & Authorization: OAuth Course
    # www.udacity.com/course/authentication-authorization-oauth--ud330
    try:
        user = session.query(User).filter_by(email=email,
                                             provider=provider).one()
        return user.user_id
    except:
        return None


def is_site_admin(user_id):
    """Return True if user is an admin for site"""
    try:
        user = getUserInfo(user_id)
    except:
        return False
    return user.is_admin


@app.route('/_auth-to-del')
def is_auth_to_deleteJSON():
    """Returns True in JSON if user is authorized to delete item"""
    is_admin = is_site_admin(login_session['user_id'])
    # If user is on the links page, there will be one link argument.
    # Check if logged in user is the one who submitted the link.
    if request.args:
        link_id = request.args.get('link', 0, type=int)
        selected_link = session.query(Link).filter_by(link_id=link_id).one()
        is_link_submitter = selected_link.user_id == login_session['user_id']
    else:
        # is_link_submitter is False if user is on the index page listing
        # collections; there are no links to handle on index page.
        is_link_submitter = False
    return jsonify(is_auth_to_delete = is_link_submitter or is_admin)


@app.route('/')
@app.route('/_del-coll/<collection>')
def index(collection=''):
    """Render the index page"""
    collections = session.query(Collection)
    try:
        is_admin = is_site_admin(login_session['user_id'])
    except:
        # False if user is not logged in
        is_admin = False
    # If the delete link was clicked, get the selected collection
    # for the delete collection modal
    if len(collection) > 0:
        if 'username' not in login_session:
            flash('You must login before deleting a collection.', 'warning')
            return redirect(url_for('login'))
        try:
            selected_coll = session.query(Collection).filter_by(path=collection).one()
        except:
            flash('Unable to delete collection. Please contact the site admin for assistance.', 'danger')
            return redirect(url_for('index'))
        if not is_admin:
            flash('You do not have permission to perform that task. Please '
                  'contact site admin for assistance.', 'danger')
        categories = session.query(Category).filter_by(
                                                coll_id=selected_coll.coll_id)
        return render_template('index.html', collections=collections,
                                             selected_coll=selected_coll,
                                             cats=categories,
                                             is_admin = is_admin)
    else:
        return render_template('index.html', collections=collections,
                                             is_admin = is_admin)


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


@csrf.exempt
@app.route('/links/collection/select/', methods=['GET', 'POST'])
def select_collection():
    """Redirect to show_category_links based on collection selected
        in dropwdown"""
    selected_coll_path = request.form['select-coll']
    return redirect(url_for('show_category_links',
                             collection=selected_coll_path))


@app.route('/links/<collection>/')
@app.route('/links/<collection>/<category>/')
@app.route('/links/<collection>/<category>/_del-link/<link_id>')
def show_category_links(collection, category='', link_id=0):
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
    try:
        is_admin = is_site_admin(login_session['user_id'])
    except:
        # False if user is not logged in
        is_admin = False
    # If the delete link was clicked, get the selected link
    # for the delete link modal
    if link_id > 0:
        if 'username' not in login_session:
            flash('You must login before deleting a link.', 'warning')
            return redirect(url_for('login'))
        try:
            selected_link = (
                session.query(Link).filter_by(
                                        link_id=link_id,
                                        cat_id=selected_cat.cat_id).one())
        except:
            flash('Unable to delete this link. Please contact the site admin for assistance.', 'danger')
            return redirect(url_for('show_category_links'))
        is_link_submitter = login_session['user_id'] == selected_link.user_id
        if not (is_link_submitter or is_admin):
            flash('You do not have permission to perform that task. Please '
                  'contact site admin for assistance.', 'danger')
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
                                         collections=collections,
                                         is_admin= is_admin)


@app.route('/links/<collection>/edit/', methods=['GET', 'POST'])
def edit_collection(collection):
    """Edit a Link Collection"""
    if 'username' not in login_session:
        flash('You must login before editing a collection.', 'warning')
        return redirect(url_for('login'))
    if is_site_admin(login_session['user_id']):
        form = forms.EditCollectionForm()
        collections = session.query(Collection) # Needed for sidebar
        try:
            selected_coll = session.query(Collection).filter_by(
                                                        path=collection).one()
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
            # Description gets updated here since it is a TextArea; name is
            # updated in the template.
            form.description.data = selected_coll.description
            return render_template('collectionedit.html',
                                    selected_coll=selected_coll,
                                    collections=collections,
                                    form=form)
    else:
        # User is not admin, so redirect instead of showing form
        flash('An error occurred accessing Edit Collection page. Please '
              'contact site admin for assistance.', 'danger')
        return redirect(url_for('index'))


@app.route('/links/<collection>/delete/', methods=['POST'])
def delete_collection(collection):
    """Delete a Link Collection"""
    if 'username' not in login_session:
        flash('You must login before deleting a collection.', 'warning')
        return redirect(url_for('login'))
    if is_site_admin(login_session['user_id']):
        try:
            selected_coll = session.query(Collection).filter_by(
                                                        path=collection).one()
        except:
            flash('Unable to delete this collection. Please contact the site '
                  'admin for assistance.', 'danger')
            return redirect(url_for('index'))
        cats = session.query(Category).filter_by(
                                            coll_id=selected_coll.coll_id)
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
    else:
        flash('You do not have permission to perform that task. Please '
              'contact site admin for assistance.', 'danger')
    return redirect(url_for('index'))


@app.route('/links/collection/new/', methods=['GET', 'POST'])
def new_collection():
    """Add a New Collection"""
    if 'username' not in login_session:
        flash('You must login before adding a new collection.', 'warning')
        return redirect(url_for('login'))
    if is_site_admin(login_session['user_id']):
        form = forms.NewCollectionForm()
        if request.method == 'POST':
            new_coll = Collection(name = request.form['name'],
                                  description = request.form['description'],
                                  path = request.form['path'])
            if form.validate_on_submit():
                # Check if the path already exists here instead of forms.py
                # to simplify forms.py by not having database logic in it.
                try:
                    db_coll = session.query(Collection).filter_by(
                                                    path=new_coll.path).one()
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
    else:
        # User is not admin, so redirect instead of showing form
        flash('An error occurred accessing New Collection page. Please '
              'contact site admin for assistance.', 'danger')
        return redirect(url_for('index'))

@app.route('/links/<collection>/<category>/edit/', methods=['GET', 'POST'])
def edit_category(collection, category):
    """Edit a Category"""
    if 'username' not in login_session:
        flash('You must login before editing a category.', 'warning')
        return redirect(url_for('login'))
    if is_site_admin(login_session['user_id']):
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
    else:
        flash('An error occurred accessing Edit Category page. Please '
              'contact site admin for assistance.', 'danger')
        return redirect(url_for('show_category_links', collection=collection,
                                                       category=category))


@app.route('/links/<collection>/<category>/delete/', methods=['POST'])
def delete_category(collection, category):
    """Delete a Category"""
    if 'username' not in login_session:
        flash('You must login before deleting a category.', 'warning')
        return redirect(url_for('login'))
    if is_site_admin(login_session['user_id']):
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
            flash('An error has occurred deleting category.', 'danger')
            return redirect(url_for('show_category_links',
                                        collection=collection,
                                        category=category))
        return redirect(url_for('show_category_links', collection=collection))
    else:
        flash('You do not have permission to perform that task. Please '
              'contact site admin for assistance.', 'danger')
        return redirect(url_for('show_category_links', collection=collection,
                                                           category=category))


@app.route('/links/<collection>/category/new/', methods=['GET', 'POST'])
def new_category(collection, previous_cat=''):
    """Add a New Category"""
    if 'username' not in login_session:
        flash('You must login before adding a new category.', 'warning')
        return redirect(url_for('login'))
    if is_site_admin(login_session['user_id']):
        form = forms.NewCategoryForm()
        try:
            selected_coll = session.query(Collection).filter_by(
                                                        path=collection).one()
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
        categories = session.query(Category).filter_by(
                                                coll_id=selected_coll.coll_id)
        collections = session.query(Collection)
        return render_template('categorynew.html',
                                    selected_coll=selected_coll,
                                    previous_cat=previous_cat,
                                    selected_cat=previous_cat,
                                    categories=categories,
                                    collections=collections,
                                    form=form)
    else:
        flash('An error occurred accessing New Category page. Please '
              'contact site admin for assistance.', 'danger')
        return redirect(url_for('show_category_links', collection=collection))


@app.route('/links/<collection>/<category>/<link_id>/edit/', methods=['GET', 'POST'])
def edit_link(collection, category, link_id):
    """Edit a Link"""
    if 'username' not in login_session:
        flash('You must login before editing a link.', 'warning')
        return redirect(url_for('login'))
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
    is_admin = is_site_admin(login_session['user_id'])
    is_link_submitter = login_session['user_id'] == selected_link.user_id
    if is_link_submitter or is_admin:
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
                return redirect(url_for('show_category_links',
                                            collection=collection,
                                            category=category))
        else:
            # Populate description field from database when method is GET.
            # Description gets updated here since it is a TextArea;
            # name and url are updated in the template.
            form.description.data = selected_link.description
    else:
        flash('An error occurred accessing Edit Link page. Please '
              'contact site admin for assistance.', 'danger')
        return redirect(url_for('show_category_links', collection=collection,
                                                       category=category))
    # Both categories and collections are needed for sidebar
    categories = session.query(Category).filter_by(coll_id=selected_coll.coll_id)
    collections = session.query(Collection)
    return render_template('linkedit.html', selected_link=selected_link,
                                            selected_cat=selected_cat,
                                            selected_coll=selected_coll,
                                            categories=categories,
                                            collections=collections,
                                            form=form)


@app.route('/links/<collection>/<category>/<link_id>/delete/', methods=['POST'])
def delete_link(collection, category, link_id):
    """Delete a Link"""
    if 'username' not in login_session:
        flash('You must login before deleting a link.', 'warning')
        return redirect(url_for('login'))
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
    is_admin = is_site_admin(login_session['user_id'])
    is_link_submitter = login_session['user_id'] == selected_link.user_id
    if is_link_submitter or is_admin:
        session.delete(selected_link)
        session.commit()
        flash('Link has been deleted.', 'success')
    else:
        flash('You do not have permission to perform that task. Please '
              'contact site admin for assistance.', 'danger')
    return redirect(url_for('show_category_links', collection=collection,
                                                    category=category))


@app.route('/links/<collection>/<category>/link/new/', methods=['GET', 'POST'])
def new_link(collection, category):
    """Add a New Link"""
    if 'username' not in login_session:
        flash('You must login before adding a new link.', 'warning')
        return redirect(url_for('login'))
    else:
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
                           cat_id = selected_cat.cat_id,
                           coll_id = selected_coll.coll_id,
                           user_id = login_session['user_id'])
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


# Login and connection/disconnection code adapted from Udacity's
# Authentication & Authorization: OAuth Course
# www.udacity.com/course/authentication-authorization-oauth--ud330
@app.route('/login')
def login():
    """Render Login page"""
    state = ''.join(random.choice
                (string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', CLIENT_ID=CLIENT_ID)


@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Process Google+ account Login"""
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
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'], 'google')
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    if user_id:
        print "login_session at google login: %s" % login_session
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
    else:
        output=''
        output+= '<p>An error occured logging you in.</p>'
        # An error occurred writing to database, but user was already
        # logged in to Google+ and login_session values were populated,
        # so need to disconnect or there will be issues using the site
        # without a user_id.
        disconnect(True)
        flash('An error occurred logging you in. Please contact site admin '
              'for assistance.', 'danger')
        return output


@csrf.exempt
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout.
    # Let's strip out the information before the equals sign in our token.
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # See if user exists
    user_id = getUserID(login_session['email'], 'facebook')
    print "user_id: %s" % user_id
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    if user_id:
        print "login_session at google login: %s" % login_session
        output = ''
        output += '<h3>Welcome, '
        output += login_session['username']

        output += '!</h3>'
        output += '<img src="'
        output += login_session['picture']
        output += (' " style = "width: 100px; height: 100px; '
                   'border-radius: 150px;-webkit-border-radius: 150px;'
                   '-moz-border-radius: 150px;"> ')
        flash("You are now logged in as %s" % login_session['username'],
                                                            'success')
        return output
    else:
        output=''
        output+= '<p>An error occured logging you in.</p>'
        # An error occurred writing to database, but user was already
        # logged in to Google+ and login_session values were populated,
        # so need to disconnect or there will be issues using the site
        # without a user_id.
        disconnect(True)
        flash('An error occurred logging you in. Please contact site admin '
              'for assistance.', 'danger')
        return output


@app.route('/disconnect')
def disconnect(login_failure=False):
    """Disconnect based on login provider"""
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect(True)
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect(True)
            del login_session['facebook_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        print 'login_session after logout: %s ' % login_session
        # Don't show successful log out message when disconnect called
        # because of failure logging in.
        if login_failure == False:
            flash('You have successfully been logged out.', 'success')
    else:
        flash('You were not logged in', 'warning')
    return redirect(url_for('index'))


@app.route('/gdisconnect')
def gdisconnect(called_from_disconnect=False):
    """Logout of Google+ Account"""
    if called_from_disconnect:
        access_token = login_session['access_token']
        if access_token is None:
            response = make_response(
                        json.dumps('Current user not connected.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        if result['status'] != '200':
            # For whatever reason, the given token was invalid.
            response = make_response(
                json.dumps('Failed to revoke token for given user.', 400))
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        flash('Attempt to logout was unsuccessful.', 'danger')
        return redirect(url_for('index'))


@app.route('/fbdisconnect')
def fbdisconnect(called_from_disconnect=False):
    """Logout of Facebook Account"""
    if called_from_disconnect:
        facebook_id = login_session['facebook_id']
        # The access token must be included to successfully logout
        access_token = login_session['access_token']
        url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
        h = httplib2.Http()
        result = h.request(url, 'DELETE')[1]
        return 'You have been logged out.'
    else:
        flash('Attempt to logout was unsuccessful.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = secret.SECRET_KEY
    app.debug = True
    app.run(host='0.0.0.0', port=5000)