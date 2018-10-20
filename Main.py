import matplotlib.pyplot as plt
import codecs
import csv
import numpy as np

with codecs.open("F:/Deeptech-ai/deeptech-ai/trumpfdata/logistik/position_history_new_starts_at_01.07.2018.tsv", "r",
                 encoding='utf-8', errors='ignore') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    next(reader)
    data = []
    for row in range(1000):
        data.append(next(reader))
    xs = [float(x) for x in np.array(data)[:, 2]]
    ys = [float(y) for y in np.array(data)[:, 3]]

    img = plt.imread("F:/Deeptech-ai/deeptech-ai/trumpfdata/logistik/ShopFloorLayout.png")

    figure, ax = plt.subplots(figsize=(9, 9))
    ax.set_xlim((-60, 60))
    ax.set_ylim((-60, 60))
    ax.imshow(img)
    plt.plot(xs, ys, 'ro')
    plt.show()
