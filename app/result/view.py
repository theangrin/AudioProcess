import os
from datetime import datetime
from urllib.parse import urlparse, unquote

import requests
import soundfile
from flask import request, flash, jsonify
from werkzeug.utils import secure_filename

from app import db
from app.algorithms import ASR
from app.algorithms.ernie import ernie
from app.plugin.plugin import make_json_response
from app.result import analyze_bp
from app.result.model import Result
from app.user.view import judge_user
from config import FrontEndConfig

from flask_cors import CORS

CORS(analyze_bp, resources={r"/*": {"origins": "https://yiyan.baidu.com"}})


@analyze_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"result": "success"})


# 临时保存音频
def save_audio(file, file_name):
    data, samplerate = soundfile.read(file)

    current_path = os.getcwd()
    audio_package = os.path.join(current_path, "audio")
    if not os.path.exists(audio_package):
        os.mkdir(audio_package)

    current_time = datetime.now().strftime("%Y-%m-%d")
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


@analyze_bp.route("/wx/detail", methods=["GET"])
def wx_detail():
    file_path = request.form["file"]
    user_id = request.form["session-id"]
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
    with open(file_name, "wb") as file:
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


# 受文心一言本身限制，接口合并
@analyze_bp.route("/work", methods=["POST"])
def work():
    session_id = request.headers.get("X-Bd-Plugin-Sessionidhash")
    result_id = request.headers.get("result_id")
    print(session_id)
    # session_id = "test"
    # result_id = 0
    if not result_id:
        print("no result_id")
        # 如果没有结果，则为第一次调用接口，需要先上传音频文件
        return make_json_response(
            {
                "data": f"""
[请点击此链接上传音视频文件]({FrontEndConfig.FRONTEND_URL}/upload/{session_id})

上传文件前后请不要刷新文心一言页面。

上传文件后，请以“分析音视频文件。”开头，并写下你想分析的内容，比如：
分析音视频文件。这是一段数学课程视频，请分别总结课程中的各个章节所讲的内容。

若没有具体想分析的内容，可以直接回复“分析音视频文件”。"""
            }
        )
    else:
        # 分析结果并返回概要信息和result_id
        # result = Result.query.filter_by(user_id=session_id).first()
        result = Result.query.filter_by(id=result_id).first()

        prompt = request.json["prompt"]

        # 文心一言分析概要
        result.summary = ernie(result.detail, prompt)

        db.session.commit()

        return make_json_response(
            {
                "data": f"""
{result.summary}

✨（｡ӧ◡ӧ｡）💫

若要获取详细分析信息，或者想进行更多操作，请点击[此链接]({FrontEndConfig.FRONTEND_URL}/{work.file_type}/{session_id}/{result.id})。
    """
            }
        )


"""网站：获取详细结果"""


@analyze_bp.route("/result/detail", methods=["POST"])
def get_detail():
    # 获取用户信息
    session_id = request.headers.get("session_id")
    # 获取音频文件
    file = request.files.get("file")
    print('sessionid:',session_id)


    print(request.files)

    # 数据校验
    if not file:
        flash("请求参数为空")
        return "error"
    # 临时保存音频
    file_path = save_audio(file, file.filename)

    # 调用算法
    asr = ASR()
    detail = asr(file_path)

    # 数据库记录信息
    result = Result(judge_user(session_id), detail, file_path, file.filename)
    db.session.add(result)
    db.session.commit()
    print(detail)

    return jsonify({"id": result.id, "detail": result.detail})


"""网站：修改详细结果"""


@analyze_bp.route("/result/detail/update", methods=["PUT"])
def update_detail():
    result_id = request.form.get("result_id")
    detail = request.form.get("detail")
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
