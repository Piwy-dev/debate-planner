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
        return render_template('/{}/home.html'.format(lang))
    
    db.init_app(app)

    with app.app_context():
        db.init_db()

    return app
