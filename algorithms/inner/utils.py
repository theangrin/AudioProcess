from pypinyin import pinyin, lazy_pinyin, Style


def text2pinyin(str: str) -> str:
    return " ".join(lazy_pinyin(str, style=Style.TONE3, neutral_tone_with_five=True))
