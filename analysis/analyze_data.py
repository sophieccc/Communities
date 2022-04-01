import json
import re
import string
from collections import Counter

import stanza
import textstat
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.parse.corenlp import CoreNLPDependencyParser, CoreNLPParser
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize

# Regular expression for negation.
NEG = r"""(?:^(?:no|not|cant|shouldnt|wont|wouldnt|dont|doesnt|isnt|arent)$)| n't"""
NEG_RE = re.compile(NEG, re.VERBOSE)

def combine_text(data):
    text = ""
    for item in data:
        text += item["text"]
        text += " "
    with open("data/combined_techsupport.json", "w") as file:
        all_text = {"text": text}
        file.write(json.dumps(all_text))

def get_negative_count(text):
    count = 0
    for word in text.split():
        if NEG_RE.search(word):
            count+=1
    return count

def get_lexicon_stats(data):
    uniques = set()
    word_count = 0
    word_sum, sentence_sum = 0, 0
    syllable_sum, letter_count, polysyllab_count, character_sum = 0, 0, 0, 0
    num_posts = len(data)
    neg_count = 0
    for item in data:
        value = item["text"]
        syllable_sum += textstat.textstat.syllable_count(value)
        word_sum += textstat.textstat.lexicon_count(value)
        sentence_sum += textstat.textstat.sentence_count(value)
        character_sum += textstat.textstat.char_count(value)
        letter_count += textstat.textstat.avg_letter_per_word(value)
        polysyllab_count += textstat.textstat.polysyllabcount(value)
        neg_count += get_negative_count(value)
        tokens = tokenize.word_tokenize(value)
        for token in tokens:
            word_count += 1
            uniques.add(token)
    results = {}
    results["Number of token"] = len(uniques)
    results["Number of posts"] = num_posts
    results["Syllables per post"] = syllable_sum / num_posts
    results["Words per post"] = word_sum / num_posts
    results["Total sentences"] = sentence_sum
    results["Sentences per post"] = sentence_sum / num_posts
    results["Syllables per word"] = syllable_sum / word_sum
    results["Words per sentence"] = word_sum / sentence_sum
    results["Characters per word"] = character_sum / word_sum
    results["Letters per word"] = letter_count / num_posts
    results["Negative count"] = neg_count
    results["Polysyllabs per post"] = polysyllab_count / num_posts
    results["Overall Type-token ratio"] = len(uniques) / word_count
    return results


def count_nodes(tree, count, num_s):
    count += 1
    if tree.label().startswith("S"):
        num_s += 1
    for subtree in tree:
        if type(subtree) == Tree:
            count, num_s = count_nodes(subtree, count, num_s)
    return count, num_s


def nltk_stuff(data):
    parser = CoreNLPParser(url='http://localhost:9001')
    num_nodes = 0
    num_s = 0
    height = 0
    for item in data:
        value = item["text"]
        for sent in sent_tokenize(value):
            small_sents = [sent[i:i + 400] for i in range(0, len(sent), 400)]
            for small_sent in small_sents:
                parsed = list(parser.raw_parse(small_sent))
                height += parsed[0].height()
                curr_num_nodes, curr_num_s = count_nodes(parsed[0][0], 0, 0)
                num_nodes += curr_num_nodes
                num_s += curr_num_s

    results = {}
    results["Num clauses"] = num_s
    results["Num nodes"] = num_nodes
    results["Total height"] = height
    results["Avg nodes per post"] = num_nodes / len(data)
    results["Avg clauses per post"] = num_s / len(data)
    results["Avg height of post"] = height / len(data)
    return results

    # dep_parser = CoreNLPDependencyParser(url='http://localhost:9001')
    # dep_parsed = dep_parser.parse('The quick brown fox jumps over the lazy dog.'.split())
    # dep_results = [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in dep_parsed]
    # print(dep_results)


def verb_stats(data):
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos')
    verb_count = 0
    for item in data:
        value = item["text"]
        doc = nlp(value)
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.upos.startswith("V"):
                    verb_count += 1
    return {"verb count": verb_count}


def top_words():
    with open('data/combined_mentalhealth.json') as file:
        text = json.load(file)["text"]
        words = tokenize.word_tokenize(text)
        no_stopwords = [
            word for word in words if not (word in stopwords.words())
            and not (word in string.punctuation)
        ]
        counter = Counter(no_stopwords)
        total_frequency = sum(counter.values())
        top_frequency = 0
        for word in counter.most_common(10):
            top_frequency += word[1]
        results = {}
        results["Frequency of all words"] = total_frequency
        results["Frequency of top 10 words"] = top_frequency
        results["percent of text is top 10 words"] = (top_frequency /
                                                      total_frequency) * 100
        return results


def main():
    with open('data/clean_mentalhealth.json') as json_file:
        data = json.load(json_file)
        results = {}
        # combine_text(data)

        print("Creating lexicon stats...\n")
        results["lexicon stats"] = get_lexicon_stats(data)

        print("Creating verb stats...\n")
        results["verb stats"] = verb_stats(data)

        print("Creating top word stats...\n")
        results["top words"] = top_words()

        print("Creating nltk stats...\n")
        results["ntlk stats"] = nltk_stuff(data)

        with open("analysisResult/analyze_data_mentalhealth.json",
                  "w") as file:
            file.write(json.dumps(results))


if __name__ == "__main__":
    main()
