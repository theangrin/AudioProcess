from datetime import datetime

from app import db


class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=False)

    def __init__(self, file_name,url):
        self.file_name=file_name
        self.url=url


    def delete(self):
        self.is_delete = 1
