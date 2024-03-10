import subprocess
from pathlib import Path


def extract_audio_from_video(video_file: str):
    """return: audio path"""

    path = Path(video_file)
    parent = str(path.parent)
    name = path.stem

    subprocess.call(
        [
            "ffmpeg",
            "-i",
            video_file,
            "-vn",
            "-acodec",
            "copy",
            f"{parent}/{name}.aac",
        ],
    )

    return f"{parent}/{name}.aac"


if __name__ == "__main__":
    extract_audio_from_video("./video/zh.mp4")
