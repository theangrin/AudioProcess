import os
from collections import namedtuple

from inner.asr_executor import ASRExecutor
from inner.text_executor import TextExecutor
from inner.mfa_executor import MFAExecutor
from inner.utils import text2pinyin

from pyannote.audio import Pipeline


class ASR:
    def __init__(self, data_path: str = "./asr/data"):
        self.data_path = data_path

        self.asr = ASRExecutor(
            # model_type="conformer_u2pp_online_wenetspeech",
            # lang="zh_en",
            # codeswitch=True,
        )
        self.text_punc = TextExecutor()
        self.mfa = MFAExecutor(corpus_directory=data_path)
        self.sd = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")

        self.Char = namedtuple("Char", ["char", "sTime", "eTime", "speaker"])
        self.AsrResult = namedtuple("AsrResult", ["text", "num_speakers", "chars"])

    def __call__(self, audio_file: str) -> tuple:
        """
        audio_file: file name (with extension)
        return: (text(with punctuation), num_speakers, chars(char, sTime, eTime, speaker))
        """

        file_name = audio_file.split(".")[0]
        audio_path = os.path.join(self.data_path, audio_file)

        # 音频转文本
        text: str = self.asr(audio_file=audio_path)
        # 文本标点恢复
        text_punc = self.text_punc(text=text)
        # 文本转拼音
        pinyin = text2pinyin(text)
        with open(os.path.join(self.data_path, file_name + ".lab"), "w") as file:
            file.write(pinyin)
        # 文本音频对齐
        intervals = self.mfa(file_name)  # [sTime, eTime, pinyin]
        assert len(text) == len(intervals)
        # 说话人分离
        diarization = self.sd(audio_path)

        # 记录文字、时间、说话人
        chars = []
        num_speakers = 0
        interval_idx = 0

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker = int(speaker[-2:])
            num_speakers = max(num_speakers, speaker + 1)

            while (
                interval_idx < len(intervals) and intervals[interval_idx][0] < turn.end
            ):
                interval = intervals[interval_idx]
                # assert text2pinyin(text[char_idx]) == interval.text
                chars.append(
                    self.Char(
                        char=text[interval_idx],
                        sTime=interval[0],
                        eTime=interval[1],
                        speaker=speaker,
                    )
                )
                interval_idx += 1

        while interval_idx < len(intervals):
            interval = intervals[interval_idx]
            # assert text2pinyin(text[char_idx]) == interval.text
            chars.append(
                self.Char(
                    char=text[interval_idx],
                    sTime=interval[0],
                    eTime=interval[1],
                    speaker=speaker,
                )
            )
            interval_idx += 1

        return self.AsrResult(text_punc, num_speakers, chars)


if __name__ == "__main__":
    asr = ASR()
    print(asr("1.wav"))
    print(asr("1.wav"))
