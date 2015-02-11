#!/usr/bin/env python

"""
Extracts the NOG, description and categaries of the NOG for each
protein of a given species from eggNOG files.

Example: 

Download the following files from eggNOG

ftp://eggnog.embl.de/eggNOG/4.0/members/bactNOG.members.txt.gz
ftp://eggnog.embl.de/eggNOG/4.0/description/bactNOG.description.txt.gz
ftp://eggnog.embl.de/eggNOG/4.0/funccat/bactNOG.funccat.txt.gz

and run

python bin/get_eggnog_selection_and_associated_functions.py \
  bactNOG.members.txt.gz \
  bactNOG.description.txt.gz \
  bactNOG.funccat.txt.gz \
  192222 \
  bactNOG_for_C_jejuni_NCTC_11168.csv

"""

__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2015 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"

import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("member_file")
parser.add_argument("description_file")
parser.add_argument("category_file")
parser.add_argument("species_id")
parser.add_argument("output_file")
args = parser.parse_args()

member_data = pd.read_table(args.member_file, compression="gzip")
member_data = member_data[
    member_data["protein name"].str.startswith(args.species_id + ".")]
description_data = pd.read_table(
    args.description_file, names=["nog name", "function"], compression="gzip")
member_data = member_data.merge(
    how="left", right=description_data, 
    left_on="#nog name", right_on="nog name")
category_data = pd.read_table(
    args.category_file, names=["nog name 2", "category"], compression="gzip")
member_data = member_data.merge(
    how="left", right=category_data, 
    left_on="#nog name", right_on="nog name 2")
output_df = pd.DataFrame()
output_df["Protein ID"] = member_data["protein name"]
output_df["Start"] = member_data["start position"]
output_df["End"] = member_data["end position"]
output_df["NOG"] = member_data["nog name"]
output_df["Function"] = member_data["function"]
output_df["Category"] = member_data["category"]
output_df.sort(inplace=True, columns=["Protein ID", "Start"])
output_df.to_csv(args.output_file, sep="\t", index=False)
