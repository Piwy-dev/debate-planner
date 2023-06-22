"""
This module contains all functions that communicates with the database.
"""
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
import click
import os
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
        'SELECT id_topic, title, content, created_at, updated_at, votes FROM topics'
        #' FROM topics t JOIN users u ON t.id_user = u.id_user'
        ' ORDER BY votes DESC, created_at DESC'
    ).fetchall()
    # Convert the topics to a list of dictionaries.
    topics = [dict(topic) for topic in topics]
    return topics


def add_topic(title: str, content: str):
    """
    Add a topic to the database.

    Args:
    - `title` - The title of the topic.
    - `content` - The content of the topic.
    """
    db = get_db()
    id_user = 1 # TODO: Get the user id from the session.
    db.execute(
        'INSERT INTO topics (title, content, id_user) VALUES (?, ?, ?)',
        (title, content, id_user)
    )
    db.commit()


def update_post_votes(post_id: str, up: bool, remove: bool):
    """
    Change the votes of a post.

    Args:
    - `post_id` - The id of the post to add a like to.
    - `up`- `True` if the user is upvoting, otherwise `False`.
    - `remove`- If `True`, remove a vote, otherwise add a vote.
    """
    db = get_db()
    if remove:
        if up:
            db.execute(
                'UPDATE posts SET votes = votes - 1 WHERE id = ?',
                (post_id,)
            )
        else:
            db.execute(
                'UPDATE posts SET votes = votes + 1 WHERE id = ?',
                (post_id,)
            )
    else:
        if up:
            db.execute(
                'UPDATE posts SET votes = votes + 1 WHERE id = ?',
                (post_id,)
            )
        else:
            db.execute(
                'UPDATE posts SET votes = votes - 1 WHERE id = ?',
                (post_id,)
            )


def update_post_dislikes(post_id: str, dislike: bool):
    """
    Add or remove a dislike to a post.

    Args:
    - `post_id` - The id of the post to add a dislike to.
    - `param dislike`- If `True`, add a dislike, otherwise remove a dislike.
    """
    db = get_db()
    if dislike:
        db.execute(
            'UPDATE posts SET dislikes = dislikes + 1 WHERE id = ?',
            (post_id,)
        )
    else:
        db.execute(
            'UPDATE posts SET dislikes = dislikes - 1 WHERE id = ?',
            (post_id,)
        )
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    CLI command to initialize the database.
    """
    init_db()
    click.echo('Initialized the database.')