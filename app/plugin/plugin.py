import json
import secrets
import time

from config import FrontEndConfig

from flask import request, send_file, make_response
from flask_cors import CORS
from flask_sse import sse

from app import db
from app.plugin import plugin_bp
from app.algorithms.ernie import ernie
from app.work.model import Work
from app.work.worker import worker
from app.work.utils import named_tuple_to_json_str

CORS(plugin_bp, resources={r"/*": {"origins": "https://yiyan.baidu.com"}})


def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@plugin_bp.route("/work", methods=["POST"])
def work():
    session_id = request.headers.get("X-Bd-Plugin-Sessionidhash")
    work = Work.query.filter_by(session_id=session_id).first()

    if work is None:
        return make_json_response(
            {
                "data": f"""
[请点击此链接上传音视频文件]({FrontEndConfig.FRONTEND_URL}/upload/{session_id})

上传文件前后请不要刷新文心一言页面。

上传文件后，请以“分析音视频文件。”开头，并写下你想分析的内容，比如：
分析音视频文件。这是一段数学课程视频，请分别总结课程中的各个章节所讲的内容。

若没有具体想分析的内容，可以直接回复“分析音视频文件”。
    """
            }
        )
    else:
        prompt = request.json["prompt"]

        json = None
        while json == None:
            json = named_tuple_to_json_str(worker.get_result(session_id))
            time.sleep(1)

        markdown = ernie(json, prompt)

        work.detail = json
        work.markdown = markdown
        db.session.commit()

        return make_json_response(
            {
                "data": f"""
{markdown}

✨（｡ӧ◡ӧ｡）💫

若要获取详细分析信息，或者想进行更多操作，请点击[此链接]({FrontEndConfig.FRONTEND_URL}/{work.file_type}/{session_id})。
    """
            }
        )


@plugin_bp.route("/logo.png")
def plugin_logo():
    return send_file("plugin/plugin_config/logo.png", mimetype="image/png")


@plugin_bp.route("/ai-plugin.json")
def plugin_manifest():
    host = request.host_url
    with open("app/plugin/plugin_config/ai-plugin.json", encoding="utf-8") as f:
        text = (
            f.read()
            .replace("RANDOM_ID", secrets.token_urlsafe(4))
            .replace("PLUGIN_HOST/", host)
        )
        return text, 200, {"Content-Type": "application/json"}


@plugin_bp.route("/openapi.yaml")
def plugin_api():
    host = request.host_url
    with open("app/plugin/plugin_config/openapi.yaml", encoding="utf-8") as f:
        text = f.read().replace("PLUGIN_HOST/", host)
        return text, 200, {"Content-Type": "text/yaml"}


@plugin_bp.route("/example.yaml")
def plugin_example():
    with open("app/plugin/plugin_config/example.yaml", encoding="utf-8") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}


@plugin_bp.route("/msg_content.yaml")
def plugin_msg_content():
    with open("app/plugin/plugin_config/msg_content.yaml", encoding="utf-8") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}
