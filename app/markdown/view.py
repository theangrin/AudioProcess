from flask import request, flash, jsonify

from app import db
from app.markdown import markdown_bp
from app.markdown.model import Markdown
from app.result.model import Result

"""获取md文件"""


@markdown_bp.route('/markdowm/download', methods=['PUT'])
def update_markdown():
    id = request.form['id']
    file = request.form['file']
    # 数据校验
    if not id and not file:
        flash("请求参数为空")
        return "error"
    # 数据库记录信息
    markdown = Markdown.query.filter_by(id=id).first()
    markdown.file_name = file

    db.session.commit()
    return jsonify({'id': markdown.id, 'detail': result.detail})


"""更新md文件"""


@markdown_bp.route('/markdowm/update', methods=['PUT'])
def update_markdown():
    id = request.form['id']
    file = request.form['file']
    # 数据校验
    if not id and not file:
        flash("请求参数为空")
        return "error"
    # 数据库记录信息
    result = Result.query.filter_by(id=id).first()
    result.detail = detail

    db.session.commit()
    return jsonify({'id': result.id, 'detail': result.detail})
