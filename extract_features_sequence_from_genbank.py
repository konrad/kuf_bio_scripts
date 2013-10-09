#!/usr/bin/env python

__description__ = ("Extract the sequences of a given feature type "
                   "(rRNA, gene, CDS) from a genebank file.")
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2013 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = "0.3"

import argparse
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

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
            feature_seq_record = SeqRecord(feature.extract(record).seq)
            feature_seq_record.id = "%s-%s_%s" % (
                feature.location.start,
                feature.location.end,
                {1 : "+", -1 : "-"}[feature.location.strand])
            feature_seq_record.description = ""
            output_fh.write(feature_seq_record.format("fasta"))
