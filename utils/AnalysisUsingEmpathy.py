from empath import Empath
import json
import os
import sys
import pandas as pd

def main():
    fn = sys.argv[1]
    if os.path.exists(fn):
        with open(fn, 'r') as json_file:
            datas = json.load(json_file)
            result = []
            for data in datas:
                text = data["text"]
                lexicon = Empath()
                result.append(lexicon.analyze(text, categories=["sympathy", "emotional", "communication", "pain", "neglect", "negative_emotion"], normalize=True))
            pd.DataFrame(result).to_csv('analysisResult/result1.csv',index=False)

if __name__ == "__main__":
    main()