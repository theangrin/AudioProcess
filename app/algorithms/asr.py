from typing import NamedTuple
import torch
import whisper
from funasr import AutoModel
from pyannote.audio import Pipeline

from config import AlgorithmConfig


class Sentence(NamedTuple):
    text: str
    start: float
    end: float
    speaker: int


class AsrResult(NamedTuple):
    full_text: str
    num_speakers: int
    sentences: list[Sentence]


class ASR:
    def __init__(self, pyannote_token: str = AlgorithmConfig.PYANNOTE_TOKEN) -> None:
        device_str: str = "cuda" if torch.cuda.is_available() else "cpu"
        device: torch.device = torch.device(device_str)

        self.mul_model = whisper.load_model("base", device=device)
        self.en_model = whisper.load_model("base.en", device=device)
        self.zh_model = AutoModel(
            model="paraformer-zh",
            model_revision="v2.0.4",
            vad_model="fsmn-vad",
            vad_model_revision="v2.0.4",
            punc_model="ct-punc-c",
            punc_model_revision="v2.0.4",
            spk_model="cam++",
            spk_model_revision="v2.0.2",
            device=device_str,
        )
        self.pyannote = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=pyannote_token,
        ).to(device)

    def detect_language(self, audio_file: str) -> None:
        audio = whisper.load_audio(audio_file)
        audio_30s = whisper.pad_or_trim(audio)
        audio_30s_mel = whisper.log_mel_spectrogram(audio_30s).to(self.mul_model.device)
        _, probs = self.mul_model.detect_language(audio_30s_mel)
        return max(probs, key=probs.get)

    def recognize_zh(self, audio_file: str) -> None:
        output: dict = self.zh_model.generate(
            input=audio_file,
            batch_size_s=300,
            hotword="魔搭",
        )[0]

        # funasr postprocess
        sentences = []
        num_speakers = 0
        for s in output["sentence_info"]:
            num_speakers = max(num_speakers, s["spk"] + 1)
            sentences.append(
                Sentence(s["text"], s["start"] / 1000, s["end"] / 1000, s["spk"])
            )

        return AsrResult(
            full_text=output["text"],
            num_speakers=num_speakers,
            sentences=sentences,
        )

    def __whisper_postprocess(self, output, diarization):
        sentences = []
        num_speakers = 0

        segments = output["segments"]
        seg_p = 0
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker = int(speaker[-2:])
            num_speakers = max(num_speakers, speaker + 1)

            s_start, s_end = segments[seg_p]["start"], segments[seg_p]["end"]
            if (
                seg_p < len(segments)
                and (min(s_end, turn.end) - max(s_start, turn.start))
                / (turn.end - turn.start)
                >= 0.5
            ):
                sentences.append(
                    Sentence(
                        segments[seg_p]["text"],
                        segments[seg_p]["start"],
                        segments[seg_p]["end"],
                        speaker,
                    )
                )
                seg_p += 1

        return AsrResult(
            full_text=output["text"],
            num_speakers=num_speakers,
            sentences=sentences,
        )

    def recognize_en(self, audio_file: str) -> None:
        output = self.en_model.transcribe(audio_file, language="en")
        diarization = self.pyannote(audio_file)
        return self.__whisper_postprocess(output, diarization)

    def recognize_mul(self, audio_file: str, lang: str) -> None:
        output = self.mul_model.transcribe(audio_file, language=lang)
        diarization = self.pyannote(audio_file)
        return self.__whisper_postprocess(output, diarization)

    def __call__(self, audio_file: str) -> None:
        lang = self.detect_language(audio_file)
        if lang == "zh":
            return self.recognize_zh(audio_file)
        elif lang == "en":
            return self.recognize_en(audio_file)
        else:
            return self.recognize_mul(audio_file, lang)


if __name__ == "__main__":
    audio_analyzer = ASR()
    print(audio_analyzer("zh.wav"))
    print(audio_analyzer("en.mp3"))
    print(audio_analyzer("jp.mp3"))
