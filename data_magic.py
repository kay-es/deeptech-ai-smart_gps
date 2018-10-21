import codecs
import csv
import numpy as np
import torch
item_history = "trumpfdata/logistik/itemshistory.tsv"
areas = "trumpfdata/logistik/areas.tsv"
file_position_history = "trumpfdata/logistik/positions_new.tsv"
myfile_path = "trumpfdata/logistik/data.csv"

marker_ids = []
with codecs.open(item_history, "r", encoding='utf-8', errors='ignore') as tsvfile:
    reader = list(csv.reader(tsvfile, delimiter='\t'))

    # GET ALL MARKERS
    for row in reader:
        if row[3] != "-1" and row[3] != "address":
            marker_ids.append(row[3])

    marker_ids = np.unique(marker_ids)
    # END GET ALL MARKERS

    # FOR LOOP OVER ALL MARKER IDS
    global_data = []
    output = []
    for k, marker_id in enumerate(marker_ids):

        # ADD ALL ROWS FOR MARKER ID TO PREPARE ALL BATCHES OF THAT MARKER
        rows = []
        for row in reader:
            if row[3] == marker_id:
                rows.append(row)


        # DUMMY PROCESSES FOR SPECIFIC MARKER
        # CALCULATE START AND END
        processes = []
        for i, row in enumerate(rows):
            train = [-1] * 5
            if row[1] != "":
                train[3] = float(row[2]) # START
                try:
                    if rows[i + 1][1] == "":
                        train[4] = float(rows[i + 1][2]) # END
                except IndexError:
                    gotdata = 'null'
                if(train[4] != -1):
                    processes.append(train)

        # END DUMMY BATCHES

        # GET ALL POSITIONS AS BATCHES FOR EACH PROCESS
        with codecs.open(file_position_history, "r", encoding='utf-8', errors='ignore') as posfile:
            pos_reader = csv.reader(posfile, delimiter=',')

            if(processes != []):
                positions = []
                for pot_position in pos_reader:
                    if (float(pot_position[1])) == float(marker_id): # marker
                        positions.append(pot_position)

                # NEUEN BATCH FÜR JEDES TRAINING_DATA INKL ALLE POSITIONS
                for train in processes:
                    batch = []
                    if train[4] != -1:
                        for p in positions:
                            if float(p[5]) >= train[3] and float(p[5]) <= train[4]:
                                new_train = train.copy()
                                new_train[1] = float(p[5])
                                new_train[0] = float(p[1])
                                new_train[2] = float(p[6])
                                batch.append(new_train)
                        if len(batch) != 0 and batch != []:
                            global_data.append(batch)


        print(k/len(marker_ids) * 100, "%")
        torch.save(global_data, open('traindata.pt', 'wb'))