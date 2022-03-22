__DATA_OF_BIG_FIVE_ = 'data/all_text.json' # 0: 'test.json', 1: '../data/all_text.json'
__DIMENTION_OF_BIG_FIVE__ = ['Extro', 'Agree', 'Consc', 'Neuro', 'Open']
__OUTPUT_FILE__ = 'analysisResult/big_five.json'

import json
import pandas as pd

class BigFiveAnalyze():
    def __init__(self, data_source):
        self.data_source = None
        self.data_type = None
        self.data = None
        self.all_text = None
        self.data_frame = None
        self._set_data_source(data_source)

    def _set_data_source(self, data_source):
        self.data_source = data_source
        self.data_type = data_source.split('.')[-1]
        self._process_data()

    def _process_data(self):
        if self.data_type == 'json':
            with open(self.data_source) as json_file:
                self.data = json.load(json_file)
                self.all_text = self.data["text"].split()
                self.data_frame = pd.DataFrame(data=[[i, 0, 0, 0, 0, 0,1] for i in self.all_text],
                                            index=self.all_text,
                                            columns=['text', *__DIMENTION_OF_BIG_FIVE__, 'total'])
                self.data_frame = self._count(self.data_frame)

    def _stat(self):
        self._count(self.data_frame)

    def _count(self, data):
        data = data.groupby(['text', *__DIMENTION_OF_BIG_FIVE__])['total']. \
            sum(). \
            reset_index(). \
            sort_values(by='total', ascending=False). \
            reset_index()
        return data

    def stat(self):
        self._stat()

    def save_result_for_test(self):
        self.data_frame.to_json(__OUTPUT_FILE__)


def run_big_five_analyze():
    data_file = __DATA_OF_BIG_FIVE_
    analyzer = BigFiveAnalyze(data_file)
    analyzer.stat()
    analyzer.save_result_for_test()

if __name__ == "__main__":
    run_big_five_analyze()