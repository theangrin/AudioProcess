from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.String(45), primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.username

    def __init__(self, id):
        self.id = id

    def delete(self):
        self.is_delete = 1
