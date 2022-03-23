# __DATA_OF_BIG_FIVE_ = 'test.json' # 0: 'test.json', 1: '../data/all_text.json'
__DATA_OF_BIG_FIVE_ = '../data/all_text.json' # 0: 'test.json', 1: '../data/all_text.json'
__DIMENTION_OF_BIG_FIVE__ = ['Extro', 'Agree', 'Consc', 'Neuro', 'Open']

import json

from basicAnalyzeMx import BasicAnalyzeMx
import pandas as pd

class BigFiveAnalyze(BasicAnalyzeMx):
    def __init__(self, data_source):
        super().__init__(data_source)
        self._process_data()

    def _process_data(self):
        if self.data_type == 'json':
            self.data = pd.read_json(self.data_source, typ='series')
            # a = self.data['text'].str.split(' ', expand = False)
            self.all_text = self.data.to_frame('text').loc['text'][0].split()
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

    def print_result_for_test(self):
        print(self.data_frame)


def run_big_five_analyze():
    data_file = __DATA_OF_BIG_FIVE_
    analyzer = BigFiveAnalyze(data_file)
    analyzer.stat()
    analyzer.print_result_for_test()

if __name__ == '__main__':
    run_big_five_analyze()