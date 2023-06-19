"""
This module contains all functions that communicates with the database.
"""
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
import click
import os


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


def update_post_likes(post_id: str, like: bool):
    """
    Add or remove a like to a post.

    Args:
    - `post_id` - The id of the post to add a like to.
    - `param like`- If `True`, add a like, otherwise remove a like.
    """
    db = get_db()
    if like:
        db.execute(
            'UPDATE posts SET likes = likes + 1 WHERE id = ?',
            (post_id,)
        )
    else:
        db.execute(
            'UPDATE posts SET likes = likes - 1 WHERE id = ?',
            (post_id,)
        )
    db.commit()


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