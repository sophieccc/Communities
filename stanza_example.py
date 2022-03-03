import stanza
from stanza.server import CoreNLPClient


def main():
    nlp = stanza.Pipeline('en', processors="tokenize,mwt,pos,lemma,depparse")
    text = 'My name is Mark and I was born in Australia.'
    doc = nlp(text)
    print(doc)

    for sentence in doc.sentences:
        print(sentence.ents)
        print(sentence.dependencies)

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


if __name__ == "__main__":
    main()