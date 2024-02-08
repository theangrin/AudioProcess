from flask import Blueprint, Flask

analyze = Blueprint("analyze", __name__)
app = Flask(__name__)
app.register_blueprint(analyze)
