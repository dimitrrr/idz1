import re
import string
from collections import Counter


def remove_chars_from_text(text, chars):
    return "".join([ch for ch in text if ch not in chars])


class Analyzer:
    def __init__(self, text):
        self.text = text.lower()
        self.raw_text = text.lower()

        spec_chars = string.punctuation + '\n\xa0«»\t—…'
        self.text = remove_chars_from_text(self.text, spec_chars)

    def get_table_stats_data(self):

        res = [
            ['Total words', self.get_words_amount()],
            ['Total chars (with spaces)', self.get_chars_amount()],
            ['Total chars (without spaces)', self.get_chars_amount_no_spaces()],
            ['Unique words', self.get_unique_words_amount()],
        ]
        res.extend(self.get_characters_stats())
        res.extend(self.get_words_stats())

        return res

    def get_characters_stats(self):
        s = self.raw_text
        numbers = sum(c.isdigit() for c in s)
        letters = sum(c.isalpha() for c in s)
        spaces = sum(c.isspace() for c in s)
        others = len(s) - numbers - letters - spaces

        return [
            ['Total numbers', numbers],
            ['Total letters', letters],
            ['Total spaces', spaces],
            ['Total others', others],
        ]

    def get_words_amount(self):
        words = self.raw_text.split(' ')
        return len(words)

    def get_chars_amount(self):
        return len(self.raw_text)

    def get_chars_amount_no_spaces(self):
        return len(self.raw_text.replace(" ", ""))

    def get_words_frequency(self):
        return self.count_words(self.raw_text, 10)

    def get_unique_words_amount(self):
        return len(self.count_words(self.raw_text, 50))

    def count_words(self, s, mc):
        elements = s.split()
        elements = [x.strip(' ') for x in elements]
        return Counter(elements).most_common(mc)

    def get_words_stats(self):
        words = self.raw_text.split(' ')
        r = re.compile("[а-яА-ЯёЁїЇ]+")
        cyrillic = [w for w in filter(r.match, words)]
        cyrillic_amount = len(cyrillic)
        latin_amount = len(words) - cyrillic_amount

        return [
            ['Cyrillic words', cyrillic_amount],
            ['Latin words', latin_amount],
        ]
