from formatter.AbstractFormatter import AbstractFormatter
import json
import os

class HtmlFormatter(AbstractFormatter):
    def make_file(self):
        rf = open(self.result_file, 'r')

        self.result_data = json.load(rf)
        rf.close()

        of = open(self.output_file, 'w')

        of.write('<!DOCTYPE html><html><head>')
        of.write('<title>%s</title>' % os.path.basename(self.result_file))
        of.write('</head><body>')

        

        of.write('</body></html>')
        of.close()
