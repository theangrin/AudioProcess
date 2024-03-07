from flask import request, send_file, make_response
from flask_cors import CORS
import json

from app.plugin import plugin_bp

CORS(plugin_bp, resources={r"/*": {"origins": "https://yiyan.baidu.com"}})


def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@plugin_bp.route("/upload", methods=["POST"])
def upload():
    sessionidhash = request.headers.get("X-Bd-Plugin-Sessionidhash")
    return make_json_response(
        {
            "data": f"[请点击此链接上传文件]({request.host_url}upload_file?sessionidhash={sessionidhash})"
        }
    )


@plugin_bp.route("/work", methods=["POST"])
def work():
    sessionidhash = request.headers.get("X-Bd-Plugin-Sessionidhash")
    is_chine = request.json["is_chinese"]
    prompt = request.json["prompt"]
    return make_json_response(
        {
            "ui_data": {
                "log": "[测试样例]",
                "content": """
**会议总结**
* **主题回顾**：讨论公司下一阶段的发展战略和市场布局。
* **技术进展**：技术团队在人工智能和大数据领域取得显著进展，研发了智能推荐系统，优化了云计算和分布式存储，降低运营成本。
* **市场策略**：利用智能推荐系统提升用户体验，与合作伙伴共享技术资源，定制化开发新产品和服务。
* **财务评估**：建议制定详细的预算和财务计划，以确保投资回报。
* **结论与行动计划**：将建议整合到公司发展战略中，制定实施计划，紧密合作推动公司发展。
                """,
                "link": "请打开链接以详细编辑文本：test link",
            }
        }
    )


@plugin_bp.route("/logo.png")
def plugin_logo():
    return send_file("app/plugin/plugin_config/logo.png", mimetype="image/png")


@plugin_bp.route("/ai-plugin.json")
def plugin_manifest():
    host = request.host_url
    with open("app/plugin/plugin_config/ai-plugin.json", encoding="utf-8") as f:
        text = f.read().replace("PLUGIN_HOST/", host)
        return text, 200, {"Content-Type": "application/json"}


@plugin_bp.route("/ui.json")
def plugin_ui():
    with open("app/plugin/plugin_config/ui.json", encoding="utf-8") as f:
        text = f.read()
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
