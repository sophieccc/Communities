
class BasicAnalyzeMx:
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

    def set_data_source(self, data_source):
        pass

    def process_data(self):
        pass

    def _stat(self):
        pass

