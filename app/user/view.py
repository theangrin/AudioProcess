import uuid

from flask import jsonify

from . import login_bp

"""登录的视图函数"""
from .model import User
from app import login_manager, db


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


# 临时用户标识
def judge_user(user_id):
    # 检查用户标识符是否已存在，不存在则创建一个新的用户
    user = User.query.filter_by(id=user_id).first()
    if not user:
        user = User(str(uuid.uuid4()))
        db.session.add(user)
        db.session.commit()
    return user.id


"""注册新用户"""


@login_bp.route('/register', methods=['GET'])
def register():
    user = User(str(uuid.uuid4()))
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id})

# @login_bp.route('/index', methods=['GET', 'POST'])
# @login_required
# def index():
#     if request.method == "GET":
#         return render_template('index.html')
#
#
# @login_bp.route('/', methods=['GET', 'POST'])
# @login_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         count = request.form['count']
#         password = request.form['password']
#         print(password)
#         if not count or not password:
#             flash('Invalid input.')
#             return redirect(url_for('login'))
#         user = User.query.filter_by(count=count).first()
#         if not user:
#             flash("用户不存在")
#             return redirect(url_for('login'))
#         if count == user.count and user.check_password(password):
#             login_user(user)  # 登入用户
#             flash('Login success.')
#             print("登录成功")
#             return redirect(url_for('login.index'))  # 重定向到主页
#
#         flash('Invalid username or password.')  # 如果验证失败，显示错误消息
#         return redirect(url_for('templates.login'))  # 重定向回登录页面
#     return render_template('login.html')
