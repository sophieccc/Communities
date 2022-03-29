import json

import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def readData(inputFile):
    data = open(inputFile, 'r').read()
    dataList = json.loads(data)
    df = pd.json_normalize(dataList)
    return df

def sentimentAnalysis(input,output):
    with open(output, 'a') as f:
        result_list = []
        for text in input['text']:
            print(text)
            result = {'text':text}
            analyzer = SentimentIntensityAnalyzer()
            vs = analyzer.polarity_scores(text)
            result.update(vs)
            result_list.append(result)
        json.dump(result_list, f)

def sentimentAnalysisWithTime(input,output):
    with open(output, 'a') as f:
        result_list = []
        for index,row in input.iterrows():
            result = {'time':str(row['date'])+' '+str(row['time'])+':00','text':row['text']}
            analyzer = SentimentIntensityAnalyzer()
            vs = analyzer.polarity_scores(row['text'])
            result.update(vs)
            result_list.append(result)
        json.dump(result_list, f)

def merge(df):
    return ' '.join(df.values)

def groupByHour(df):
    df['datetime'] = pd.to_datetime(df['created'], unit='s')
    df['date'] = df['datetime'].dt.date
    df['time'] = df['datetime'].dt.hour
    df = df[['text', 'datetime','date','time']]
    df = df.groupby(['date','time'])['text'].apply(merge)
    df = df.reset_index()
    return df


# Overall Sentiment Analysis
allTechSupport_df = readData(inputFile='../data/combined_techsupport.json')
allMentalHealth_df = readData(inputFile='../data/combined_mentalhealth.json')
sentimentAnalysis(allTechSupport_df,'../analysisResult/combined_tectsupport_sentiment.json')
sentimentAnalysis(allMentalHealth_df,'../analysisResult/combined_mentalhealth_sentiment.json')

techSupport_df = readData(inputFile='../data/techsupport.json')
mentalHealth_df = readData(inputFile='../data/mentalhealth.json')

# Individual Emotional Analysis
sentimentAnalysis(techSupport_df,'../analysisResult/tectsupport_sentiment.json')
sentimentAnalysis(mentalHealth_df,'../analysisResult/mentalhealth_sentiment.json')

# get sentiment result
sentiment_techSupport_df = readData(inputFile='../analysisResult/tectsupport_sentiment.json')
print(sentiment_techSupport_df)
sentiment_techSupport_df['compound_group'] = pd.cut(sentiment_techSupport_df['compound'],bins=[-1,-0.8,-0.6,-0.4,-0.2,-0.05,0.05,0.2,0.4,0.6,0.8,1],labels=['[-1,-0.8]','[-0.8,-0.6]','[-0.6,-0.4]','[-0.4,-0.2]','[-0.2,-0.05]','[-0.05,0.05]','[0.05,0.2]','[0.2,0.4]','[0.4,0.6]','[0.6,0.8]','[0.8,1]'])
sentiment_techSupport_df.groupby('compound_group').compound.count().plot(kind='bar',rot=20)
plt.title('Tech Support')
plt.show()
sentiment_mentalHealth_df = readData(inputFile='../analysisResult/mentalhealth_sentiment.json')
print(sentiment_mentalHealth_df)
sentiment_mentalHealth_df['compound_group'] = pd.cut(sentiment_mentalHealth_df['compound'],bins=[-1,-0.8,-0.6,-0.4,-0.2,-0.05,0.05,0.2,0.4,0.6,0.8,1],labels=['[-1,-0.8]','[-0.8,-0.6]','[-0.6,-0.4]','[-0.4,-0.2]','[-0.2,-0.05]','[-0.05,0.05]','[0.05,0.2]','[0.2,0.4]','[0.4,0.6]','[0.6,0.8]','[0.8,1]'])
sentiment_mentalHealth_df.groupby('compound_group').compound.count().plot(kind='bar',rot=20)
plt.title('Mental Health')
plt.show()

# Group by time
time_techSupport_df = groupByHour(techSupport_df)
print(time_techSupport_df)
sentimentAnalysisWithTime(time_techSupport_df,'../analysisResult/time_tectsupport_sentiment.json')

time_mentalHealth_df = groupByHour(mentalHealth_df)
print(time_mentalHealth_df)
sentimentAnalysisWithTime(time_mentalHealth_df,'../analysisResult/time_mentalhealth_sentiment.json')

# get sentiment result
time_sentiment_techSupport_df = readData(inputFile='../analysisResult/time_tectsupport_sentiment.json')
print(time_sentiment_techSupport_df)
time_sentiment_techSupport_df.plot(x='time', y=['neg', 'neu', 'pos', 'compound'],rot=10)
plt.title('Tech Support')
plt.show()
time_sentiment_mentalHealth_df = readData(inputFile='../analysisResult/time_mentalhealth_sentiment.json')
print(time_sentiment_mentalHealth_df)
time_sentiment_mentalHealth_df.plot(x='time', y=['neg', 'neu', 'pos', 'compound'],rot=10)
plt.title('Mental Health')
plt.show()




