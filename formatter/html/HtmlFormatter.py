from formatter.AbstractFormatter import AbstractFormatter
import json
import os


class HtmlFormatter(AbstractFormatter):
    def make_file(self):
        rf = open(self.result_file, 'r', encoding='utf-8')

        self.result_data = json.load(rf)
        rf.close()

        of = open(self.output_file, 'w', encoding="utf-8")

        of.write('<!DOCTYPE html><html><head>')
        of.write('<title>%s</title>' % os.path.basename(self.result_file))
        of.write('</head><body>')

        # Main data
        of.write("<table>")

        of.write("<tr><td><b>Author:</b></td><td>%s</td></tr>" % self.result_data['author'])
        of.write("<tr><td><b>Config file:</b></td><td>%s</td></tr>" % self.result_data['config']['file'])
        of.write("<tr><td><b>Config file SHA256:</b></td><td>%s</td></tr>" % self.result_data['config']['sha256'])
        of.write("<tr><td><b>Evidence folder path:</b></td><td>%s</td></tr>" % self.result_data['evidence_folder'])

        of.write("</table>")

        of.write("<hr>")

        of.write("<h1>Result</h1>")

        of.write('</body></html>')
        of.close()