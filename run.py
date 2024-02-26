"""启动文件"""
from app import create_app
# import pgvector


app = create_app()

if __name__ == '__main__':
    app.run(debug=True,port=5173)
