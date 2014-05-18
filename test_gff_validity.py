#!/usr/bin/env python                                                                                                                                  
""" Tiny script to test validity (i.e. parsebility by Gff3Parser) of a GFF3
file.

Just give a GFF3 file as paremeter

"""

__description__ = ""
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2014 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = ""

import sys
from kufpybio.gff3 import Gff3Parser

parser = Gff3Parser()
previous_entry = None
try:
    for entry in parser.entries(open(sys.argv[1])):
        previous_entry = entry
    print("File can be parsed without any error.")
except:
    print("Error. Last valid entry:\n%s" % previous_entry)
