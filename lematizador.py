#!/usr/bin/env python

__author__ = "Martin Kondra"

import nltk
import codecs
from difflib import get_close_matches
import pickle

class Lemmatizer():
    def __init__(self, tagger, debug=False):
        self.tagger = tagger
        self.debug = debug
        
    def build_dicc(self):
        freeling_dicc = codecs.open('dicc.src', 'r', 'utf-8')
        my_dicc = {}
        for line in freeling_dicc:
            line = line.strip().split()
            form = line[0]
            my_dicc[form] = line[1:]
        self.dicc = my_dicc

    def get_lemma(self, word, tag):
        try:
            entry = self.dicc[word]
            #devuelve una lista de tuplas lemma/tag
            lemma_tag_pairs = zip(entry[::2], entry[1::2])
            tags = [i[1] for i in lemma_tag_pairs]
            tag = get_close_matches(tag, tags, cutoff=0.2)[0]
            lemma = [i[0] for i in lemma_tag_pairs if i[1]==tag][0]
            if self.debug:
                print(word)
                print('Pares de lemma/tag posibles:')
                print(lemma_tag_pairs)
                print('Tag elegido:')
                print(tag)
                print('\n')
            return lemma
        except Exception as e:
            return word

    def process(self, text):
        lemmatized_sentences = []
        #text = text.decode('utf-8')
        sentences = nltk.sent_tokenize(text)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        postagged_sentences = [self.tagger.tag(sentence) for sentence in tokenized_sentences]
        for sentence in postagged_sentences:
            s = []
            for i in sentence:
                word = i[0].lower()
                tag = i[1].upper()
                lemma = self.get_lemma(word, tag)
                s.append((word, lemma))
            lemmatized_sentences.append(s)
        return lemmatized_sentences