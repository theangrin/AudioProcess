import librosa
import numpy as np
import json


def get_amplitudes(audio_path: str):
    audio, sr = librosa.load(audio_path)
    duration = len(audio) / sr

    audio = abs(audio)
    x = np.arange(0, duration, 0.1)
    y = []
    for i in range(len(x)):
        start = x[i - 1] if i > 0 else 0
        end = x[i + 1] if i < len(x) - 1 else duration
        amplitude = audio[int(start * sr) : int(end * sr)].mean()
        y.append(amplitude)

    y = np.interp(y, (np.min(y), np.max(y)), (0, 1))

    return {"amplitudes": [(round(x[i], 1), round(y[i], 4)) for i in range(len(x))]}


if __name__ == "__main__":
    amplitudes = get_amplitudes("audio/zh.wav")
    print(json.dumps(amplitudes))
