import pandas as pd
import json
import numpy as np
import csv
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import codecs

# Generated Training File
trainingsfile = "trumpfdata/logistik/trainingdata.tsv"

# position history
file_position_history = "trumpfdata/logistik/position_history_new_starts_at_01.07.2018.tsv"

# Relevant fields are id and shape from areas.tsv
fields = ['id', 'shape']
areas = "trumpfdata/logistik/areas.tsv"

# Read areas.tsv
df = pd.read_csv(areas, delimiter='\t', skipinitialspace=True, usecols=fields)

# Get postion history
positions_df = pd.read_csv(file_position_history, delimiter='\t', skipinitialspace=True)

# Get column shape
shapes = df['shape']

# Get column id
id = df['id']

# Write into trainingsdata.tsv
with codecs.open(trainingsfile, "w", encoding='utf-8', errors='ignore') as tsvfile:
    wr = csv.writer(tsvfile, quoting=csv.QUOTE_ALL)

    # Iterate over every position in position history
    length = len(np.array(positions_df[1:]))
    for ka,position in enumerate(np.array(positions_df[1:])):

        new_position = position.copy()

        # Go through every row in areas and extract coordinates
        for i, shape in enumerate(shapes):
            # Extract coordinates
            x = json.loads(shape)['coordinates'][0]

            # Create a point
            point = Point(position[2], position[3])

            polygon = Polygon([(float(x[0][0]), float(x[0][1])), (float(x[1][0]), float(x[1][1])),
                               (float(x[2][0]), float(x[2][1])), (float(x[3][0]), float(x[3][1]))])
            final_position = []
            # If polygon cointains the given point the position is at an area of interest
            if polygon.contains(point):
                final_position = np.append(new_position, int(id[i]))
                wr.writerow(final_position)
                break
            elif i == len(shapes) - 1:
                final_position = np.append(new_position, int(1000))
                wr.writerow(final_position)


        if ka % 1000 == 0:
            print(ka/length, "%")