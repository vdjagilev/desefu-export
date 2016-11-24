from formatter.AbstractFormatter import AbstractFormatter
import json
import os


class IndexElement:
    anchor = 0

    def __init__(self, content):
        self.content = content
        self.a = IndexElement.anchor
        self.node_list = []
        IndexElement.anchor += 1

    def addNode(self, e):
        self.node_list.append(e)

    def getHtmlIndex(index):
        html = "<li><a href=\"#%d\">%s</a></li>" % (index.a, index.content)

        if len(index.node_list) > 0:
            html += "<ol>"
            for node in index.node_list:
                html += IndexElement.getHtmlIndex(node)
            html += "</ol>"

        return html

class ResultElement:
    def __init__(self):
        self.content = ""

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

        result_element = ResultElement()
        result_element.content = "<h1>Result</h1>"
        index_list = []

        index_content = "<h1>Index</h1>"
        #of.write("<h2>Result</h2>")

        for mc in self.result_data['result']:
            index_elem = IndexElement(mc['module_chain_id'])
            index_list.append(index_elem)
            self.traverse_chain(result_element, index_elem, mc)

        index_content += "<ol>"
        for node in index_list:
            index_content += IndexElement.getHtmlIndex(node)
        index_content += "</ol>"
        #result_element.content += "<hr />"
        of.write(index_content)
        of.write(result_element.content)

        of.write('</body></html>')
        of.close()

    def traverse_chain(self, result: ResultElement, index: IndexElement, mc):
        result.content += "<h2 id=\"%d\">%s</h2>" % (index.a, mc['module_chain_id'])

        for mod in mc['modules']:
            mod_id_index = IndexElement(mod['title'])
            index.addNode(mod_id_index)

            result.content += "<h3 id=\"%d\" style=\"background-color: #ccc;\">%s</h3>" % (mod_id_index.a, mod['title'])
            result.content += "<table>"
            result.content += "<tr><td><b>Module ID</b></td><td>%s</td></tr>" % mod['mod']
            result.content += "<tr><td><b>File count</b></td><td>%s</td></tr>" % mod['files_count']
            result.content += "</table>"

            if len(mod['data']) > 0:
                result.content += "<h4 id=\"%d\" style=\"background-color: #ccc;\">Collected data</h4>" % IndexElement.anchor
                mod_id_index.addNode(IndexElement("Collected data"))

                file_list = sorted(mod['data'].keys())
                for file_name in file_list:
                    file_data = mod['data'][file_name]
                    result.content += "<b>%s</b>" % file_name

                    if len(file_data) > 0:
                        is_tuple = isinstance(file_data[0], tuple)

                        if not is_tuple:
                            result.content += "<ul>"
                        else:
                            result.content += "<table>"

                        for file_data_elem in file_data:
                            if is_tuple:
                                result.content += "<tr>"
                                result.content += "<td style=\"background-color: #ccc;\"><b>%s</b></td><td>%s</td>" % (file_data_elem[0], file_data_elem[1])
                                result.content += "</tr>"
                            else:
                                result.content += "<li>%s</li>" % file_data_elem

                        if not is_tuple:
                            result.content += "</ul>"
                        else:
                            result.content += "</table>"

            try:
                if len(mod['extract_data']) > 0:
                    result.content += "<h4 id=\"%d\">Extracted data</h4>" % IndexElement.anchor
                    mod_id_index.addNode(IndexElement("Extracted data"))
                    file_list = sorted(mod['extract_data'].keys())

                    for file_name in file_list:
                        file_data = mod['extract_data'][file_name]
                        table_views = sorted(file_data.keys())

                        result.content += "<b style=\"background-color: #ccc;\">%s</b><br />" % file_name

                        for table in table_views:
                            table_info = file_data[table]

                            result.content += "<b>%s</b>" % table
                            result.content += "<table style=\"white-space: nowrap;\">"

                            for col in table_info[0]:
                                result.content += "<th style=\"background-color: #ccc;\">%s</th>" % col

                            for row in table_info[1]:
                                result.content += "<tr>"
                                for col_data in row:
                                    cell_data = col_data

                                    if isinstance(col_data, bytes):
                                        cell_data = col_data.decode('utf-8', 'ignore')
                                    elif col_data == None:
                                        cell_data = "NULL"
                                    else:
                                        cell_data = col_data

                                    result.content += "<td style=\"min-width: 100px;\">%s</td>" % cell_data
                                result.content += "</tr>"

                            result.content += "</table>"

                        result.content += '<hr style="margin-bottom: 100px;" />'
            except KeyError:
                pass

            sub_module_chain = None

            try:
                sub_module_chain = mod['module_chain']
            except KeyError:
                continue

            if sub_module_chain:
                result.content += '<hr />'
                result.content += "<div style=\"padding-left: 5px; border-left: 3px; border-left-style: dotted; border-left-color: #ccc\""
                self.traverse_chain(result, index, sub_module_chain)
                result.content += "</div>"
