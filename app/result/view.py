import os
from datetime import datetime
from urllib.parse import urlparse, unquote

import requests
import soundfile
from flask import request, flash, jsonify
from werkzeug.utils import secure_filename

from app import db
from app.algorithms import ASR
from app.result import analyze_bp
from app.result.model import Result
from app.user.view import judge_user


@analyze_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"result": "success"})


# 临时保存音频
def save_audio(file, file_name):
    data, samplerate = soundfile.read(file)

    current_path = os.getcwd()
    audio_package = os.path.join(current_path, 'audio')
    if not os.path.exists(audio_package):
        os.mkdir(audio_package)

    current_time = datetime.now().strftime('%Y-%m-%d')
    time_package = os.path.join(audio_package, current_time)
    if not os.path.exists(time_package):
        os.mkdir(time_package)

    # 确保文件名是安全的
    safe_filename = secure_filename(file_name)

    # 完整的文件路径
    full_path = os.path.join(time_package, safe_filename)

    soundfile.write(full_path, data, samplerate)

    print(full_path)
    return full_path


"""文心一言：获取详细结果"""


# TODO 服务器相关
@analyze_bp.route("/wx/detail", methods=["GET"])
def wx_detail():
    file_path = request.form["path"]
    user_id = request.form["hash_string"]
    # 数据校验
    if not file_path:
        flash("请求参数为空")
        return "error"

    # 下载音频文件
    response = requests.get(file_path)

    # 确保请求成功
    if response.status_code != 200:
        flash("音频下载失败")
        return "error"

    # 临时保存音频
    file_name = os.path.basename(unquote(urlparse(file_path).path))
    with open(file_name, 'wb') as file:
        file.write(response.content)
        file_path = save_audio(file, file_name)

        # 音频文件分析
        asr = ASR()
        detail = asr(file_path)

    # 更新数据库
    result = Result(user_id, detail, file_name)
    db.session.add(result)
    db.session.commit(result)

    return jsonify({"id": result.id, "detail": result.detail})


"""网站：获取详细结果"""


@analyze_bp.route("/result/detail", methods=["POST"])
def get_detail():
    # 获取用户信息
    user_id = request.headers.get('user_id')
    # 获取音频文件
    file = request.files.get('audioFile')

    print(request.files)

    # 数据校验
    if not file:
        flash("请求参数为空")
        return "error"
    # 临时保存音频
    file_path = save_audio(file, file.filename)

    asr = ASR()
    detail = asr(file_path)

    # 数据库记录信息
    result = Result(judge_user(user_id), detail, file_path, file.filename)
    db.session.add(result)
    db.session.commit()

    return jsonify({"id": result.id, "detail": result.detail})


"""网站：修改详细结果"""


@analyze_bp.route("/result/detail/update", methods=["PUT"])
def update_detail():
    result_id = request.form.get("result_id")
    detail = request.form.get('detail')
    print(detail, result_id)
    # 数据校验
    if not detail or not result_id:
        flash("请求参数为空")
        return "error"
    # 数据库记录信息
    result = Result.query.filter_by(id=result_id).first()
    result.detail = detail

    db.session.commit()

    return "success"
