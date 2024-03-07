from datetime import datetime

from app import db


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    detail = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, detail,file_path,file_name):
        self.user_id = user_id
        self.detail = detail
        self.file_path=file_path
        self.file_name=file_name

    def delete(self):
        self.is_delete = 1
