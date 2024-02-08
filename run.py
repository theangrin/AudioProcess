"""启动文件"""
from app import create_app
from app.result import analyze

app = create_app()
 
if __name__ == '__main__':
    app.register_blueprint(analyze)
    app.run(debug=True)