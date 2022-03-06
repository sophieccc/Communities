from empath import Empath
import json
import os
import sys

def main():
    fn = sys.argv[1]
    if os.path.exists(fn):
        with open(fn, 'r') as json_file:
            data = json.load(json_file)
            text = data["text"]
            lexicon = Empath()
            print(lexicon.analyze(text, categories=["sympathy", "emotional", "communication", "pain", "neglect", "negative_emotion"], normalize=True))

if __name__ == "__main__":
    main()