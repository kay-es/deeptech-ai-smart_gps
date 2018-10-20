import codecs
import csv
import numpy as np
import torch

item_history = "trumpfdata/logistik/itemshistory.tsv"
areas = "trumpfdata/logistik/areas.tsv"
file_position_history = "trumpfdata/logistik/position_history_new_starts_at_01.07.2018.tsv"

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

    ############################################
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
            train = [None] * 5
            if row[1] != "":
                train[3] = float(row[2]) # START
                try:
                    if rows[i + 1][1] == "":
                        train[4] = float(rows[i + 1][2]) # END
                except IndexError:
                    gotdata = 'null'
                if(train[4] != None):
                    processes.append(train)

        # END DUMMY BATCHES

        # GET ALL POSITIONS AS BATCHES FOR EACH PROCESS

        with codecs.open(file_position_history, "r", encoding='utf-8', errors='ignore') as posfile:
            pos_reader = csv.reader(posfile, delimiter='\t')

            if(processes != []):
                print(processes)
                positions = []
                for pot_position in pos_reader:
                    if pot_position[1] == marker_id: # marker
                        positions.append(pot_position)

                print(positions)


                # NEUEN BATCH FÜR JEDES TRAINING_DATA INKL ALLE POSITIONS
                for train in processes:
                    batch = []
                    if train[4] != None:
                        for p in positions:
                            if float(p[5]) >= train[3] and float(p[5]) <= train[4]:
                                new_train = train.copy()
                                new_train[1] = float(p[5])
                                new_train[0] = float(p[1])
                                #new_train[2] = float(p[6])
                                # ADD AREA HERE AS new_train[2]
                                #print(new_train, "NEW_TRAIN")
                                print(p[5])
                                batch.append(new_train)
                        global_data.append(batch)


        if len(global_data) != 0:
            output = np.append(output, np.array(global_data))
            #print(output, "output")

        if k > 2:
            torch.save(output, open('traindata.pt', 'wb'))
            #with open('your_file.txt', 'w') as f:
             #   f.write("%s\n" % output)
            break