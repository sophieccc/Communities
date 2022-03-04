import json
import re
from autocorrect import Speller


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


def main():
    with open('data/example2.json') as json_file:
        data = json.load(json_file)
        remove_usernames_and_emojis(data)
        remove_links(data)
        correct_spelling(data)
        remove_hashtags(data)
        with open('data/clean_example2.json', 'a') as f:
            json.dump(data, f)


if __name__ == "__main__":
    main()