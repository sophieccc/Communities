import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def main():
    input_file = open('../techsupport.json', 'r')
    output_file = open('../analysisResult/techSupportSentiment.json', 'w')
    result_list = []
    datas = json.load(input_file)
    for data in datas:
        text = data["text"]
        result = {'text':text}
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(text)
        result.update(vs)
        result_list.append(result)
    json.dump(result_list, output_file)

if __name__ == "__main__":
    main()

