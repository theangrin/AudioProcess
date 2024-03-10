import os

from flask import request

from app import db
from app.work import work_bp
from app.work.worker import Worker
from app.work.model import Work
from app.work.utils import save_media, make_json_response


worker = Worker()


@work_bp.route("/upload", methods=["POST"])
def upload_file():
    session_id = request.form.get("session_id")
    file = request.files.get("media_file")

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
