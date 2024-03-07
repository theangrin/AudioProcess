"""启动文件"""

from app import create_app

# import pgvector


app = create_app()

if __name__ == '__main__':
    # 配置一个密钥用于签名会话数据
    app.config['SECRET_KEY'] = 'this_is_a_secret_key@yujie'
    # 设置会话过期时间（以秒为单位）
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 小时

    # app.run(host='localhost',debug=True, port=4523)
    app.run(debug=True, port=4523)
