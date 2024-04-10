import os

from flask import request, send_file
from flask_cors import CORS

from app import db
from app.work import work_bp
from app.work.worker import worker
from app.work.model import Work
from app.work.utils import save_media, make_json_response

from config import FrontEndConfig

CORS(
    work_bp,
    resources={r"/*": {"origins": FrontEndConfig.FRONTEND_URL}},
    allow_headers="session-id",
)


@work_bp.route("/upload_media", methods=["POST"])
def upload_file():
    session_id = request.headers.get("session-id")
    file = request.files.get("file")

    if not file:
        return make_json_response({"ok": False, "msg": "上传文件为空"}, 400)

    file_type = file.mimetype[: file.mimetype.index("/")]
    if file_type not in ["audio", "video"]:
        return make_json_response({"ok": False, "msg": "不支持的文件类型"}, 400)

    file_ext = os.path.splitext(file.filename)[-1]
    file_path = save_media(file, session_id + file_ext, file_type)

    work = Work(session_id=session_id, file_path=file_path, file_type=file_type)
    db.session.add(work)
    db.session.commit()

    worker.add_task(session_id, file_path, file_type)

    return make_json_response({"ok": True}, 200)


@work_bp.route("/get_media", methods=["GET"])
def get_media():
    session_id = request.headers.get("session-id")
    work = Work.query.filter_by(session_id=session_id).first()
    return send_file(work.file_path)


@work_bp.route("/get_detail", methods=["GET"])
def get_detail():
    session_id = request.headers.get("session-id")
    work = Work.query.filter_by(session_id=session_id).first()
    return make_json_response(work.detail, 200)


@work_bp.route("/get_markdown", methods=["GET"])
def get_markdown():
    session_id = request.headers.get("session-id")
    work = Work.query.filter_by(session_id=session_id).first()
    return make_json_response({"data": work.markdown}, 200)
