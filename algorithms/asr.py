from collections import namedtuple


class ASR:
    def __init__(self, data_path: str = "./asr/data"):
        self.Char = namedtuple("Char", ["char", "sTime", "eTime", "speaker"])
        self.AsrResult = namedtuple("AsrResult", ["text", "num_speakers", "chars"])

    def __call__(self, audio_file: str) -> tuple:
        return self.AsrResult(
            "你好，世界。",
            1,
            [
                self.Char("你", 0, 1, 0),
                self.Char("好", 1, 2, 0),
                self.Char("世", 2, 3, 0),
                self.Char("界", 3, 4, 0),
            ],
        )
