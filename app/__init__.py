import os
from flask import *
from app import db


def create_app(test_config=None):
    """
    Create and configure the app.
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    lang = 'fr'
    
    @app.route("/")
    def index():
        return redirect('/{}/home'.format(lang))
    
    @app.route("/<lang>/home")
    def home(lang):
        topics = db.get_topics()
        # If user is logged in
        if 'logged_in' in session:
            return render_template('/{}/home.html'.format(lang), topics=topics, logged_in=True, username=session['username'])
        return render_template('/{}/home.html'.format(lang), topics=topics, logged_in=False)
    
    @app.route("/<lang>/create-topic", methods=['GET', 'POST'])
    def create_topic(lang):
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            db.add_topic(title, content, session['username'])
            return redirect('/{}/home'.format(lang))

        else:
            # If user is logged in
            if 'logged_in' in session:
                return render_template('/{}/create-topic.html'.format(lang), logged_in=True, username=session['username'])
            # If user is not logged in, redirect to connection page
            return redirect('/{}/connection'.format(lang))

       
    @app.route("/topics/<int:topic_id>/vote/<vote_type>", methods=['POST'])
    def vote_topic(topic_id, vote_type):
        print(topic_id, vote_type)
        if 'logged_in' not in session:
            return redirect('/{}/connection'.format(lang))
        
        if vote_type == 'upvote':
            db.update_topic_votes(topic_id, True, False)
        elif vote_type == 'downvote':
            db.update_topic_votes(topic_id, False, True)
    
        topics = db.get_topics()
        return render_template('/{}/home.html'.format(lang), topics=topics, logged_in=True, username=session['username'])
    
        
    @app.route("/<lang>/connection", methods=['GET', 'POST'])
    def connection(lang):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if db.check_user(username, password):
                session['logged_in'] = True
                session['username'] = username
                return redirect('/{}/home'.format(lang))
            else:
                return render_template('/{}/connection.html'.format(lang), error="Mauvais identifiants")
        return render_template('/{}/connection.html'.format(lang))
        
    @app.route("/<lang>/inscription", methods=['GET', 'POST'])
    def inscription(lang):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not db.check_username(username):
                db.add_user(username, password)
                # TODO: add session and connect user
                return redirect('/{}/home'.format(lang))
            else:
                return render_template('/{}/inscription.html'.format(lang), error="Nom d'utilisateur déjà utilisé")
        else:
            return render_template('/{}/inscription.html'.format(lang))
        
    @app.route("/<lang>/deconnection")
    def deconnection(lang):
        session.pop('logged_in', None)
        session.pop('username', None)
        return redirect('/{}/home'.format(lang))
    
    db.init_app(app)

    with app.app_context():
        db.init_db()

    return app
