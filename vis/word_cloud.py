import re

import hazm
import parsivar
import numpy as np
from os import path
from wordcloud_fa import WordCloudFa as WordCloud
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


class WordCloudGen:
    """Word Cloud Generator"""

    def __init__(self, mask=None, size=900, stop_words_addr=default_stop_words_path, mask_addr=None):
        self.hazm_normalizer = hazm.Normalizer()
        self.parsivar_normalizer = parsivar.Normalizer()
        self.stemmer = hazm.Stemmer()
        self.lemmatizer = hazm.Lemmatizer()
        self.stop_words = set(hazm.stopwords_list(stop_words_addr))
        mask = np.array(Image.open(mask_addr)) if mask_addr is not None else None
        self.generator = WordCloud(
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
            msg = re.sub(r"https?:\/\/\S*", "", msg)  # https://github.com/MasterScrat/Chatistics
            msg = re.sub(r"\@\S*", "", msg)
            msg = self._normalize(msg)
            msg = msg.replace("ؤ", "و")
            msg = msg.replace("أ", "ا")
            msg = self._remove_punctuations(msg)
            msg = self._remove_weird_chars(msg)
            for word in msg.split():
                if self._is_stop_word(word):
                    word = ""
                if word:
                    # word = self.stemmer.stem(word)
                    word = word.replace(u"\u200c", "")
                    words.append(word)
        return " ".join(words)

    def _normalize(self, text):
        text = self.hazm_normalizer.normalize(text)
        text = self.parsivar_normalizer.normalize(text)
        return text

    def _is_stop_word(self, word):
        if word in {"بابا", "کار", "وقت", "دست", "خدا", "انقد", " چقد", "نیس", "جدی", "ینی", "چقد", "واسه", "دگ", "اینقد", "gt", "lt"}:
            return True
        if word.startswith("در"):
            modified_word = word[3:]
            if self._is_stop_verb(modified_word):
                return True
        if word.startswith("ب"):
            modified_word = word[2:]
            if self._is_stop_verb(modified_word):
                return True
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
            modified_word = word[:-1] + "د"  # داره
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
            if modified_word in self.stop_words:
                return True
            modified_word = word[:-1] + "ود"  # می‌ره
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
            modified_word = word + "د"  # می‌ده
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
            modified_word = word[:-1]  # رفته
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
        if word[-1] == "ن":
            modified_word = word + "د"  # داره
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
        if "میا" in word:
            modified_word = word.replace("میا", "می\u200cآی")
            if self._is_stop_verb(modified_word):
                return True
        if "گ" in word:
            modified_word = word.replace("گ", "گوی")
            modified_word = modified_word.replace("گویه", "گوید")
            modified_word = modified_word.replace("گوین", "گویند")
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
            if word == "میگن":
                print(modified_word)
        if word[-1] == "ا":
            modified_word = word[:-1] + "ی"  # حتا -> حتی
            if modified_word in self.stop_words:
                return True
        if "ا" in word:
            modified_word = word[::-1].replace("ا", "اه\u200c", 1)[::-1]
            if modified_word in self.stop_words:
                return True
            if self.stemmer.stem(modified_word) in self.stop_words:
                return True
            modified_word = word[::-1].replace("ا", "یاه\u200c", 1)[::-1]
            if modified_word in self.stop_words:
                return True
            if self.stemmer.stem(modified_word) in self.stop_words:
                return True
        if word[-1] == "ن":
            modified_word = word[:-1]  # حتمن -> حتماً
            if self.stemmer.stem(modified_word) in self.stop_words:
                return True
            modified_word = word[:-1] + "ا"  # حتمن -> حتماً
            if modified_word in self.stop_words:
                return True
            modified_word = word[:-1] + "لا"  # اصن -> اصلاً
            if modified_word in self.stop_words:
                return True
        if word[-1] == "و":  # خودشو -> خودش را
            modified_word = word[:-1]
            if modified_word in self.stop_words:
                return True
            if self.stemmer.stem(modified_word) in self.stop_words:
                return True
        if "و" in word:
            modified_word = word.replace("و", "ا")  # همون -> همان
            modified_word = modified_word.replace("اا", "آ")  # اومده -> آمده
            if modified_word in self.stop_words:
                return True
            if self.stemmer.stem(modified_word) in self.stop_words:
                return True
            if self._is_stop_verb(modified_word):  # نمیدونم -> نمی‌دانم
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
            if word[-1] == "ا":  # خودشونو -> خودشان را
                modified_word = word[:-1]
                if modified_word in self.stop_words:
                    return True
                if self.stemmer.stem(modified_word) in self.stop_words:
                    return True
        if "خوا" in word:  # می‌خوام
            modified_word = word.replace("خوا", "خواه", 1)
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
        if "خا" in word:  # می‌خام
            modified_word = word.replace("خا", "خواه", 1)
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
        if "تو" in word:  # می‌خام
            modified_word = word.replace("تو", "اوت", 1)
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
        if "ر" in word:  # می‌رم
            modified_word = word.replace("ر", "رو", 1)
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
        if "بود" in word:  # رفته بودم
            modified_word = re.sub("ه[\u200c ]بود.*", "", word)
            if self._is_stop_verb(modified_word):
                return True
            if self._is_stop_verb(modified_word.replace("می", "می\u200c", 1)):
                return True
        if word == "فک":
            modified_word = "فکر"
            if modified_word in self.stop_words:
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
