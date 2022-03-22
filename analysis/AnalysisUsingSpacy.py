import spacy, sys, os, json

def main():
    fn = ""
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "data/example.json"
    if os.path.exists(fn):
        with open(fn, 'r') as json_file:
            data = json.load(json_file)
            text = data["text"]

            # Load English tokenizer, tagger, parser and NER
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text)

            # Analyze syntax
            results = {}
            results["Noun phrases"] =  [chunk.text for chunk in doc.noun_chunks]
            results["Verbs"] =  [token.lemma_ for token in doc if token.pos_ == "VERB"]
            preps = [token.tag_ for token in doc if token.tag_ == 'PRP']
            results["num preps"] = len(preps)
            with open("analysisResult/spacy.json", "w") as file:
                file.write(json.dumps(results))

if __name__ == "__main__":
    main()