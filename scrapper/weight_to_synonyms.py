import re
import json

import pymorphy2

from wiki_ru_wordnet import WikiWordnet
from nltk.stem.snowball import SnowballStemmer

morph = pymorphy2.MorphAnalyzer()
wiki_wordnet = WikiWordnet()

source_filename = 'anekdot.json'
synonyms_filename = 'synonyms.txt'

with open(source_filename, encoding='UTF-8') as f:
    source_document_json = json.load(f)

# print(source_document_json)

uniq_words = set()

for i in range(len(source_document_json)):
    words = source_document_json[i]['text']
    uniq_words.update(words.split())


def add_value(dict_to_add, key, value):
    if key in dict_to_add:
        if not isinstance(dict_to_add[key], list):
            dict_to_add[key] = [dict_to_add[key]]
        dict_to_add[key].append(value)
    else:
        dict_to_add[key] = value


# making synonyms
with open(synonyms_filename, 'a', encoding='utf-8') as f:
    for i in list(uniq_words):
        synonym_wiki = wiki_wordnet.get_synsets(i)
        if synonym_wiki:
            synonyms_list = synonym_wiki[0].get_words()
            for j, word in enumerate(synonyms_list):
                if len(synonyms_list) != 1:
                    true_word = word.lemma().lower()
                    if j != 0:
                        f.write(f',{true_word}|0.6')
                    else:
                        f.write(f',\n{true_word}|1.0')


# stemmer and lemma
stemmer = SnowballStemmer("russian")
lem = pymorphy2.MorphAnalyzer()
dict_stem = {}
for word in list(uniq_words):
    # stem
    new_word = re.sub("[:|)|!|(|,|.|<|>|?|\"|\[|\]]", "", word).lower()
    stem_syn = stemmer.stem(new_word).lower()
    # lemma
    lemma = lem.parse(new_word)[0].normal_form
    if new_word != stem_syn:
        if stem_syn in dict_stem and new_word not in dict_stem[stem_syn]:
            add_value(dict_stem, stem_syn, new_word)
        else:
            dict_stem[f'{stem_syn}'] = new_word
    if new_word != lemma:
        if lemma in dict_stem and new_word not in dict_stem[lemma]:
            add_value(dict_stem, lemma, new_word)
        else:
            dict_stem[f'{lemma}'] = new_word


with open(synonyms_filename, 'a', encoding='utf-8') as f:
    for i in dict_stem:
        value = dict_stem[i]
        f.write(f'\n{i}|1.0')
        if isinstance(value, list):
            for j in value:
                f.write(f',{j}|0.8')
        elif isinstance(value, str):
            f.write(f',{value}|0.8')