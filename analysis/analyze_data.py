import json
import string
from collections import Counter
import stanza
import textstat
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.parse import CoreNLPDependencyParser, CoreNLPParser
from nltk.tree import Tree


def combine_text(data):
    text = ""
    for item in data:
        text += item["text"]
        text += " "
    with open("data/all_text.json", "w") as file:
        all_text = {"text": text}
        file.write(json.dumps(all_text))


def get_lexicon_stats(data):
    uniques = set()
    word_count = 0
    word_sum, sentence_sum = 0, 0
    syllable_sum, letter_count, polysyllab_count, character_sum = 0, 0, 0, 0
    num_posts = len(data)
    for item in data:
        value = item["text"]
        syllable_sum += textstat.textstat.syllable_count(value)
        word_sum += textstat.textstat.lexicon_count(value)
        sentence_sum += textstat.textstat.sentence_count(value)
        character_sum += textstat.textstat.char_count(value)
        letter_count += textstat.textstat.avg_letter_per_word(value)
        polysyllab_count += textstat.textstat.polysyllabcount(value)
        tokens = tokenize.word_tokenize(value)
        for token in tokens:
            word_count += 1
            uniques.add(token)
    print("Number of token: {}".format(len(uniques)))
    print("Number of posts: {}".format(num_posts))
    print("Syllables per post: {}".format(syllable_sum / num_posts))
    print("Words per post: {}".format(word_sum / num_posts))
    print("Total sentences: {}".format(sentence_sum))
    print("Sentences per post: {}".format(sentence_sum / num_posts))
    print("Syllables per word: {}".format(syllable_sum / word_sum))
    print("Words per sentence: {}".format(word_sum / sentence_sum))
    print("Characters per word: {}".format(character_sum / word_sum))
    print("Letters per word: {}".format(letter_count / num_posts))
    print("Polysyllabs per post: {}".format(polysyllab_count / num_posts))
    print("Number of unique words: {}".format(len(uniques)))
    print("Overall Type-token ratio: {}".format(len(uniques) / word_count))


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
    get_lexicon_stats(data)
    print("\n")
    for item in data:
        value = item["text"]

        # Example data text is too large, small workaround:
        value = value[0:500]

        parsed = list(parser.parse(value.split()))
        height += parsed[0].height()
        curr_num_nodes, curr_num_s = count_nodes(parsed[0][0], 0, 0)
        num_nodes += curr_num_nodes
        num_s += curr_num_s

    print("Num clauses: {}".format(num_s))
    print("Num nodes: {}".format(num_nodes))
    print("Total height: {}".format(height))
    print("Avg nodes per post: {}".format(num_nodes / len(data)))
    print("Avg height of post: {}".format(height / len(data)))

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
    print("Number of berns: {}".format(verb_count))


def top_words():
    with open('data/all_text.json') as file:
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
        print("Frequency of all words: {}".format(total_frequency))
        print("Frequency of top 10 words: {}".format(top_frequency))
        print("% in text of top 10 words: {}".format(
            (top_frequency / total_frequency) * 100))


def main():
    with open('data/example2.json') as json_file:
        data = json.load(json_file)
        combine_text(data)
        verb_stats(data)
        nltk_stuff(data)
        top_words()


if __name__ == "__main__":
    main()
