from formatter.AbstractFormatter import AbstractFormatter
import json
import os


class HtmlFormatter(AbstractFormatter):
    def make_file(self):
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

        of.write("<h2>Result</h2>")

        for mc in self.result_data['result']:
            self.traverse_chain(of, mc)

        of.write('</body></html>')
        of.close()

    def traverse_chain(self, of, mc):
        of.write("<h3>%s</h3>" % mc['module_chain_id'])

        for mod in mc['modules']:
            of.write("<h4 style=\"background-color: #ccc;\">%s</h4>" % mod['title'])
            of.write("<table>")
            of.write("<tr><td><b>Module ID</b></td><td>%s</td></tr>" % mod['mod'])
            of.write("<tr><td><b>File count</b></td><td>%s</td></tr>"  % mod['files_count'])
            of.write("</table>")

            sub_module_chain = None

            try:
                sub_module_chain = mod['module_chain']
            except KeyError:
                continue

            if sub_module_chain:
                of.write('<hr />')
                of.write("<div style=\"margin-left: 5px;\"")
                self.traverse_chain(of, sub_module_chain)
                of.write("</div>")
