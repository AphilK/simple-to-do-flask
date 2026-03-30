import sqlite3
from datetime import datetime, timedelta

import click
from flask import current_app, g

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

    # Ensure database migrations are run
    with app.app_context():
        ensure_db()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def ensure_db():
    db = get_db()
    db.execute(
        'CREATE TABLE IF NOT EXISTS user ('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' username TEXT UNIQUE NOT NULL,'
        ' password TEXT NOT NULL'
        ')'
    )
    db.execute(
        'CREATE TABLE IF NOT EXISTS sprint ('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' author_id INTEGER NOT NULL,'
        ' name TEXT NOT NULL,'
        ' description TEXT,'
        ' start_date DATE NOT NULL,'
        ' end_date DATE NOT NULL,'
        ' status TEXT DEFAULT "active",'
        ' created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
        ' FOREIGN KEY (author_id) REFERENCES user (id)'
        ')'
    )
    db.execute(
        'CREATE TABLE IF NOT EXISTS task ('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' author_id INTEGER NOT NULL,'
        ' created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
        ' title TEXT NOT NULL,'
        ' body TEXT NOT NULL,'
        ' status TEXT DEFAULT "Started",'
        ' sprint_id INTEGER,'
        ' FOREIGN KEY (author_id) REFERENCES user (id),'
        ' FOREIGN KEY (sprint_id) REFERENCES sprint (id)'
        ')'
    )
    # Add status column to existing tables if it doesn't exist
    try:
        db.execute('ALTER TABLE task ADD COLUMN status TEXT DEFAULT "Started"')
    except sqlite3.OperationalError as e:
        if 'duplicate column name' not in str(e).lower():
            pass
    # Add sprint_id column to existing tables if it doesn't exist
    try:
        db.execute('ALTER TABLE task ADD COLUMN sprint_id INTEGER')
    except sqlite3.OperationalError as e:
        if 'duplicate column name' not in str(e).lower():
            pass
    db.commit()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Sprint helper functions
def get_current_sprint(user_id):
    """Get or create the current active sprint for a user."""
    db = get_db()
    today = datetime.now().date()

    # Check if there's an active sprint
    sprint = db.execute(
        'SELECT * FROM sprint WHERE author_id = ? AND status = "active" AND end_date >= ?',
        (user_id, today)
    ).fetchone()

    if sprint:
        return sprint

    # Create a new sprint if none exists
    start_date = today
    end_date = today + timedelta(days=14)

    # Calculate sprint number
    all_sprints = db.execute(
        'SELECT COUNT(*) as count FROM sprint WHERE author_id = ?',
        (user_id,)
    ).fetchone()
    sprint_number = all_sprints['count'] + 1

    db.execute(
        'INSERT INTO sprint (author_id, name, start_date, end_date, status)'
        ' VALUES (?, ?, ?, ?, ?)',
        (user_id, f'Sprint {sprint_number}', start_date, end_date, 'active')
    )
    db.commit()

    # Return the newly created sprint
    return db.execute(
        'SELECT * FROM sprint WHERE author_id = ? AND start_date = ?',
        (user_id, start_date)
    ).fetchone()


def get_sprint(sprint_id):
    """Get a sprint by ID."""
    return get_db().execute(
        'SELECT * FROM sprint WHERE id = ?',
        (sprint_id,)
    ).fetchone()


def get_all_sprints(user_id):
    """Get all sprints for a user, ordered by start_date descending."""
    return get_db().execute(
        'SELECT * FROM sprint WHERE author_id = ? ORDER BY start_date DESC',
        (user_id,)
    ).fetchall()


def complete_sprint(sprint_id):
    """Complete a sprint and archive finished tasks."""
    db = get_db()

    # Mark sprint as completed
    db.execute(
        'UPDATE sprint SET status = ? WHERE id = ?',
        ('completed', sprint_id)
    )

    # Archive finished tasks (update status to 'Archived' or create archive table)
    # For now, we'll just mark sprint as completed
    db.commit()