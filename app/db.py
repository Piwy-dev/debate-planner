"""
This module contains all functions that communicates with the database.
"""
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
import click
from datetime import datetime


def get_db():
    """
    Get the database connection if it exists, otherwise create it.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    Close the database connection if it exists.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initialize the database.
    """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    

def init_app(app):
    """
    Register the database functions with the Flask app.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_topics():
    """
    Get all topics from the database, and order them by number of votes and date (newest first).
    """
    db = get_db()
    topics = db.execute(
        'SELECT * FROM topics ORDER BY votes DESC, created_at DESC'
    ).fetchall()
    # Convert to list of dicts
    topics = [dict(topic) for topic in topics]
    return topics


def add_topic(title: str, content: str, username: int):
    """
    Add a topic to the database.

    Args:
    - `title` - The title of the topic.
    - `content` - The content of the topic.
    - `username` - The id of the user who created the topic.
    """
    db = get_db()
    db.execute(
        'INSERT INTO topics (title, content, username) VALUES (?, ?, ?)',
        (title, content, username)
    )
    db.commit()


def update_topic_votes(topic_id: str, add_votes: int):
    """
    Change the votes of a post.

    Args:
    - `topic_id` - The id of the post to add a like to.
    - `add_votes` - The new number of votes to add to the post.
    """
    db = get_db()
    db.execute(
        'UPDATE topics SET votes = ? WHERE topic_id = ?',
        (add_votes, topic_id)
    )
    db.commit()


def get_previous_vote_type(username: str, topic_id: int):
    """
    Get the type of vote that a user has already made on a post.

    Args:
    - `username` - The username of the user.
    - `topic_id` - The id of the post.

    Returns:
    - `1` if the user has upvoted the post, `-1` if the user has downvoted the post, otherwise `0`.
    """
    db = get_db()
    vote = db.execute(
        'SELECT * FROM votes WHERE username = ? AND topic_id = ?',
        (username, topic_id)
    ).fetchone()
    if vote is None:
        return 0
    else:
        vote = dict(vote)
        return int(vote['vote_type'])
    

def get_topic_votes(topic_id: int):
    """
    Get the number of votes of a post.

    Args:
    - `topic_id` - The id of the post.

    Returns:
    - The number of votes of the post.
    """
    db = get_db()
    topic = db.execute(
        'SELECT * FROM topics WHERE topic_id = ?',
        (topic_id,)
    ).fetchone()
    topic = dict(topic)
    return int(topic['votes'])


def add_vote(username: str, topic_id: int, vote_type: int):
    """
    Add a vote to a post.

    Args:
    - `username` - The username of the user who voted.
    - `topic_id` - The id of the post to add a vote to.
    - `vote_type` - `1` if the user upvoted the post, `-1` if the user downvoted the post, otherwise `0`.
    """
    db = get_db()
    db.execute(
        'INSERT INTO votes (username, topic_id, vote_type) VALUES (?, ?, ?)',
        (username, topic_id, vote_type)
    )
    db.commit()


def check_user(username: str, password: str):
    """
    Check if the username and password are correct.

    Args:
    - `username` - The username to check.
    - `password` - The password to check.

    Returns:
    - `True` if the username and password are correct, otherwise `False`.
    """
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()
    if user is None:
        return False
    else:
        return True
    

def add_user(username: str, password: str):
    """
    Add a user to the database.

    Args:
    - `username` - The username of the user.
    - `password` - The password of the user.
    """
    db = get_db()
    db.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, password)
    )
    db.commit()


def check_username(username: str):
    """
    Check if the username is already in use.

    Args:
    - `username` - The username to check.

    Returns:
    - `True` if the username is already in use, otherwise `False`.
    """
    if username == 'logged_in':
        return True
    
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    if user is None:
        return False
    else:
        return True


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    CLI command to initialize the database.
    """
    init_db()
    click.echo('Initialized the database.')