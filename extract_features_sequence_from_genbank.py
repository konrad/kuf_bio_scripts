#!/usr/bin/env python

__description__ = ("Extract the sequences of a given feature type "
                   "(rRNA, gene, CDS) from a genebank file.")
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2013 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = "0.2"

import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description=__description__)
parser.add_argument("input_genkbank")
parser.add_argument("feature_type", help="e.g. rRNA, CDS")
parser.add_argument("--output_fasta", default="output.fa")
args = parser.parse_args()

with open(args.output_fasta, "w") as output_fh:
    for record in SeqIO.parse(args.input_genkbank, "genbank"):
        for feature in record.features:
            if feature.type != args.feature_type:
                continue
            output_fh.write(">%s-%s_%s\n%s\n" % (
                    feature.location.start,
                    feature.location.end,
                    {1 : "+", -1 : "-"}[feature.location.strand],
                    feature.extract(record).seq))
