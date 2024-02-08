from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.username

    def __init__(self, token):
        self.token = token

    def delete(self):
        self.is_delete = 1

    def update(self,token):
        self.token=token
        self.update_time=datetime.now()