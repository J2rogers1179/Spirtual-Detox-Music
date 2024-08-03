import sqlite3
import click
from flask import current_app, g

def get_db():
    # Check if a database connection already exists
    if 'db' not in g:
        try:
            # Create a new database connection
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            # Set row factory to return rows as dictionaries
            g.db.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            # Log the error and re-raise to handle it higher up if necessary
            current_app.logger.error(f"Failed to connect to the database: {e}")
            raise e
    return g.db

def close_db(e=None):
    # Remove the database connection from g
    db = g.pop('db', None)
    if db is not None:
        try:
            db.close()
        except sqlite3.Error as e:
            # Log the error when closing the database connection
            current_app.logger.error(f"Failed to close the database connection: {e}")

def init_db():
    # Get the current database connection
    db = get_db()
    
    # Execute the schema script to set up the database
    with current_app.open_resource('schema.sql') as f:
        try:
            db.executescript(f.read().decode('utf8'))
        except sqlite3.Error as e:
            # Handle errors that occur during the initialization of the database
            current_app.logger.error(f"Failed to initialize the database: {e}")
            raise e

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    try:
        init_db()
        click.echo("Initialized the database")
    except Exception as e:
        click.echo(f"Failed to initialize the database: {e}")

def init_app(app):
    # Register the close_db function to run on application context teardown
    app.teardown_appcontext(close_db)
    # Add the init_db_command to the Flask CLI commands
    app.cli.add_command(init_db_command)