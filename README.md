# Link Collector

## About
Link Collector is a multi-user bookmarking web app built with Flask, a Python Microframework.<br> 
**DEMO:** http://links.pythonanywhere.com

### Important Terms: Collections, Categories and Links
In the app, links are contained in categories, and categories are all part of a more general collection. For instance, you might have a collection called <em>Recipes</em>, and within that collection you have categories like <em>Breakfast</em>, <em>Entrees</em>, and <em>Desserts</em>. You would then add links to breakfast recipes in the <em>Breakfast</em> category, and links to desserts in the <em>Desserts</em> category, etc.

## Run the Project Locally

### Initial Steps for setting up this Repo
* Setup Vagrant on your local machine. See https://www.udacity.com/wiki/ud197/install-vagrant for instructions. Please note that when running the virtual machine, do not follow those instructions exactly. Instead, run the virtual machine from the `link-collector` directory since there is a config file in that directory for this project.
* Download this repo as `link-collector` to your local machine and put it in the `vagrant` directory.
* Rename the file `secret.py.config` in the `link-collector` directory to `secret.py`.
* Edit `secret.py` and enter your own secret key of randomly generated characters as the value for the variable `SECRET_KEY`.

### Setup Steps for Google+ Login
* Create your own Google Web Application project at [console.developers.google.com](https://console.developers.google.com) using `OAuth Client ID` for credentials.
* Add `http://localhost:5000` under Authorized JavaScript Origins 
* Add these Authorized Redirect URIs:
 * `http://localhost:5000/gconnect`
 * `http://localhost:5000/login`
 * `http://localhost:5000/gdisconnect`
 * `https://localhost:5000/oauth2callback`
* Download JSON for your web application from Google and name it `client_secrets.json`.
* Add the `client_secrets.json` file to the `link-collector` directory.

<em>See my notes with more detailed instructions at https://docs.google.com/document/d/1bTbW_KyrQ5BOhboJU4fhm6sdMnq7MZuoWPGcBAo8wR0/edit?usp=sharing</em>.

### Setup Steps for Facebook Login
* Create a Facebook Web App at [developers.facebook.com](https://developers.facebook.com).
* Save the `fb_client_secrets.json` skeleton file from 
`https://github.com/udacity/ud330/blob/master/Lesson4/step2/fb_client_secrets.json` to the `link-collector` directory.
* Update `fb_client_secrets.json` with your `App ID` and `Client Secret`.
* Add `Facebook Login` as a `Product`.
* Add `http://localhost:5000/` to the `OAuth redirect URIs` section.

<em>See my notes with more detailed instructions at https://docs.google.com/document/d/1jfBH5okUEHx-MW7WD1in-dOQ2YhCGzeqDySd_E1Kz2g/edit?usp=sharing</em>.

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

### Troubleshooting 
* If you get errors indicating `Flask-WTF`, `Flask-Bootstrap` or `sqlalchemy-utils` are missing, install them from the `link-collector directory` using these commands:
 * `sudo pip install Flask-WTF`
 * `sudo pip install Flask-Bootstrap`
 * `sudo pip install sqlalchemy-utils`
<br><em>Note: It's possible you may not need to run these as sudo on your system</em>

### Testing Admin Functionality
When you login to the site with Google+ or Facebook, you'll be a regular user and can only add links or edit your own links. After you've logged in to the site successfully, you can update the database to make yourself an admin so that you can add, edit, and delete collections and categories.

After you `cd` to the `/vagrant` directory in your vagrant virtual machine:
* Type `psql links` to open the `links` database in `psql`.
* At the `psql` command prompt, type `SELECT * FROM users;` to see what the `user_id` is of the account you want to make an admin. Press `enter` when done.
* At the `psql` command prompt, type `UPDATE users SET is_admin = True WHERE user_id = #;`, replacing # with the `user_id` of the user you wish to make an admin. Press `enter` when done.
* Type `\q` into the `psql` command prompt and press `enter` to exit `psql`.
<hr>
 <em>Please note the app is set to debug mode, which you would not want to use in production. You would also not want to use Flask's built-in server in production.</em>
