import os
from flask import *


def create_app(test_config=None):
    """
    Create and configure the app.
    """
    app = Flask(__name__, instance_relative_config=True)

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

    return app
