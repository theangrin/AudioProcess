from flask import Blueprint
from werkzeug.utils import redirect

from app.user.model import User

# user_bp = Blueprint('user', __name__)
# @user_bp.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"
# @user_bp.route('/login', methods=['POST'])
# def login():
#     # # 检查用户是否已经登录
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('index'))
#     if request.method == 'POST':
#         # 所有插件拿到后token都会在header里的Authrization字段传入插件
#         user = User.query.filter_by(token=request.form['Authrization']).first()
#         if user and user.token == request.form['Authrization']:
#             login_user(user)
#         else:
#             flash('Invalid username or password')
#     return render_template('detail.html')
# coding:   utf-8
# 作者(@Author):   Messimeimei
# 创建时间(@Created_time): 2023/1/6 11:39

"""登录的视图函数"""
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user
from . import login
from .model import User
from app import login_manager


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


@login.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "GET":
        return render_template('index.html')


@login.route('/register', methods=['GET', 'POST'])
def register():
    # 如果请求为post
    if request.method == 'POST':
        count = request.form.get('count')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        print(count, password)
        from app import db
        if password == repassword:
            user = User(count, password)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return '注册成功'
        else:
            return '两次密码不一致'
    # 请求为get
    return render_template('register.html')


@login.route('/', methods=['GET', 'POST'])
@login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        count = request.form['count']
        password = request.form['password']
        print(password)
        if not count or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = User.query.filter_by(count=count).first()
        if not user:
            flash("用户不存在")
            return redirect(url_for('login.login'))
        if count == user.count and user.check_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            print("登录成功")
            return redirect(url_for('login.index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('templates.login'))  # 重定向回登录页面
    return render_template('login.html')
