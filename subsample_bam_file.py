#!/usr/bin/env python
"""

This script subsamples the alignments of a BAM file. For this a
likelihood (0.0 < p(keep) < 1.0) of keeping all alignments of a read
has to be provided. All alignments of a read are treated the same
(i.e. are discarded or kept).

"""

import argparse
import random
import sys
import pysam

__description__ = "Subsample BAM file entries"
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2013 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = "0.1"

parser = argparse.ArgumentParser()
parser.add_argument("input_bam")
parser.add_argument("output_bam")
parser.add_argument("keeping_likelihood", type=float)
args = parser.parse_args()

input_bam = pysam.Samfile(args.input_bam, "rb")
output_bam = pysam.Samfile(
    args.output_bam, "wb", referencenames=input_bam.references, 
    referencelengths=input_bam.lengths, header=input_bam.header,
    text=input_bam.text)

prev_query = None
prev_keep = None
for alignment in input_bam:
    # This is for reads that multiple alignments. If there previous
    # alignment comes from the same read treat the current one the
    # same way (keep or discard).
    if  alignment.qname == prev_query:
        if prev_keep is True:
            output_bam.write(alignment)
            continue
        else:
            continue
    if random.random() <= args.keeping_likelihood:
        output_bam.write(alignment)
        prev_keep = True
    else:
        prev_keep = False
    prev_query = alignment.qname
