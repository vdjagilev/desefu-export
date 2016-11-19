from formatter.AbstractFormatter import AbstractFormatter
import json
import os


class HtmlFormatter(AbstractFormatter):
    def make_file(self):
        of = open(self.output_file, 'w', encoding="utf-8")

        of.write('<!DOCTYPE html><html><head>')
        of.write('<meta charset="utf-8">')
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

            if len(mod['data']) > 0:
                of.write("<h5>Collected data</h5>")
                file_list = sorted(mod['data'].keys())
                for file_name in file_list:
                    file_data = mod['data'][file_name]
                    of.write("<b>%s</b>" % file_name)

                    of.write("<ul>")
                    for file_data_elem in file_data:
                        if isinstance(file_data_elem, tuple):
                            of.write("<li>")
                            of.write("<ul>")
                            for i in file_data_elem:
                                of.write("<li>%s</li>" % i)
                            of.write("</ul>")
                            of.write("</li>")
                        else:
                            of.write("<li>%s</li>" % file_data_elem)
                    of.write("</ul>")

            try:
                if len(mod['extract_data']) > 0:
                    of.write("<h5>Extracted data</h5>")
                    file_list = sorted(mod['extract_data'].keys())

                    for file_name in file_list:
                        file_data = mod['extract_data'][file_name]
                        table_views = sorted(file_data.keys())
                        of.write("<b style=\"background-color: #ccc;\">%s</b><br />" % file_name)

                        for table in table_views:
                            table_info = file_data[table]

                            of.write("<b>%s</b>" % table)
                            of.write("<table style=\"white-space: nowrap;\">")

                            for col in table_info[0]:
                                of.write("<th style=\"background-color: #ccc;\">%s</th>" % col)

                            for row in table_info[1]:
                                of.write("<tr>")
                                for col_data in row:
                                    if isinstance(col_data, bytes):
                                        of.write("<td style=\"min-width: 100px;\">%s</td>" % col_data.decode('utf-8', 'ignore'))
                                    else:
                                        of.write("<td style=\"min-width: 100px;\">%s</td>" % col_data)
                                of.write("</tr>")

                            of.write("</table>")

                        of.write('<hr style="margin-bottom: 100px;" />')
            except KeyError:
                pass

            sub_module_chain = None

            try:
                sub_module_chain = mod['module_chain']
            except KeyError:
                continue

            if sub_module_chain:
                of.write('<hr />')
                of.write("<div style=\"padding-left: 5px; border-left: 3px; border-left-style: dotted; border-left-color: #ccc\"")
                self.traverse_chain(of, sub_module_chain)
                of.write("</div>")
