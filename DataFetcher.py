import codecs
import csv
import matplotlib.pyplot as plt

file_position_history = "trumpfdata/logistik/position_history_new_starts_at_01.07.2018.tsv"
x = []
y = []
i = 0

myfile_path = "trumpfdata/logistik/test.csv"
with codecs.open(file_position_history, "r", encoding='utf-8', errors='ignore') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    with codecs.open(myfile_path, "w", encoding='utf-8', errors='ignore') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(next(reader))
        for row in reader:
            if row[1] == "4751451578702838656":
                wr.writerow(row)

    '''for i, row in enumerate(plots):
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
    '''
