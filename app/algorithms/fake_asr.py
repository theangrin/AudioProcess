from typing import NamedTuple


class Sentence(NamedTuple):
    text: str
    start: float
    end: float
    speaker: int


class AsrResult(NamedTuple):
    full_text: str
    num_speakers: int
    sentences: list[Sentence]


class FakeASR:
    def __call__(self, audio_file: str) -> None:
        if audio_file.endswith("zh.wav"):
            return AsrResult(
                full_text="试错的过程很简单啊，今特别是今天冒名插血卡的同学，你们可以听到后面的有专门的活动课，它会大大降低你的思错成本。其实你也可以不要来听课，为什么你自己写嘛？我先今天写五个点，我就实试实验一下，反正这五个点不行，我再写五个点，再是再不行，那再写五个点嘛。你总会所谓的活动大神和所谓的高手都是只有一个，把所有的错。所有的坑全部趟一遍，留下正确的你就是所谓的大神明白吗？所以说关于活动通过这一块，我只送给你们四个字啊， 换位思考。如果说你要想降低你的试错成本，今天来这里你们就是对的。因为有创企创需要搞这个机会。所以说关于活动过于不过这个问题或者活动很难通过这个话题。呃，如果真的要坐下来聊的话，要聊一天。但是我觉得我刚才说的四个字足 够好，谢谢。好，非常感谢那个三毛老师的回答啊，三毛老师说我们在整个店铺的这个活动当中，我们要学会换位思考。其实。",
                num_speakers=2,
                sentences=[
                    Sentence(
                        text="试错的过程很简单啊，", start=0.38, end=3.01, speaker=0
                    ),
                    Sentence(
                        text="今特别是今天冒名插血卡的同学，",
                        start=3.01,
                        end=5.01,
                        speaker=0,
                    ),
                    Sentence(
                        text="你们可以听到后面的有专门的活动课，",
                        start=5.01,
                        end=9.27,
                        speaker=0,
                    ),
                    Sentence(
                        text="它会大大降低你的思错成本。",
                        start=9.27,
                        end=11.97,
                        speaker=0,
                    ),
                    Sentence(
                        text="其实你也可以不要来听课，",
                        start=11.97,
                        end=13.87,
                        speaker=0,
                    ),
                    Sentence(
                        text="为什么你自己写嘛？", start=13.87, end=15.49, speaker=0
                    ),
                    Sentence(
                        text="我先今天写五个点，", start=15.49, end=17.21, speaker=0
                    ),
                    Sentence(
                        text="我就实试实验一下，", start=17.21, end=18.87, speaker=0
                    ),
                    Sentence(
                        text="反正这五个点不行，", start=18.87, end=19.83, speaker=0
                    ),
                    Sentence(text="我再写五个点，", start=19.83, end=20.91, speaker=0),
                    Sentence(text="再是再不行，", start=20.91, end=21.99, speaker=0),
                    Sentence(
                        text="那再写五个点嘛。", start=21.99, end=23.485, speaker=0
                    ),
                    Sentence(
                        text="你总会所谓的活动大神和所谓的高手都是只有一个，",
                        start=23.485,
                        end=31.235,
                        speaker=0,
                    ),
                    Sentence(text="把所有的错。", start=31.235, end=32.94, speaker=0),
                    Sentence(
                        text="所有的坑全部趟一遍，", start=32.94, end=35.24, speaker=0
                    ),
                    Sentence(
                        text="留下正确的你就是所谓的大神明白吗？",
                        start=35.24,
                        end=38.96,
                        speaker=0,
                    ),
                    Sentence(
                        text="所以说关于活动通过这一块，",
                        start=38.96,
                        end=40.84,
                        speaker=0,
                    ),
                    Sentence(
                        text="我只送给你们四个字啊，", start=40.84, end=42.58, speaker=0
                    ),
                    Sentence(text="换位思考。", start=42.58, end=43.48, speaker=0),
                    Sentence(
                        text="如果说你要想降低你的试错成本，",
                        start=43.48,
                        end=46.725,
                        speaker=0,
                    ),
                    Sentence(
                        text="今天来这里你们就是对的。",
                        start=46.725,
                        end=49.495,
                        speaker=0,
                    ),
                    Sentence(
                        text="因为有创企创需要搞这个机会。",
                        start=49.495,
                        end=52.2,
                        speaker=0,
                    ),
                    Sentence(
                        text="所以说关于活动过于不过这个问题或者活动很难通过这个话题。",
                        start=52.2,
                        end=56.295,
                        speaker=0,
                    ),
                    Sentence(text="呃，", start=56.295, end=57.21, speaker=0),
                    Sentence(
                        text="如果真的要坐下来聊的话，",
                        start=57.21,
                        end=58.63,
                        speaker=0,
                    ),
                    Sentence(text="要聊一天。", start=58.63, end=59.345, speaker=0),
                    Sentence(
                        text="但是我觉得我刚才说的四个字足够好，",
                        start=59.345,
                        end=63.27,
                        speaker=0,
                    ),
                    Sentence(text="谢谢。", start=63.27, end=63.67, speaker=1),
                    Sentence(text="好，", start=63.67, end=64.13, speaker=1),
                    Sentence(
                        text=" 非常感谢那个三毛老师的回答啊，",
                        start=64.13,
                        end=66.01,
                        speaker=1,
                    ),
                    Sentence(
                        text="三毛老师说我们在整个店铺的这个活动当中，",
                        start=66.01,
                        end=68.75,
                        speaker=1,
                    ),
                    Sentence(
                        text="我们要学会换位思考。", start=68.75, end=69.99, speaker=1
                    ),
                    Sentence(text="其实。", start=69.99, end=70.315, speaker=1),
                ],
            )
        elif audio_file.endswith("en.mp3"):
            return AsrResult(
                full_text=" Christmas is round the corner and I'm looking for a gift for my girlfriend. Any suggestions? Well, you have to tell me something about your girlfriend first. Also, what's your budget?",
                num_speakers=2,
                sentences=[
                    Sentence(
                        text=" Christmas is round the corner and I'm looking for a gift for my girlfriend. Any suggestions?",
                        start=0.0,
                        end=9.0,
                        speaker=0,
                    ),
                    Sentence(
                        text=" Well, you have to tell me something about your girlfriend first. Also, what's your budget?",
                        start=9.0,
                        end=16.0,
                        speaker=1,
                    ),
                ],
            )
        elif audio_file.endswith("jp.mp3"):
            return AsrResult(
                full_text="お子様さんずいぶ寂しそうな顔しているそんなことないですよじゃあ私の間違いですかあいつに足りあせになってもらいたいんですよ僕たち唯一の動機ですから自分が幸せにしたいと思ったことないんですか同じことを朝朝にもお聞きしたいですね話がなるくなってもよければお答えしますけどじゃあ いやあところの言うましょうかいいですね私も今日は無償に飲みたい気分になって",
                num_speakers=3,
                sentences=[
                    Sentence(
                        text="お子様さんずいぶ寂 しそうな顔している",
                        start=0.0,
                        end=4.0,
                        speaker=1,
                    ),
                    Sentence(
                        text="そんなことないですよ", start=4.0, end=6.0, speaker=2
                    ),
                    Sentence(
                        text="じゃあ私の間違いですか", start=6.0, end=9.0, speaker=1
                    ),
                    Sentence(
                        text="あい つに足りあせになってもらいたいんですよ",
                        start=10.0,
                        end=12.0,
                        speaker=2,
                    ),
                    Sentence(
                        text="僕たち唯一の動機ですから", start=12.0, end=15.0, speaker=2
                    ),
                    Sentence(
                        text="自分が幸せにしたいと思ったことないんですか",
                        start=17.0,
                        end=20.0,
                        speaker=0,
                    ),
                    Sentence(
                        text="同じことを朝朝にもお聞きしたいですね",
                        start=20.0,
                        end=23.0,
                        speaker=0,
                    ),
                ],
            )
        else:
            return AsrResult(
                full_text="Hello world",
                num_speakers=1,
                sentences=[Sentence("Hello world", 0, 1, 0)],
            )


if __name__ == "__main__":
    audio_analyzer = FakeASR()
    print(audio_analyzer("zh.wav"))
    print(audio_analyzer("en.mp3"))
    print(audio_analyzer("jp.mp3"))
