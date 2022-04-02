from empath import Empath
import json
import os
import sys
import pandas as pd

def main():
    fn = ""
    sympathyCount = 0.0
    emotionalCount = 0.0
    communicationCount = 0.0
    neglectCount = 0.0
    swearingTermsCount = 0.0
    negativeEmotionCount = 0.0
    positiveEmotionCount = 0.0

    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "../data/techsupport.json"
    if os.path.exists(fn):
        with open(fn, 'r') as json_file:
            datas = json.load(json_file)
            result = []
            for data in datas:
                text = data["text"]
                lexicon = Empath()
                result.append(lexicon.analyze(text, categories=["sympathy", "emotional", "communication", "neglect", "swearing_terms", "negative_emotion", "positive_emotion", "hate"], normalize=True))
            jsonStr = json.dumps(result)
            #print(jsonStr)

            with open('../analysisResult/sample.json', "w") as outfile:
                outfile.write(jsonStr)

        with open('../analysisResult/sample.json', 'r') as json_file:
            analyses = json.load(json_file)

        for index in analyses:
            sympathyCount = sympathyCount + index['sympathy']
            emotionalCount = emotionalCount + index['emotional']
            communicationCount = communicationCount + index['communication']
            neglectCount = neglectCount + index['neglect']
            swearingTermsCount = swearingTermsCount + index['swearing_terms']
            negativeEmotionCount = negativeEmotionCount + index['negative_emotion']
            positiveEmotionCount = positiveEmotionCount + index['positive_emotion']
        results = {}
        results['Sympathy'] = sympathyCount/len(analyses)
        print(sympathyCount/len(analyses))

        results['Emotional'] = emotionalCount/len(analyses)
        print(emotionalCount/len(analyses))

        results['Communication'] = communicationCount/len(analyses)
        print(communicationCount/len(analyses))

        results['Neglect'] = neglectCount/len(analyses)
        print(neglectCount/len(analyses))

        results['Swearing'] = swearingTermsCount/len(analyses)
        print(swearingTermsCount/len(analyses))

        results['NegativeEmotion'] = negativeEmotionCount/len(analyses)
        print(negativeEmotionCount/len(analyses))

        results['PositiveEmotion'] = positiveEmotionCount/len(analyses)
        print(positiveEmotionCount/len(analyses))

        with open("../analysisResult/EmpathResult.json", "w") as file:
            file.write(json.dumps(results))

if __name__ == "__main__":
    main()