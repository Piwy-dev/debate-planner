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
        return render_template('/{}/home.html'.format(lang), topics=topics)
    
    @app.route("/<lang>/create-topic", methods=['GET', 'POST'])
    def create_topic(lang):
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            db.add_topic(title, content)
            return redirect('/{}/home'.format(lang))
        else:
            return render_template('/{}/create-topic.html'.format(lang))
        
    @app.route("/<lang>/connection", methods=['GET', 'POST'])
    def connection(lang):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if db.check_user(username, password):
                return redirect('/{}/home'.format(lang))
            else:
                return render_template('/{}/connection.html'.format(lang), error="Mauvais identifiants")
        else:
            return render_template('/{}/connection.html'.format(lang))
        
    @app.route("/<lang>/inscription", methods=['GET', 'POST'])
    def inscription(lang):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if db.check_username(username):
                db.add_user(username, password)
                return redirect('/{}/home'.format(lang))
            else:
                return render_template('/{}/inscription.html'.format(lang), error="Nom d'utilisateur déjà utilisé")
        else:
            return render_template('/{}/inscription.html'.format(lang))
    
    db.init_app(app)

    with app.app_context():
        db.init_db()

    return app
