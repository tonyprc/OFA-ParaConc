#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Tony Chang (42716403@qq.com)

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
        chapter_title = article_result.chapter_title
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
