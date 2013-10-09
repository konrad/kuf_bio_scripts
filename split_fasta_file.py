#!/usr/bin/env python

__description__ = "Split a fasta file and generate a file for each entry"
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2013 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = "0.2"

import argparse
import sys
from Bio import SeqIO

parser = argparse.ArgumentParser(description=__description__)
parser.add_argument("input_fasta")
parser.add_argument("--output_folder", default=".")
parser.add_argument("--prefix", default="", 
                    help="A prefix that is put before the sequence id in the "
                    "entry and the file name.")
args = parser.parse_args()
seen_id = {}
for record in SeqIO.parse(args.input_fasta, "fasta"):
    record.id = args.prefix + record.id
    if record.id in seen_id:
        sys.stderr.write("Error! ID '%s' used before. Stopped.\n" % record.id)
        sys.exit(1)
    with open("%s/%s.fa" % (args.output_folder, record.id), "w") as output_fh:
        output_fh.write(record.format("fasta"))
    seen_id[record.id] = 1
