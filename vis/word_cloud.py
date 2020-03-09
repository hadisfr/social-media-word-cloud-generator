import re

import hazm
import numpy as np
from os import path
from wordcloud_fa import WordCloudFa
from PIL import Image

default_stop_words_path = path.join(path.dirname(__file__), ("assets/stopwords/persian").replace("/", path.sep))

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
    r"\@\?\;\#\$\%\^\&\*\+\=\\\{\}\_\^…'\"\|\/"
    u"ًٌٍَُِّْ"
    r"]+"
    )


class WordCloud:
    """Telegram Word Cloud"""

    def __init__(self, mask=None, size=900, stop_words_addr=default_stop_words_path, mask_addr=None):
        self.normalizer = hazm.Normalizer()
        self.stemmer = hazm.Stemmer()
        self.lemmatizer = hazm.Lemmatizer()
        self.stop_words = set(hazm.stopwords_list(stop_words_addr))
        mask = np.array(Image.open(mask_addr)) if mask_addr is not None else None
        self.generator = WordCloudFa(
            width=size,
            height=size,
            include_numbers=False,
            persian_normalize=False,
            collocations=True,
            mask=mask,
            background_color='white'
        )

    def get_word_cloud(self, msgs):
        return self.generator.generate_from_text(self._preprocess(msgs)).to_image()

    def _preprocess(self, msgs):
        words = []
        for msg in msgs:
            msg = re.sub(r"https?:\/\/.*", "", msg)  # https://github.com/MasterScrat/Chatistics
            msg = self._normalize(msg)
            msg = msg.replace("ؤ", "و")
            msg = msg.replace("أ", "ا")
            msg = self._remove_punctuations(msg)
            msg = self._remove_weird_chars(msg)
            for word in msg.split():
                if self._is_stop_word(word):
                    word = ""
                if word:
                    word = word.replace(u"\u200c", "")
                    if "\u200c" in word:
                        print(word)
                    words.append(word)
        return " ".join(words)

    def _normalize(self, text):
        text = self.normalizer.normalize(text)
        text = re.sub(r" (های[متش])", u"\u200c\\1", text)  # کتاب هایت -> کتاب‌هایت
        text = re.sub(r" (ا[متش])", u"\u200c\\1", text)  # نامه ام -> نامه‌ام
        text = re.sub(r" (ا[می])", u"\u200c\\1", text)  # رفته ام -> رفته‌ام
        return text

    def _is_stop_word(self, word):
        if word in self.stop_words:
            return True
        if self.stemmer.stem(word) in self.stop_words:
            return True
        if self._is_stop_verb(word):
            return True
        if self._is_stop_verb(word.replace("می", "می\u200c", 1)):  # میمیرد -> می‌میرد
            return True
        if (word[0] == "ب" or word[0] == "ن"):  # برو، نره
            if word[1:] in self.stop_words:
                return True
            if word[-1] == "ه":
                if word[1:-1] + "ود" in self.stop_words:
                    return True
        if word[-1] == "ه":
            word = word[:-1] + "د"  # داره
            if self._is_stop_verb(word):
                return True
            if self._is_stop_verb(word.replace("می", "می\u200c", 1)):
                return True
            word = word[:-1]  # رفته
            if self._is_stop_verb(word):
                return True
            if self._is_stop_verb(word.replace("می", "می\u200c", 1)):
                return True
        return False

    def _is_stop_verb(self, word):
        lem = self.lemmatizer.lemmatize(word).split("#")
        if len(lem) == 2:
            if lem[0] in self.stop_words or lem[1] in self.stop_words:
                return True
        return False

    @staticmethod
    def _remove_punctuations(text):
        return punctuation_patterns.sub(" ", text)

    @staticmethod
    def _remove_weird_chars(text):
        return weird_patterns.sub(" ", text)
