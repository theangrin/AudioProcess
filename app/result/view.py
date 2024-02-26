from flask import request, flash, jsonify
from flask_login import current_user

from algorithms.asr import ASR
from app import db
from app.result import analyze_bp
from app.result.model import Result
from app.user.model import User

"""文心一言：获取详细结果"""


@analyze_bp.route('/wx/detail', methods=['GET'])
def wx_detail():
    authrization = request.form['hash_string']
    path = request.form['path']
    # 数据校验
    if not authrization and not path:
        flash("请求参数为空")
        return "error"
    # 用户验证
    user = User.query.filter_by(token=authrization).first()
    if not user:
        flash("用户不存在")
        return "error"

    # TODO 异步处理1
    asr = ASR()
    detail = asr(path)

    # 数据库记录信息
    result = Result(user.id, detail, path)
    db.session.add(result)
    db.session.commit(result)

    return jsonify({'id': result.id, 'detail': result.detail})


"""获取详细结果"""


@analyze_bp.route('/detail/<path:path>', methods=['GET'])
def get_detail():
    # 获取路径参数
    path = request.args.get('path')

    # 数据校验
    if not path:
        flash("请求参数为空")
        return "error"

    # TODO 异步处理2
    asr = ASR()
    detail = asr(path)

    # 数据库记录信息
    result = Result(current_user.id, detail, path)
    db.session.add(result)
    db.session.commit()

    return jsonify({'id': result.id, 'detail': result.detail})



"""修改详细结果"""


@analyze_bp.route('/detail/update', methods=['PUT'])
def update_detail():
    id =request.form['result_id']
    detail = request.form['detail']
    # 数据校验
    if not detail:
        flash("请求参数为空")
        return "error"
    # 数据库记录信息
    result =Result.query.filter_by(id=id).first()
    result.detail = detail

    db.session.commit()

    return jsonify({'id': result.id, 'detail': result.detail})
