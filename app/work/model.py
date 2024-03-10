from app import db


class Work(db.Model):
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    session_id = db.Column(db.VARCHAR(32), nullable=False)
    file_path = db.Column(db.VARCHAR(128), nullable=False)
    file_type = db.Column(db.VARCHAR(8), nullable=False)
    detail = db.Column(db.JSON, nullable=True)
    markdown = db.Column(db.TEXT, nullable=True)

    def __init__(self, session_id: str, file_path: str, file_type: str) -> None:
        self.session_id = session_id
        self.file_path = file_path
        self.file_type = file_type
