import scipy.stats as stats
import csv

# Spearman's correlation
def spearman(sample1,sample2):
    spearman = stats.spearmanr(sample1, sample2)
    return spearman

with open('analysisResult/result1.csv') as f:
    csvFile = csv.reader(f)
    headers = next(csvFile)
    col_types = [float,float,float,float,float,float]
    sample = []
    for row in csvFile:
        row = tuple(convert(value) for convert, value in zip(col_types,row))
        sample.append(row)
print(sample)

spearman = spearman(sample[0], sample[1])
print(spearman)
