#!/usr/bin/env python
"""
FUNCTION: Adds a column with GO term and their names. 

Copyright (c) 2013, Konrad Foerstner <konrad@foerstner.org>

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.

THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

"""
__description__ = ""
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2013 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = "0.1"

import argparse
import json
import os
import csv
import sys
from bioservices import UniProt
from bioservices import QuickGO

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file")
    parser.add_argument("gene_id_column", 
                        help="Column that contain the GeneID entry.")
    parser.add_argument("output_file")
    args = parser.parse_args()
    go_term_adder = GOTermAdder(args.input_file, args.output_file)
    go_term_adder.add_go_terms()
    
class GOTermAdder(object):
        
    def __init__(self, input_file, output_file):
        self._input_file = input_file
        self._output_file = output_file
        self._tmp_folder = "tmp_data"
        self._uniprot = UniProt(verbose=False)
        self._quickgo = QuickGO(verbose=False)
        if os.path.exists(self._tmp_folder) is False:
            os.mkdir(self._tmp_folder)
            
    def add_go_terms(self):
        i = 0
        with open(self._output_file, "w") as output_fh:
            for row in csv.reader(open(self._input_file), delimiter="\t"):
                i += 1
                if len(row[0]) == 0:
                    self._write_row(row, output_fh)
                    continue
                else:
                    row = self._add_go_term_column(row)
                    self._write_row(row, output_fh)
                if i > 10:
                    sys.exit()

    def _write_row(self, row, output_fh):
        output_fh.write("\t".join(row) + "\n")

    def _add_go_term_column(self, row):
        gene_id = self._gene_id(row)
        uniprot_id = self._uniprot_id(gene_id)
        if uniprot_id is None:
            return row
        go_terms = self._go_terms(uniprot_id)
        go_term_names = [
            self._go_term_name(go_term) for go_term in go_terms]
        assert len(go_terms) == len(go_term_names)
        row.append(", ".join(
            ["%s (%s)" % (go_terms, go_term_names) 
             for go_terms, go_term_names in 
             zip(go_terms, go_term_names)]))
        return row

    def _uniprot_id(self, gene_id):
        file_path = self._tmp_file_path(gene_id)
        if os.path.exists(file_path) is True:
            with open(file_path) as json_fh:
                return json.load(json_fh)["Uniprot"] 
        else:
            uniprot_id = self._search_uniprot_id(gene_id)
            gene_data = {"Uniprot" : uniprot_id}
            with open(file_path, "w") as json_fh:
                json.dump(gene_data, json_fh)

    def _go_terms(self, uniprot_id):
        file_path = self._tmp_file_path(uniprot_id)
        if os.path.exists(file_path) is True:
            with open(file_path) as json_fh:
                return json.load(json_fh)["GO-Terms"]
        else:
            uniprot_entry = self._uniprot.searchUniProtId(uniprot_id)
            go_ids = []
            for dbref in uniprot_entry.findAll("dbreference"):
                if dbref.attrs["type"] == "GO":
                    go_ids.append(dbref.attrs["id"])
                go_term_data = {"GO-Terms" : go_ids}
                with open(file_path, "w") as json_fh:
                    json.dump(go_term_data, json_fh)
            return go_ids

    def _go_term_name(self, go_term):
        file_path = self._tmp_file_path(go_term)
        if os.path.exists(file_path) is True:
            with open(file_path) as json_fh:
                return json.load(json_fh)["name"]
        else:
            go_term_info = self._quickgo.Term(go_term).soup
            go_term_name = go_term_info.term.find("name").text
            go_term_data = {"name" : go_term_name}
            with open(file_path, "w") as json_fh:
                    json.dump(go_term_data, json_fh)
            return go_term_name

    def _search_uniprot_id(self, gene_id):
        uniprot_id_search = self._uniprot.quick_search(gene_id)
        if len(uniprot_id_search) == 1:
            uniprot_id = uniprot_id_search.keys()[0]
            return uniprot_id
        elif len(uniprot_id_search) > 1:
            pass
        elif len(uniprot_id_search) > 0:
            pass

    def _tmp_file_path(self, gene_id):
        return "%s/%s.json" % (self._tmp_folder, gene_id)

    def _gene_id(self, row):
        return row[9].split("GeneID:")[1].split(";")[0]

if __name__ == "__main__": 
    main()
