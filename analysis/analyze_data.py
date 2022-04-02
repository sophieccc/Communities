import itertools
import json
import re
import string
from collections import Counter
from operator import itemgetter

import stanza
import textstat
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.parse.corenlp import CoreNLPDependencyParser, CoreNLPParser
from nltk.tokenize import sent_tokenize
from nltk.tree import Tree

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
    for word in text:
        if NEG_RE.search(word):
            count += 1
    return count


def get_advice_count(text):
    count = 0
    for word in text:
        if word in [
                "should", "suggest", "advise", "would", "ought", "advice",
                "help", "question", "answer", "opinion", "recommend"
        ]:
            count += 1
    return count


def get_avg_deviation(data):
    uniques = set()
    token_count = 0
    word_sum, sentence_sum, character_sum = 0, 0, 0
    num_posts = len(data)
    sent_per_post, word_per_sent, word_per_post, char_per_word = [], [], [], []
    type_token_ratio = []
    for item in data:
        value = item["text"]
        num_sent = textstat.textstat.sentence_count(value)
        sentence_sum += num_sent
        sent_per_post.append(num_sent)

        num_words = textstat.textstat.lexicon_count(value)
        word_sum += num_words
        word_per_post.append(num_words)
        word_per_sent.append(word_sum / sentence_sum)

        num_chars = textstat.textstat.char_count(value)
        character_sum += num_chars
        char_per_word.append(character_sum / word_sum)

        tokens = tokenize.word_tokenize(value)
        post_uniques = set()
        post_token_count = 0
        for token in tokens:
            post_token_count += 1
            uniques.add(token)
            post_uniques.add(token)
        token_count += post_token_count
        type_token_ratio.append(len(post_uniques) / post_token_count)

    mean_sent_per_post = sentence_sum / num_posts
    mean_word_per_sent = word_sum / sentence_sum
    mean_word_per_post = word_sum / num_posts
    mean_char_per_word = character_sum / word_sum
    mean_type_token_ratio = len(uniques) / token_count

    std_dev_s_per_p = 0
    std_dev_w_per_s = 0
    std_dev_w_per_p = 0
    std_dev_c_per_w = 0
    std_dev_ttr = 0
    for sent, wordsent, wordpost, char, ttr in zip(sent_per_post,
                                                   word_per_sent,
                                                   word_per_post,
                                                   char_per_word,
                                                   type_token_ratio):
        std_dev_s_per_p += abs(sent - mean_sent_per_post)
        std_dev_w_per_s += abs(wordsent - mean_word_per_sent)
        std_dev_w_per_p += abs(wordpost - mean_word_per_post)
        std_dev_c_per_w += abs(char - mean_char_per_word)
        std_dev_ttr += abs(ttr - mean_type_token_ratio)

    results = {}
    results["std dev sentences per post"] = std_dev_s_per_p / num_posts
    results["std dev words per sentence"] = std_dev_w_per_s / num_posts
    results["std dev words per post"] = std_dev_w_per_p / num_posts
    results["std dev characters per word"] = std_dev_c_per_w / num_posts
    results["std dev type token ratio"] = std_dev_ttr / num_posts

    total_deviation = std_dev_s_per_p + std_dev_w_per_s + std_dev_w_per_p + std_dev_c_per_w + std_dev_ttr
    avg_standard_deviation = total_deviation / (num_posts * 5)
    results["average user style std dev"] = avg_standard_deviation
    return results


def get_lexicon_stats(data):
    uniques = set()
    token_count = 0
    word_sum, sentence_sum = 0, 0
    syllable_sum, letter_count, polysyllab_count, character_sum = 0, 0, 0, 0
    num_posts = len(data)
    neg_count = 0
    advice_count = 0
    word_count = 0
    for item in data:
        value = item["text"]
        syllable_sum += textstat.textstat.syllable_count(value)
        word_sum += textstat.textstat.lexicon_count(value)
        sentence_sum += textstat.textstat.sentence_count(value)
        character_sum += textstat.textstat.char_count(value)
        letter_count += textstat.textstat.avg_letter_per_word(value)
        polysyllab_count += textstat.textstat.polysyllabcount(value)

        words = value.split()
        word_count += len(words)
        neg_count += get_negative_count(words)
        advice_count += get_advice_count(words)
        tokens = tokenize.word_tokenize(value)
        for token in tokens:
            token_count += 1
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
    results["Negative percent of all words"] = neg_count / word_count
    results["Advice percent of all words"] = advice_count / word_count
    results["Polysyllabs per post"] = polysyllab_count / num_posts
    results["Overall Type-token ratio"] = len(uniques) / token_count
    return results


