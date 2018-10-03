# Link Collector

Link Collector is a multi-user bookmarking web app built with Flask, a Python Microframework where users can login with their Google account. Admin users can create categories and collections, and non-admin users can add links and update or delete their own links. Admins can edit or delete any links.

In the app, links are contained in categories, and categories are all part of a more general collection. For instance, you might have a collection called <em>Recipes</em>, and within that collection you have categories like <em>Breakfast</em>, <em>Entrees</em>, and <em>Desserts</em>. You would then add links to breakfast recipes in the <em>Breakfast</em> category, and links to desserts in the <em>Desserts</em> category, etc.

## Demo

Check out the demo at https://links.pythonanywhere.com

## Run the Project in a Local Development Environment

### Initial Steps for setting up this Repo
* Setup Vagrant on your local machine. See https://www.udacity.com/wiki/ud197/install-vagrant for instructions. Please note that when running the virtual machine, do not follow those instructions exactly. Instead, run the virtual machine from the `link-collector` directory since there is a config file in that directory for this project.
* Download this repo as `link-collector` to your local machine and put it in the `vagrant` directory.
* Rename the file `secret.py.config` in the `link-collector` directory to `secret.py`.
* Edit `secret.py` and enter your own secret key of randomly generated characters as the value for the variable `SECRET_KEY`.

### Setup Steps for Google+ Login
* Create your own Google Web Application project at [console.developers.google.com](https://console.developers.google.com) using `OAuth Client ID` for credentials.
* Add these Authorized Redirect URIs (you'd want to change these to appropriate URLs using https for your server if using in production.):
 * `http://localhost:5000/gconnect`
 * `http://localhost:5000/login`
 * `http://localhost:5000/gdisconnect`
 * `https://localhost:5000/oauth2callback`
* Download JSON for your web application from Google and name it `client_secrets.json`.
* Add the `client_secrets.json` file to the `link-collector` directory.

### Run the Project
* In the `link-collector` directory run these commands:
 * `vagrant up`
 * `vagrant ssh`
 * `cd /vagrant`
* Then, run these Python files:
 * `python models.py` - creates the database
 * `python add_test_data.py` - adds test data to database
 * `python app.py` - runs app using Flask's built-in server
* In a web browser, go to `http://localhost:5000` to use the app.

### Testing Admin Functionality
When you login to the site with Google, you'll be a regular user and can only add links or edit your own links. After you've logged in to the site successfully, you can update the database to make yourself an admin so that you can add, edit, and delete collections and categories.

After you `cd` to the `/vagrant` directory in your vagrant virtual machine:
* Type `psql links` to open the `links` database in `psql`.
* At the `psql` command prompt, type `SELECT * FROM users;` to see what the `user_id` is of the account you want to make an admin. Press `enter` when done.
* At the `psql` command prompt, type `UPDATE users SET is_admin = True WHERE user_id = #;`, replacing # with the `user_id` of the user you wish to make an admin. Press `enter` when done.
* Type `\q` into the `psql` command prompt and press `enter` to exit `psql`.

 <em>Please note the app is set to debug mode, which you would not want to use in production. You would also not want to use Flask's built-in server in production.</em>
