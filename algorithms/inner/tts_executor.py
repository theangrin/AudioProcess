from paddlespeech.cli.tts.infer import TTSExecutor


class TTS:
    def __init__(self):
        self.tts = TTSExecutor()

    def __call__(self, text: str, output: str):
        # tts(text="你好世界", output="output.wav")
        self.tts(text=text, output=output)
