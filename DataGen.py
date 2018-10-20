import codecs
import csv
#import pandas
import matplotlib.pyplot as plt

item_history = "trumpfdata/logistik/itemshistory.tsv"
areas = "trumpfdata/logistik/areas.tsv"
file_position_history = "trumpfdata/logistik/position_history_new_starts_at_01.07.2018.tsv"

myfile_path = "trumpfdata/logistik/data.csv"
with codecs.open(item_history, "r", encoding='utf-8', errors='ignore') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    rows = []
    for row in reader:
        if row[3] == "4751451578702838656":
            rows.append(row)
    #print(len(rows))
    #print(rows)


    # address timestamp area start end
    #rows.sort_values() # SORT VALUES BY TIMESTAMP
    training_data = []
    for i, row in enumerate(rows):
        train = [None] * 5
        if row[1] != "":
            train[3] = row[2] # START
            try:
                if rows[i + 1][1] == "":
                    train[4] = rows[i + 1][2] # END
            except IndexError:
                gotdata = 'null'
            training_data.append(train)

    print(training_data)


