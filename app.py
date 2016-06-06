from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, abort)
app = Flask(__name__)

@app.route('/')
def index():
    """Render the index page"""
    return render_template('index.html')

@app.route('/links/<collection>/')
@app.route('/links/<collection>/<category>/')
def showCategoryLinks(collection, category="default"):
    """Render the links page for selected collection and category"""
    if category == "default":
        category = "set a default category"
    return render_template('links.html', collection =  collection,
                           category= category)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)