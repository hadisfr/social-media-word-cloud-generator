import re

from wordcloud_fa import WordCloudFa

weird_patterns = re.compile(  # https://stackoverflow.com/a/57506785
    r"["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u'\U00010000-\U0010ffff'
    u"\u200d"
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\u3030"
    u"\ufe0f"
    u"\u2069"
    u"\u2066"
    # u"\u200c"
    u"\u2068"
    u"\u2067"
    r"]+",
    flags=re.UNICODE)


punctuation_patterns = re.compile(
    r"["
    u"،؟«»؛٬"  # https://github.com/ImanMh/persianRex
    r"\.:\!\-\[\]\(\)\/"  # https://github.com/ImanMh/persianRex
    r"\@\?\;\#\$\%\^\&\*\+\=\\\{\}\_\^"
    r"]+"
    )


class WordCloud:
    """Telegram Word Cloud"""

    def __init__(self, mask=None, size=900):
        self.generator = WordCloudFa(width=size, height=size,
                                     include_numbers=False, persian_normalize=True,
                                     background_color='white')

    def get_word_cloud(self, msgs):
        self.generator.generate_from_text(self._preprocess(msgs)).to_image().show()

    def _preprocess(self, msgs):
        words = []
        for msg in msgs:
            msg = re.sub(r'^https?:\/\/.*', "", msg)  # https://github.com/MasterScrat/Chatistics
            msg = self._remove_punctuations(msg)
            msg = self._remove_weird_chars(msg)
            words += msg.split()
        return " ".join(words)

    @staticmethod
    def _remove_punctuations(text):
        return punctuation_patterns.sub("", text)

    @staticmethod
    def _remove_weird_chars(text):
        return weird_patterns.sub("", text)
