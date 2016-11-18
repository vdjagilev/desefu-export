from abc import ABC, abstractmethod
import sys
import jsonpickle


class AbstractFormatter(ABC):
    def __init__(self, result_file, output_file):
        self.result_file = result_file
        self.output_file = output_file

        data = open(self.result_file, 'r', encoding='utf-8').read()
        self.result_data = jsonpickle.decode(data)

    @abstractmethod
    def make_file(self):
        pass
