import codecs
import csv

with codecs.open("trumpfdata/logistik/areas.tsv", "r", encoding='utf-8', errors='ignore') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        print(row)