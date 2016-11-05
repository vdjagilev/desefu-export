from abc import ABC, abstractmethod
import sys


class AbstractFormatter(ABC):
    def __init__(self, result_file, output_file):
        self.result_file = result_file
        self.output_file = output_file

        self.result_data = None

    @abstractmethod
    def make_file(self):
        pass
