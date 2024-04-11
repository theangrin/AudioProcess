import json
import os
from datetime import datetime
from urllib.parse import urlparse, unquote

import requests
import soundfile
from flask import request, flash, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from app import db
from app.algorithms import ASR
from app.algorithms.ernie import ernie
from app.plugin.plugin import make_json_response
from app.result import analyze_bp
from app.result.model import Result

from config import FrontEndConfig

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
    path = '..\\audio\\' + current_time + '\\' + safe_filename

    soundfile.write(full_path, data, samplerate)

    return [full_path, path]


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
    print('work-sessionid:', session_id)
    print('work-resultid:', result_id)
    results = Result.query.filter_by(user_id=session_id).all()
    if not results:
        print("no result")
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
        result = results[-1]
        print(result.id, result.detail)

        prompt = request.json["prompt"]

        # 文心一言分析概要
        result.summary = ernie(pickle.loads(result.detail).full_text, prompt)

        db.session.commit()

        return make_json_response(
            {
                "data": f"""
{result.summary}

✨（｡ӧ◡ӧ｡）💫

若要获取详细分析信息，或者想进行更多操作，请点击[此链接]({FrontEndConfig.FRONTEND_URL}/{result.file_type}/{session_id}/{result.id})。
    """
            }
        )


"""网站：获取详细结果"""


@analyze_bp.route("/result/detail", methods=["POST"])
def result_detail():
    # 获取用户信息
    session_id = request.headers.get("session_id")
    # 获取音频文件
    file = request.files.get("file")
    print('resultdetail-sessionid:', session_id)

    print(request.files)

    # 数据校验
    if not file:
        flash("请求参数为空")
        return "error"
    # 临时保存音频
    file_path = save_audio(file, file.filename)
    full_path = file_path[0]
    relative_path = file_path[-1]
    print('resultdetail-fullpath', file_path)
    print('resultdetail-fullpath', full_path)
    print('resultdetail-relativepath', relative_path)

    # 调用算法
    asr = ASR()
    detail = asr(full_path)

    # 数据库记录信息
    result = Result(session_id, pickle.dumps(detail), relative_path, file.filename, file.mimetype[:file.mimetype.index("/")])
    db.session.add(result)
    db.session.commit()
    print('resultdetail-detail', pickle.dumps(detail))
    print('resultdetail-filetype', result.file_type)

    return jsonify({"id": result.id, "detail": detail})


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


@analyze_bp.route("/get_media/<session_id>/<result_id>", methods=["GET"])
def get_media(session_id, result_id):
    print('getmedia-sessionid:', session_id)
    print('getmedia-resultid:', result_id)

    result = Result.query.filter_by(id=result_id).first()

    print("getmediapath:", result.file_path)
    return send_file(result.file_path)

import pickle
@analyze_bp.route("/get_detail", methods=["GET"])
def get_detail():
    session_id = request.headers.get("session_id")
    result_id = request.headers.get("result_id")
    print('getdetail-sessionid:', session_id)

    result = Result.query.filter_by(id=result_id).first()

    print("getdetail:", result.detail)
    print(pickle.loads(result.detail))
    # return make_json_response(named_tuple_to_json_str(result.detail))
    return jsonify(pickle.loads(result.detail).to_dict())
