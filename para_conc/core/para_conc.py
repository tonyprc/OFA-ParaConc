# -*- coding: utf-8 -*-
# compiled by Tony96163

import json
import os

from para_conc.core.corpus import Corpus
from para_conc.core.search.search import SearchRequest, SearchResult
from para_conc.core.search.searcher import Searcher
from .pinyin_sorter import Pinyin


class ParaConc:
    def __init__(self):
        self._currentDir = os.getcwd()
        self._dataDir = os.path.join(self._currentDir, "app_data")
        self._corpusRoot = os.path.join(self._dataDir, "corpus")
        self._workFileDir = os.path.join(self._dataDir, "workfiles")

        self._name_key_dict = {}

        self.corpora = []
        self.titles = []
        self.authors = []
        self.translators = []
        self.genres = []

        self._searcher = Searcher()

        self.reload()

    def reload(self):
        # the en lemma file adopted here is cited from antConc
        self._searcher.en_lemma_dict.clear()
        filename = os.path.join(self._workFileDir, 'en_lemma.txt')
        with open(filename, 'r', encoding='utf-8-sig') as f:
            tag_corpus = [line.strip() for line in f.readlines()]
            for line in tag_corpus:
                word = line.split('\t')[0]
                lemmas = line.split('\t')[-1].split(',')
                self._searcher.en_lemma_dict[word] = lemmas

        json_dict_list = os.listdir(self._corpusRoot)
        self.corpora.clear()
        for dict_item in json_dict_list:
            dict_item_id = os.path.join(self._corpusRoot, dict_item)
            with open(dict_item_id, mode='r', encoding='utf-8-sig') as f:
                self.corpora.append(Corpus(json.load(f)))

        titles = []
        authors = set()
        translators = set()
        genres = set()
        for corpus in self.corpora:
            titles.append(corpus.original.title)
            authors.add(corpus.original.author)
            translators.update(corpus.translators)
            genres.add(corpus.original.genre)
        self.titles = sorted(titles)
        self.authors = sorted(authors)
        pinyin = Pinyin()
        temp = [(pinyin.get_pinyin(item), item) for item in translators]
        self.translators = [char for (pinyin, char) in sorted(temp, key=lambda x: x[0])]
        self.genres = sorted(genres)

    def corpus(self, title):
        for corpus in self.corpora:
            if title == corpus.original.title:
                return corpus
        return None

    def name_key(self, en_text):
        return self._name_key_dict[en_text]

    def search(self, req: SearchRequest) -> SearchResult:
        return self._searcher.search(self.corpora, req)
