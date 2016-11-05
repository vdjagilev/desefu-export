#!/usr/bin/env python3

import sys
from optparse import OptionParser
import importlib

if __name__ == '__main__':
    _version = '0.1'
    parser = OptionParser(
        usage="%prog [options] result.json output_file",
        version=_version
    )
    parser.add_option("-f", "--format", choices=['html', 'pdf'])

    (options, args) = parser.parse_args()

    print("Desefu export (%s)" % _version)

    result_file = None
    output_file = 'output.html'

    try:
        result_file = args[0]
    except IndexError:
        print("Please insert result JSON file generated with DESEFU")
        sys.exit()

    _format = 'html'

    if options.format is not None:
        _format = options.format

    try:
        output_file = args[1] + _format
    except IndexError:
        print("Using default \"output_file.%s\"" % _format)

    print("-------------------------------------------------------------------")

    formatter_mod = importlib.import_module('formatter.%s.%sFormatter' % (_format, _format.title()))
    formatter_class = getattr(formatter_mod, '%sFormatter' % _format.title())
    formatter_obj = formatter_class(result_file, output_file)
    formatter_obj.make_file()
    print("Done")
