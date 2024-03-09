import os

from flask import request

from app import db
from app.algorithms import ASR
from app.work import work_bp
from app.work.model import Work
from app.work.utils import save_media, make_json_response


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

    print(type(file))

    return make_json_response({"ok": True}, 200)

    # asr = ASR()
    # detail = asr(file_path)

    # # 数据库记录信息
    # result = Result(judge_user(user_id), detail, file_path, file.filename)
    # db.session.add(result)
    # db.session.commit()

    # return jsonify({"id": result.id, "detail": result.detail})
