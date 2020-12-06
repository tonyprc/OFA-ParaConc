# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Tony96163 (42716403@qq.com)

# Disclaimer:

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from enum import Enum

from para_conc.core.corpus import Article

class SearchMode(Enum):
    NORMAL = 1
    EXTENDED = 2
    REGEX = 3

class SearchType(Enum):
    CORPUS_KEY = 1
    ARTICLE_KEY = 2
    AUTHOR = 3
    TRANSLATOR = 4
    GENRE = 5

class SearchRequest:
    def __init__(self):
        self.q = ''
        self.mode: SearchMode = SearchMode.EXTENDED
        self.type = SearchType.CORPUS_KEY
        self.type_value = ''  # (corpus_key, article_key, chapter_titles) for SearchType.ARTICLE_KEY

class MatchResult:
    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end

class ArticleResult:
    def __init__(self):
        self.key = ''
        self.title = ''
        self.author = ''
        self.translator = ''
        self.chapter_title = ''
        self.lines = []
        self.matches = []
        
    def assign_from(self, article: Article):
        self.key = article.key
        self.title = article.title
        self.author = article.author
        self.translator = article.translator

class SearchResultItem:
    def __init__(self):
        self.original = ArticleResult()
        self.translations = []

class SearchResult:
    def __init__(self):
        self.items = []
