import json
import os
from datetime import datetime

from flask import make_response

from werkzeug.utils import secure_filename


def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


def save_media(file, file_name, file_type):
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
