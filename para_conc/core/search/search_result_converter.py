# -*- coding: utf-8 -*-
from para_conc.core.search.search import SearchResult, ArticleResult


class SearchResultConverter:
    def __init__(self):
        pass

    def convert(self, search_result: SearchResult,
                show_context_original: bool,
                show_context_translation: bool,
                show_source_author: bool,
                show_source_translator: bool,
                show_source_title: bool):
        raise NotImplementedError()

    def source_note(self, article_result: ArticleResult, show_title: bool, show_author: bool):
        if article_result.key[0] == 's':
            return self._source_note_en(article_result, show_title, show_author)
        return self._source_note_zh(article_result, show_title, show_author)

    def _source_note_en(self, article_result: ArticleResult, show_title: bool, show_author: bool):
        # 篇章标题 等于 语料结果的篇章标题
        chapter_title = article_result.chapter_title
        # 如果篇章标题为"FULL TEXT"或者篇章标题语料结果标题，篇章标题为空
        if chapter_title == 'FULL TEXT' or chapter_title.lower() == article_result.title.lower():
            chapter_title = ''
        result = ''
        if show_title:
            result += chapter_title + ' from ' + article_result.title
        if show_author:
            result += ' by ' + article_result.author
        return result.strip()

    def _source_note_zh(self, article_result: ArticleResult, show_title: bool, show_translator: bool):
        chapter_title = ''
        if article_result.chapter_title not in ('全文', 'FULL TEXT', article_result.title):
            chapter_title = '：' + article_result.chapter_title
        result = ''
        if show_title:
            result += '《' + article_result.title + chapter_title + '》'
        if show_translator:
            result += article_result.translator + '译'
        return result.strip()
