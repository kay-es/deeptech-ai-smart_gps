import csv

with open("trumpfdata/logistik/items.tsv") as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row in reader:
    print("H")