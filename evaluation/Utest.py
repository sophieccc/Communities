import scipy.stats as stats
import csv

# Mann Whitney U Test
def mannWhitney(sample1,sample2):
    Utest = stats.mannwhitneyu(sample1, sample2, use_continuity=True, alternative='two-sided')
    return Utest

with open('analysisResult/result1.csv') as f:
    csvFile = csv.reader(f)
    headers = next(csvFile)
    col_types = [float,float,float,float,float,float]
    sample = []
    for row in csvFile:
        row = tuple(convert(value) for convert, value in zip(col_types,row))
        sample.append(row)
print(sample)

Utest = mannWhitney(sample[0],sample[1])
print(Utest)