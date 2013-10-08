"""
Reformat a single entry fasta file.

E.g. useful if a fasta file contains a sequence in a single long
line. The Biopython SeqIO writer will generate a sequence with 
proper line lenght of 60 character.s

"""

import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument("input_fasta")
parser.add_argument("output_fasta")
args = parser.parse_args()
SeqIO.write(SeqIO.read(args.input_fasta, "fasta"), args.output_fasta, "fasta")
