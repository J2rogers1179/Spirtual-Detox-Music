from flask import     Blueprint, flash, g, redirect, render_template, request, session, url_for


# Create a Blueprint for your site routes
site = Blueprint('site', __name__)

@site.route('/')
def index():
    """Render the main homepage."""
    return render_template('page/index.html')

@site.route('/luvell')
def luvell():
    """Render the Luvell profile page."""
    return  render_template('page/luvell.html')

@site.route('/ozlee')
def ozlee():
    """Render the Ozlee profile page."""
    return render_template('page/ozlee.html')
# More routes can be added here if needed