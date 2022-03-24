import json
import re
from venv import create
from autocorrect import Speller
from emot.emo_unicode import EMOTICONS_EMO

emot_words = {}
valid_token = re.compile(r"^[\da-zA-Z0-1\s_\-\(\)\/!\.,\?]+$")


# This function removes any emojis and replaces usernames
# with a person's name ('Sarah'). If there are multiple usernames
# in a row, they will all be replaced by one name.
def remove_usernames_and_emojis(data):
    for item in data:
        value = item["text"]
        no_user = " ".join(value.split())
        no_user2 = re.sub('@[a-zA-Z0-9_]*', '  ', no_user)
        no_user3 = re.sub(' {2,}', ' Sarah ', no_user2)
        no_emojis = no_user3.encode('ascii', 'ignore').decode('ascii')
        no_extra_spaces = " ".join(no_emojis.split())
        item["text"] = re.sub('^Sarah', '', no_extra_spaces)


def remove_links(data):
    for item in data:
        value = item["text"]
        replaced = re.sub('https://[a-zA-Z]*.[a-zA-Z0-9/?&.;=-]*', '  ', value)
        item["text"] = re.sub(' {2,}', ' ', replaced)


def correct_spelling(data):
    spell = Speller(fast=True)
    for item in data:
        value = item["text"]
        no_sym_emojis = re.sub(r' \:\) | \:\( | \:D | \:P | \:o | xD | \:\/ ',
                               ' ', value)
        corrected = spell(no_sym_emojis)
        item["text"] = " ".join(corrected.split())


def remove_hashtags(data):
    for item in data:
        value = item["text"]
        no_hashtags = value
        no_hashtags = re.sub(r'(#[a-zA-Z]*[\. ]*)+\Z', '', value)
        no_hash_symbols = re.sub('#', '', no_hashtags)
        normal_spaces = " ".join(no_hash_symbols.split())
        if (normal_spaces.endswith('.') or normal_spaces.endswith('!')
                or normal_spaces.endswith('?')) is not True:
            normal_spaces += "."
        item["text"] = normal_spaces

# replaces a wide range of emoticons with word-versions describing them.
def replace_emoticons(data):
    for item in data:
        value = item["text"]
        for emot in emot_words:
            value = re.sub(re.escape(emot), emot_words[emot], value)
        item["text"] = value


def create_emot_dict():
    for emot in EMOTICONS_EMO:
        repl = " " + "_".join(EMOTICONS_EMO[emot].replace(",",
                                                          "").split()) + " "
        emot_words[emot] = repl

def main():
    create_emot_dict()
    with open('data/mentalhealth.json') as json_file:
        data = json.load(json_file)
        remove_usernames_and_emojis(data)
        remove_links(data)
        correct_spelling(data)
        remove_hashtags(data)
        replace_emoticons(data)
        with open('data/clean_mentalhealth.json', 'a') as f:
            json.dump(data, f)


if __name__ == "__main__":
    main()