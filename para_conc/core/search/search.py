# -*- coding: utf-8 -*-

from enum import Enum

from para_conc.core.corpus import Article

# 检索方式：普通检索，拓展检索，正则检索
class SearchMode(Enum):    
    NORMAL = 1
    EXTENDED = 2
    REGEX = 3

# 检索范围：全部语料，当前语料，指定作者，指定译者，指定类型
class SearchType(Enum):    
    CORPUS_KEY = 1
    ARTICLE_KEY = 2
    AUTHOR = 3
    TRANSLATOR = 4
    GENRE = 5

# 检索请求:检索词，检索方式，检索范围，当前语料内容(中的全部语料（译本），当前语料（译本）与篇章标题)
class SearchRequest:
    def __init__(self):
        self.q = ''
        self.mode: SearchMode = SearchMode.EXTENDED
        self.type = SearchType.CORPUS_KEY
        self.type_value = ''  # (corpus_key, article_key, chapter_titles) for SearchType.ARTICLE_KEY

# 匹配结果：起止值
class MatchResult:
    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end

# 单个语料结果：键名，标题，作者，译者，篇章标题，句子列表，匹配列表
class ArticleResult:
    def __init__(self):
        self.key = ''
        self.title = ''
        self.author = ''
        self.translator = ''
        self.chapter_title = ''
        self.lines = []
        # 匹配列表用于存贮句子高亮坐标
        self.matches = []
        
    # 从语料类ARTICLE取值：语料键名，标题，作者，译者
    def assign_from(self, article: Article):
        self.key = article.key
        self.title = article.title
        self.author = article.author
        self.translator = article.translator

# 检索结果具体项：单个原文检索结果，所有译文检索结果列表
class SearchResultItem:
    def __init__(self):
        self.original = ArticleResult()
        self.translations = []

# 检索结果列表
class SearchResult:
    def __init__(self):
        self.items = []
