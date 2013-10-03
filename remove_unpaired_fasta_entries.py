#!/usr/bin/env python

"""
Remove unpaired reads from a fasta file.

This script can be used for the case that unpaired reads (e.g. as
reads were removed during quality trimming) in a pair of fasta files
from paired-end sequencing need to be removed.

"""

import argparse
from Bio import SeqIO
from Bio.SeqIO.FastaIO import FastaWriter

parser = argparse.ArgumentParser()
parser.add_argument("fasta_file_to_filter")
parser.add_argument("reference_fasta_file")
parser.add_argument("--output_fasta", default="output.fa")
args = parser.parse_args()

# Read reference file header
reference_headers = {}
for seq_record in SeqIO.parse(args.reference_fasta_file, "fasta"):
    reference_headers[seq_record.id.split()[0]] = 1

# Read fasta file to filter and write output
with open(args.output_fasta, 'w') as output_fh:
    writer = FastaWriter(output_fh, wrap=0)
    writer.write_file(
        filter(lambda seq_record: seq_record.id.split()[0] in reference_headers,
               SeqIO.parse(args.fasta_file_to_filter, "fasta")))
