from datetime import datetime

from app import db


class Markdown(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result_id = db.Column(db.Integer, nullable=False)
    file = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)

    def __init__(self, file):
        self.file = file

    def delete(self):
        self.is_delete = 1
