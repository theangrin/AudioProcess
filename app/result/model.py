from datetime import datetime

from app import db


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    detail = db.Column(db.Text, nullable=False)
    audio_file = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, detail, audio_file):
        self.user_id = user_id
        self.detail = detail
        self.audio_file = audio_file

    def delete(self):
        self.is_delete = 1
