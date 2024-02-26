from flask import Flask
from config import BaseConfig
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login_bp'
db = SQLAlchemy()


def register_bp(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    from .user.view import login_bp
    from .result.view import analyze_bp
    app.register_blueprint(login_bp)
    app.register_blueprint(analyze_bp)


def database(app, db):
    """
    初始化数据库
    :param app:
    :return:
    """
    db.init_app(app)
    db.create_all()
    db.session.commit()


def create_app():
    my_app = Flask(__name__)
    with my_app.app_context():
        # app注册蓝图
        register_bp(my_app)
        # app加载配置
        my_app.config.from_object(BaseConfig)
        # 数据库管理对象
        database(my_app, db)
        # 用于登录验证
        login_manager.init_app(my_app)
        login_manager.login_view = 'login_bp.login'
    return my_app