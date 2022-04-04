# -*- coding = utf-8 -*-
# @Time : 29/03/2022 18:19
# @Author : Yan Zhu
# @File : BasicAnalytics.py
# @Software : PyCharm
import json
import nltk
from collections import Counter
from stylecloud import gen_stylecloud


data_file = '../data/clean_mentalhealth.json'
data_file_t = '../data/clean_techsupport.json'


def getText(text):
    text = text.lower()
    for ch in '!"$&()*+,-./<=>?@[\\]^_{}|~;`':
        text = text.replace(ch, " ")
    return text


def count_i_we_them():
    with open(data_file) as f:
        result = json.load(f)
        for post in result:
            text = getText(post["text"])
            words = text.split()
            counts = {"i":0, "we": 0, "them": 0}
            for word in words:
                if word == 'i' or word == 'I':
                    counts["i"] += 1
                elif word == 'we' or word == 'We':
                    counts["we"] += 1
                elif word == 'them' or word == 'Them':
                    counts["them"] += 1
                print(counts)


def length_posts():
    with open(data_file) as f:
        result = json.load(f)
        for post in result:
            text = getText(post["text"])
            print(len(text))

# Nouns: NN,NNS,NNP,NNPS
# Pronouns: PRP, PRP$
# Adjectives: JJ, JJR,JJS
# Numeral: CD
# Verbs: VB,VBD,VBG,VBN,VBP,VBZ
# Adverbs: RB,RBR,RBS
def adjective_verb():
    with open(data_file) as f:
        result = json.load(f)
        for post in result:
            text = getText(post["text"])
            text = nltk.word_tokenize(text)
            tagged = nltk.pos_tag(text)
            counts = Counter(tag for word, tag in tagged)
            print("adjective:" + str(counts['JJ'] + counts['JJR'] + counts['JJS'])+ "  noun:" + str(counts['NN'] + counts['NNS'] + counts['NNP'] + counts['NNPS']))

# VB     Verb, base form
# VBD     Verb, past tense
# VBG     Verb, gerund or present participle
# VBN     Verb, past participle
def verb_tense():
    with open(data_file) as f:
        result = json.load(f)
        for post in result:
            text = getText(post["text"])
            text = nltk.word_tokenize(text)
            tagged = nltk.pos_tag(text)
            counts = Counter(tag for word, tag in tagged)
            print("Base form: " + str(counts['VB']))
            print("Past tense: " + str(counts['VBD']))
            print("Gerund or present participle: " + str(counts['VBG']))
            print("Past participle: " + str(counts['VBN']))

def user_similarity():
    return

def generate_word_cloud():
    with open(data_file_t) as f:
        result = json.load(f)
        text = ""
        for post in result:
            text +=  getText(post["text"])
        gen_stylecloud(text,
                       icon_name='fas fa-circle'
                       )


if __name__ == "__main__":
    # count_i_we_them()
    # length_posts()
    # adjective_verb()
    # verb_tense()
    generate_word_cloud()
