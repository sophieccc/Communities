import spacy, sys, os, json

def main():
    fn = sys.argv[1]
    if os.path.exists(fn):
        with open(fn, 'r') as json_file:
            data = json.load(json_file)
            text = data["text"]

            # Load English tokenizer, tagger, parser and NER
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text)

            # Analyze syntax
            print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
            print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
            preps = [token.tag_ for token in doc if token.tag_ == 'PRP']
            print(len(preps))

if __name__ == "__main__":
    main()