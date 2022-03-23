# __DATA_OF_BIG_FIVE_ = "test.json" # 0: "test.json", 1: "../data/all_text.json"
__DATA_OF_CONTEXTUAL_ = "../data/all_text.json" # 0: "test.json", 1: "../data/all_text.json"
__TYPE_OF_WORD__ = ["Noun", "Verb", "Prep", "Adj", "Adv"]

import json

from BasicAnalyzeMx import BasicAnalyzeMx
import pandas as pd
import stanza

class ContextualAnalyze(BasicAnalyzeMx):
    def __init__(self, data_source):
        super().__init__(data_source)
        self._process_data()

    def _process_data(self):
        if self.data_type == "json":
            self.data = pd.read_json(self.data_source, typ="series")
            self.all_text = self.data.to_frame("text").loc["text"][0].split()
            print(self.all_text)
            self.data_frame = pd.DataFrame(data=[[i, 0, 0, 0, 0, 0,1] for i in self.all_text],
                                           index=self.all_text,
                                           columns=["text", *__TYPE_OF_WORD__, "total"])
            self.data_frame = self._count(self.data_frame)

    def _stat(self):
        self._count(self.data_frame)

    def _count(self, data):
        data = data.groupby(["text", *__TYPE_OF_WORD__])["total"]. \
            sum(). \
            reset_index(). \
            sort_values(by="total", ascending=False). \
            reset_index()
        return data

    def stat(self):
        self._stat()
        self.verb_stats()

    def print_result_for_test(self):
        print(self.data_frame)

    def verb_stats(self):
        nlp = stanza.Pipeline(lang="en", processors="tokenize,mwt,pos")
        verb_count = 0
        value = "One may easily find online platforms that support discussions of particular" # test
        doc = nlp(value)
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.upos.startswith("V"):
                    verb_count += 1
        print("Number of berns: {}".format(verb_count))


def run_big_five_analyze():
    data_file = __DATA_OF_CONTEXTUAL_
    analyzer = ContextualAnalyze(data_file)
    analyzer.stat()
    analyzer.print_result_for_test()

if __name__ == "__main__":
    run_big_five_analyze()
