import stanza

def main():
    nlp = stanza.Pipeline('en', processors="tokenize,mwt,pos,lemma,depparse")
    doc = nlp('My name is Mark and I was born in Australia.')
    print(doc)


if __name__ == "__main__":
    main()