#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Martin Kondra"

import nltk
import codecs
from difflib import get_close_matches
import pickle

# POSTagger
maxent_tagger = pickle.load(open("maxent_taggerEagle.p", "rb"))

def build_dicc():
    freeling_dicc = codecs.open('dicc.src', 'r', 'utf-8')
    my_dicc = {}
    for line in freeling_dicc:
        line = line.strip().split()
        form = line[0]
        my_dicc[form] = line[1:]
    print('Dumping pickle...')
    pickle.dump(my_dicc, open("freeling_dicc.p", "wb"))

#my_dicc = build_dicc()
my_dicc = pickle.load(open("freeling_dicc.p", "rb")) #lista de diccionarios (sentences)

def processing(sample):
    lemmatized_sentences = []
    sample = sample.decode('utf-8')
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    postagged_sentences = [maxent_tagger.tag(sentence) for sentence in tokenized_sentences]
    #print tokenized_sentences
    print(postagged_sentences)
    for sentence in postagged_sentences:
        s = []
        for i in sentence:
            word = i[0].lower()
            tag = i[1].upper()
            lemma = get_lemma(word, tag)
            s.append((word, lemma))
        lemmatized_sentences.append(s)
    return lemmatized_sentences

def get_lemma_and_pos(word, tag):
    try:
        entry = my_dicc[word]
        lemma_tag_pairs = zip(entry[::2], entry[1::2]) #devuelve una lista de tuplas lemma/tag
        tags = [i[1] for i in lemma_tag_pairs]
        tag = get_close_matches(tag, tags)[0]
        lemma = [i[0] for i in lemma_tag_pairs if i[1]==tag][0]
        return word, lemma, tag
    except:
        return word, word, tag

def get_lemma(word, tag):
    try:
        entry = my_dicc[word]
        lemma_tag_pairs = zip(entry[::2], entry[1::2]) #devuelve una lista de tuplas lemma/tag
        tags = [i[1] for i in lemma_tag_pairs]
        tag = get_close_matches(tag, tags)[0]
        lemma = [i[0] for i in lemma_tag_pairs if i[1]==tag][0]
        return lemma
    except:
        return word

sample = u"Las calles de Buenos Aires tienen esas casas azules."
print(processing(sample))