def count_nodes(tree, count, num_s):
    count += 1
    if tree.label().startswith("S"):
        num_s += 1
    for subtree in tree:
        if type(subtree) == Tree:
            count, num_s = count_nodes(subtree, count, num_s)
    return count, num_s


def get_support_patterns():
    pronouns = ["i", "we", "you"]
    aux_words = ["can", "could", "do", "would", "will", "may"]
    pos_verbs = ["know", "feel", "understand", "sense", "support"]
    advice_words = ["should", "must", "need", "might"]
    opinion_verbs = ["recommend", "advise", "suggest", "advocate", "request"]

    emo_permut = list(itertools.product(pronouns[0:2], aux_words, pos_verbs))
    emo_permut = emo_permut + list(itertools.product(pronouns[0:2], pos_verbs))

    info_permut = list(
        itertools.product([pronouns[0]], aux_words, opinion_verbs))
    info_permut = info_permut + list(
        itertools.product([pronouns[0]], opinion_verbs))
    info_permut = info_permut + list(
        itertools.product([pronouns[2]], advice_words))

    for idx, emo in enumerate(emo_permut):
        emo_permut[idx] = ' '.join(word for word in emo)
    for idx, info in enumerate(info_permut):
        info_permut[idx] = ' '.join(word for word in info)
    return emo_permut, info_permut


def calculate_support_types(data):
    emo_patterns, info_patterns = get_support_patterns()
    emo_index = 0
    info_index = 0
    for item in data:
        value = item["text"]
        for patt in emo_patterns:
            emo_index += value.count(patt)
        for patt in info_patterns:
            info_index += value.count(patt)
    results = {}
    results["Emotional support index"] = emo_index / len(data)
    results["Informational support index"] = info_index / len(data)
    return results


def count_pronouns_and_sentiment(data):
    indiv_pronouns = ["i", "me", "myself", "my", "mine"]
    indiv_count = 0

    in_group_count = 0
    in_group_pronouns = ["we", "us", "ourselves", "our", "ours"]

    out_group_count = 0
    out_group_pronouns = ["they", "them", "themselves", "their", "theirs"]

    total_sentiment = 0
    sentiment_count = 0
    nlp = stanza.Pipeline('en', processors="tokenize,mwt,pos,sentiment")
    for item in data:
        value = item["text"]
        doc = nlp(value)
        for i, sentence in enumerate(doc.sentences):
            sentiment_count += 1
            total_sentiment += sentence.sentiment
            for word in sentence.words:
                if word.upos == "PRON":
                    if word.text.lower() in indiv_pronouns:
                        indiv_count += 1
                    elif word.text.lower() in in_group_pronouns:
                        in_group_count += 1
                    elif word.text.lower() in out_group_pronouns:
                        out_group_count += 1
    results = {}
    results[
        "Average sentiment for sentences"] = total_sentiment / sentiment_count
    results["I (etc.) pronouns"] = indiv_count
    results["We (etc.) pronouns"] = in_group_count
    results["They (etc.) pronouns"] = out_group_count
    results[
        "Added up pronouns"] = indiv_count + in_group_count + out_group_count
    return results


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


def average_user_posts(data):
    num_authors = 0
    total_scores = 0
    total_comments = 0
    # Sort post data by `author` key.
    sorted_data = sorted(data, key=itemgetter('author'))

    # Display data grouped by `author`
    for key, value in itertools.groupby(sorted_data, key=itemgetter('author')):
        num_authors += 1
        for item in value:
            total_scores += item.get("score")
            total_comments += item.get("num_comments")

    results = {"Avg posts per author": len(data) / num_authors}
    results["Avg score"] = total_scores / len(data)
    results["Avg num comments"] = total_comments / len(data)
    return results


def main():
    with open('data/clean_techsupport.json') as json_file:
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

        print("Creating pronoun and sentiment stats...\n")
        results["pronoun_and_sentiment_stats"] = count_pronouns_and_sentiment(
            data)

        print("Creating author stats...\n")
        results["author data"] = average_user_posts(data)

        print("Getting post style deviation...\n")
        results["avg deviation data"] = get_avg_deviation(data)

        print("Getting support type index stats...\n")
        results["Support index data"] = calculate_support_types(data)

        with open("analysisResult/analyze_data_mentalhealth.json",
                  "w") as file:
            file.write(json.dumps(results))


if __name__ == "__main__":
    main()
