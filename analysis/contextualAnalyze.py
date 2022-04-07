# __DATA_OF_BIG_FIVE_ = "test.json" # 0: "test.json", 1: "../data/all_text.json"
__DATA_OF_CONTEXTUAL_ = "../data/all_text.json"
__TYPE_OF_WORD__ = ["noun", "adjective", "preposition", "article", "pronoun", "verb", "adverb", "interjection"]

import json

import pandas as pd
import stanza

class BasicAnalyze:
    def __init__(self, data_source):
        self.data_source = None
        self.data_type = None
        self.data = None
        self.all_text = None
        self.data_frame = None
        self._set_data_source(data_source)
        self.noun_freq = None
        self.adjective_freq = None
        self.preposition_freq = None
        self.article_freq = None
        self.pronoun_freq = None
        self.ver_freq = None
        self.adverb_freq = None
        self.interjection_freq = None

    def _set_data_source(self, data_source):
        self.data_source = data_source
        self.data_type = data_source.split('.')[-1]

    def set_data_source(self, data_source):
        self._set_data_source(data_source)

    def process_data(self):
        pass

    def _stat(self):
        pass

class ContextualAnalyze(BasicAnalyze):
    def __init__(self, data_source):
        super().__init__(data_source)
        self._process_data()

    def _process_data(self):
        if self.data_type == "json":
            self.data = pd.read_json(self.data_source, typ="series")
            self.all_text = self.data.to_frame("text").loc["text"][0].split()
            print(self.all_text)
            self.data_frame = pd.DataFrame(data=[[i, 0, 0, 0, 0, 0, 0, 0, 0, 1] for i in self.all_text],
                                           index=self.all_text,
                                           columns=["text", *__TYPE_OF_WORD__, "total"])
            self.data_frame = self._count(self.data_frame)

    def _count(self, data):
        data = data.groupby(["text", *__TYPE_OF_WORD__])["total"]. \
            sum(). \
            reset_index(). \
            sort_values(by="total", ascending=False). \
            reset_index(drop=True)
        return data

    def stat(self):
        self._count(self.data_frame)
        # self.verb_stats()

    def print_result_for_test(self):
        # pd.set_option('display.max_columns', None)
        print(self.data_frame)

    def calculate(self):
        return (self.noun_freq + self.adjective_freq + self.preposition_freq + self.article_freq
             - self.pronoun_freq - self.ver_freq - self.adverb_freq - self.adverb_freq + 100)/2

    def verb_stats(self):
        nlp = stanza.Pipeline(lang="en", processors="tokenize,mwt,pos")
        verb_count = 0
        value = "a good car in it" # test
        doc = nlp(value)
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.upos.startswith("R"):
                    verb_count += 1
        print("Number of berns: {}".format(verb_count))


def run_contextual():
    data_file = __DATA_OF_CONTEXTUAL_
    analyzer = ContextualAnalyze(data_file)
    analyzer.stat()
    # analyzer.print_result_for_test()
    analyzer.verb_stats()

    # zh_nlp = stanza.Pipeline('zh')
    # en_nlp = stanza.Pipeline('en')
    # stanza.download('en')
    # nlp = stanza.Pipeline('en')
    # doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
    # nlp = stanza.Pipeline('en')
    # doc = nlp("Barack Obama was born in Hawaii.  John studies at Stanford University in NewYork.")
    # for sentence in doc.sentences:
    #     print(sentence.ents)

if __name__ == "__main__":
    run_contextual()
