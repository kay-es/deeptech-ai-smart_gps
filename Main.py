import codecs
import csv
import matplotlib.pyplot as plt
import imageio

file_position_history = "trumpfdata/logistik/position_history_new_starts_at_01.07.2018.tsv"
x = []
y = []
i = 0
with codecs.open(file_position_history, "r", encoding='utf-8', errors='ignore') as tsvfile:
    plots = csv.reader(tsvfile, delimiter='\t')
    next(plots)
    for i, row in enumerate(plots):
        x.append(row[2])
        y.append(row[3])
        if i > 20:
            break
print("Plotting...")
plt.plot(x, y, 'ro', label='Loaded from file!')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()

