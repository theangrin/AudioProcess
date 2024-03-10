from app import db


class Work(db.Model):
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    session_id = db.Column(db.VARCHAR(16), nullable=False)
    file_path = db.Column(db.VARCHAR(64), nullable=False)
    file_type = db.Column(db.VARCHAR(8), nullable=False)
    status = db.Column(db.INT, nullable=False, default=0)
    detail = db.Column(db.JSON, nullable=True)

    def __init__(self, session_id: str, file_path: str, file_type: str) -> None:
        self.session_id = session_id
        self.file_path = file_path
        self.file_type = file_type
