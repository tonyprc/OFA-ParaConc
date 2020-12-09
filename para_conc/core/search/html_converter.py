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

from para_conc.core.search.search import SearchResult
from para_conc.core.search.search_result_converter import SearchResultConverter


class HtmlConverter(SearchResultConverter):
    def __init__(self):
        super().__init__()

    def convert(self, search_result: SearchResult, show_context_original: bool, show_context_translation: bool,
                show_source_author: bool, show_source_translator: bool, show_source_title: bool):
        html = []
        html.append('<html>')
        html.append('<head>')
        html.append('<style>table{border-collapse:collapse}td{border:1px solid gray}</style>')
        html.append('</head>')
        html.append('<body>')
        html.append('<table style="border:1px solid blue">')
        for i_item in range(len(search_result.items)):
            item = search_result.items[i_item]
            row_span = 1 + show_context_original + len(item.translations) * (1 + int(show_context_translation))
            html.append(f'<tr><td rowspan={row_span}>{i_item + 1}</td>')
            html.append('<td>S</td><td>')
            for i_match, match in enumerate(item.original.matches):
                if match is not None:
                    line = item.original.lines[i_match]
                    html.append(line[:match.start])
                    html.append('<font color="red">')
                    html.append(line[match.start:match.end])
                    html.append('</font>')
                    html.append(line[match.end:])
                    html.append('<i>(')
                    html.append(SearchResultConverter.source_note(item.original, show_source_title, show_source_author))
                    html.append(')</i>')
            html.append('</td></tr>')
            if show_context_original:
                html.append('<td>C</td><td>')
                for i_match, match in enumerate(item.original.matches):
                    if match is not None:
                        html.append('<font color="blue">')
                        html.append(item.original.lines[i_match])
                        html.append('</font>')
                    else:
                        html.append(' ')
                        html.append(item.original.lines[i_match])
                html.append('<i>(')
                html.append(SearchResultConverter.source_note(item.original, show_source_title, show_source_author))
                html.append(')</i>')
                html.append('</td></tr>')
            for tr in item.translations:
                html.append('<tr><td>')
                html.append(tr.key.upper())
                html.append('</td><td>')
                for i_match, match in enumerate(tr.matches):
                    if match is not None:
                        html.append(tr.lines[i_match][:match.start])
                        html.append('<font color="red">')
                        html.append(tr.lines[i_match][match.start:match.end])
                        html.append('</font>')
                        html.append(tr.lines[i_match][match.end:])
                        html.append('<i>(')
                        html.append(SearchResultConverter.source_note_zh(tr, show_source_title, show_source_translator))
                        html.append(')</i>')
                html.append('</td></tr>')
                if show_context_translation:
                    html.append('<tr><td>')
                    html.append(tr.key.upper().replace('T', 'C'))
                    html.append('</td><td>')
                    for i_match, match in enumerate(tr.matches):
                        if match is not None:
                            html.append('<font color="blue">')
                            html.append(tr.lines[i_match])
                            html.append('</font>')
                        else:
                            html.append(' ')
                            html.append(tr.lines[i_match])
                    html.append('<i>(')
                    html.append(SearchResultConverter.source_note_zh(tr, show_source_title, show_source_translator))
                    html.append(')</i>')
                    html.append('</td></tr>')
        html.append('</table>')
        html.append('</body>')
        html.append('</html>')
        return ''.join(html)
