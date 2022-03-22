import stanza
from stanza.server import CoreNLPClient


def try_stanza_pipeline(text):
    nlp = stanza.Pipeline(
        'en', processors="tokenize,mwt,pos,lemma,depparse, constituency")
    doc = nlp(text)
    print(doc)

    for sentence in doc.sentences:
        print(sentence.ents)
        print(sentence.dependencies)


def try_corenlp_client(text):
    # Construct a CoreNLPClient with some basic annotators and a memory allocation of 4GB
    with CoreNLPClient(
            annotators=['tokenize', 'ssplit', 'pos', 'lemma',
                        'ner'], memory='4G') as client:
        print(client)

        # Annotate some text
        doc = client.annotate(text)
        print(doc)

        # get the first sentence
        sentence = doc.sentence[0]

        # get the constituency parse of the first sentence
        constituency_parse = sentence.parseTree
        print(constituency_parse)

        print(sentence.basicDependencies)


def main():
    text = 'My name is Mark and I was born in Australia.'
    try_stanza_pipeline(text)
    try_corenlp_client(text)


if __name__ == "__main__":
    main()
