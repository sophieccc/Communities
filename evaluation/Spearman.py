import scipy.stats as stats
import csv

with open('analysisResult/result1.csv') as f:
    csvFile = csv.reader(f)
    headers = next(csvFile)
    col_types = [float,float,float,float,float,float]
    sample = []
    for row in csvFile:
        row = tuple(convert(value) for convert, value in zip(col_types,row))
        sample.append(row)
print(sample)

# Spearman's correlation
spearman = stats.spearmanr(sample[0], sample[1])
print(spearman)
