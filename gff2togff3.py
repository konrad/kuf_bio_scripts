"""Change attribute string from GFF2 format GGF3 format."""

import csv
import sys

for row in csv.reader(open(sys.argv[1]), delimiter="\t"):
    if not row[0].startswith("#"):
        row[8] = ";".join(
            ["%s=%s" % (attribute.split()[0], " ".join(attribute.split()[1:]))
             for attribute in row[8].split(" ; ")])
    print("\t".join(row))
