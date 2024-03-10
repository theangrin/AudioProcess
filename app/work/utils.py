import json
import os
from datetime import datetime

from flask import Response, make_response

from werkzeug.utils import secure_filename


def make_json_response(data, status_code=200) -> Response:
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


def save_media(file, file_name: str, file_type: str) -> str:
    """return: save path"""

    path = os.getcwd()

    if file_type == "audio":
        path = os.path.join(path, "audio")
        if not os.path.exists(path):
            os.mkdir(path)
    elif file_type == "video":
        path = os.path.join(path, "video")
        if not os.path.exists(path):
            os.mkdir(path)

    current_time = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(path, current_time)
    if not os.path.exists(path):
        os.mkdir(path)

    safe_filename = secure_filename(file_name)
    path = os.path.join(path, safe_filename)

    file.save(path)

    return path


def named_tuple_to_dict(obj):
    if isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return dict(zip(obj._fields, (named_tuple_to_dict(item) for item in obj)))
    elif isinstance(obj, list):
        return [named_tuple_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: named_tuple_to_dict(value) for key, value in obj.items()}
    else:
        return obj


def named_tuple_to_json_str(obj):
    return json.dumps(named_tuple_to_dict(obj))
