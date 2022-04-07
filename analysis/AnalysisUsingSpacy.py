import spacy, sys, os, json

def calculateFormalityOfText():
    fn = ""
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "data/techsupport.json"
    if os.path.exists(fn):
        with open(fn, 'r') as json_file:
            datas = json.load(json_file)
            # Load English tokenizer, tagger, parser and NER
            nlp = spacy.load("en_core_web_sm")
            noun_freq = 0
            adjective_freq = 0
            preposition_freq = 0
            determiner_freq = 0
            pronoun_freq = 0
            verb_freq = 0
            adverb_freq = 0
            interjection_freq = 0

            for data in datas:
                text = data["text"]
                doc = nlp(text)

                # Analyze syntax
                #calculate nonun frequency
                noun = [token.lemma_ for token in doc if token.pos_ == "NOUN"]
                if len(noun) != 0:
                    noun_freq = noun_freq + len(noun[0])

                #calculate adjective frequency
                adjective = [token.lemma_ for token in doc if token.pos_ == "ADJ"]
                if len(adjective) != 0:
                    adjective_freq = adjective_freq + len(adjective[0])

                #calculate preposition frequency
                preposition = [token.tag_ for token in doc if token.tag_ == 'IN']
                if len(preposition) != 0:
                    preposition_freq = preposition_freq + len(preposition[0])

                #calculate article frequency
                determiner = [token.tag_ for token in doc if token.tag_ == 'DT']
                if len(determiner) != 0:
                    determiner_freq = determiner_freq + len(determiner[0])

                #calculate pronoun frequency
                pronoun = [token.lemma_ for token in doc if token.pos_ == "PRON"]
                if len(pronoun) != 0:
                    pronoun_freq = pronoun_freq + len(pronoun[0])

                #calculte verb freuency
                verb = [token.lemma_ for token in doc if token.pos_ == "VERB"]
                if len(verb) != 0:
                    verb_freq = verb_freq + len(verb[0])

                #calculate adverb frequency
                adverb = [token.tag_ for token in doc if token.tag_ == 'ADV']
                if len(adverb) != 0:
                    adverb_freq = adverb_freq + len(adverb[0])

                #calculate interjection frequency
                interjection = [token.lemma_ for token in doc if token.pos_ == "INTJ"]
                if len(interjection) != 0:
                    interjection_freq = interjection_freq + len(interjection[0])

            #F = (noun frequency + adjective freq. + preposition freq. +article freq. − pronoun freq. − verb freq. − adverb freq. − interjection freq. + 100)/2
            print("Noun freq:" + str(noun_freq))
            print("Adj freq:" + str(adjective_freq))
            print("preposition freq:" + str(preposition_freq))
            print("Determiner freq:" + str(determiner_freq))
            print("Pronoun Freq:" + str(pronoun_freq))
            print("verb freq:" + str(verb_freq))
            print("adverb freq:" + str(adverb_freq))
            print("interjection freq:" + str(interjection_freq))

            f_count = (noun_freq + adjective_freq + preposition_freq + determiner_freq - pronoun_freq - verb_freq - adverb_freq - interjection_freq + 100) / 2
            print("Formality of text:" + str(f_count))

            #with open("../analysisResult/spacy.json", "w") as file:
            #    file.write(json.dumps(results))

if __name__ == "__main__":
    calculateFormalityOfText()