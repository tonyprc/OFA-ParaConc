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

import pandas as pd

from para_conc.core.search.search import SearchResult
from para_conc.core.search.search_result_converter import SearchResultConverter


class PandasHtmlConverter(SearchResultConverter):
    def __init__(self):
        super().__init__()

    def convert_to_list(self, search_result: SearchResult, show_context_original: bool, show_context_translation: bool,
                show_source_author: bool, show_source_translator: bool, show_source_title: bool):
        num_list = []
        lang_list = []
        con_list = []
        for i_item in range(len(search_result.items)):
            i_num = i_item + 1
            item = search_result.items[i_item]
            for i_match, match in enumerate(item.original.matches):
                if match is not None:
                    line = item.original.lines[i_match]
                    num_list.append(i_num)
                    lang_list.append('S')
                    con_list.append(f'{line[:match.start]}<font color="red"><b>{line[match.start:match.end]}</b></font>'
                                    f'{line[match.end:]}'
                                    f' <i><font color="grey" size=3>{self.source_note(item.original, show_source_title, show_source_author)}</font></i>')
            if show_context_original:
                context_line = ''
                for i_match, match in enumerate(item.original.matches):
                    if len(item.original.matches)==1:
                        context_line=''
                    else:
                        if match is not None:
                            context_line += '<font color="blue">' + item.original.lines[i_match] + '</font>'
                        else:
                            context_line += item.original.lines[i_match]

                if context_line:
                    context_line += ' <i><font color="grey" size=3>' + self.source_note(item.original, show_source_title, show_source_author) + '</font></i>'
                    num_list.append(i_num)
                    lang_list.append('C')
                    con_list.append(context_line)
                else: pass
            for tr in item.translations:
                for i_match, match in enumerate(tr.matches):
                    if match is not None:
                        num_list.append(i_num)
                        lang_list.append(tr.key.upper())
                        con_list.append(f'{tr.lines[i_match][:match.start]}<font color="red"><b>{tr.lines[i_match][match.start:match.end]}</b></font>'
                                        f'{tr.lines[i_match][match.end:]}'
                                        f' <font color="grey" size=3>{self.source_note(tr, show_source_title, show_source_translator)}</font>')
                if show_context_translation:
                    context_line = ''
                    for i_match, match in enumerate(item.original.matches):
                        if len(item.original.matches) == 1:
                            context_line = ''
                        else:
                            if match is not None:
                                context_line += '<font color="blue">' + tr.lines[i_match] + '</font>'
                            else:
                                context_line += tr.lines[i_match]
                    if context_line:
                        context_line += '<font color="grey" size=3>' + self.source_note(tr, show_source_title, show_source_translator) + '</font>'
                        num_list.append(i_num)
                        lang_list.append(tr.key.upper().replace('T', 'C'))
                        con_list.append(context_line)
                    else: pass
        return num_list,lang_list,con_list

    def convert_to_pd(self,num_list,lang_list,con_list):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', 10000)
        df = pd.DataFrame({'num': num_list,
                           'lang': lang_list,
                           'content': con_list})
        df.set_index(['num', 'lang'], inplace=True)
        tm_html = df.to_html(header=None, index=True, index_names=False, escape=False, col_space='5', border='2')
        tm_html = tm_html.replace('border="2"',
                                  'border="2", style="border-collapse:collapse; border-color:grey; background-color:WhiteSmoke"')
        tm_html = tm_html.replace('valign="top"',
                                  'valign="middle" align="center"')
        tm_html = tm_html.replace('<table',
                                  '<html>\n<body style="background-color:WhiteSmoke">\n<table ')
        tm_html = tm_html.replace('</table>',
                                  '</table>\n</body>\n</html>')
        tm_html = tm_html.replace('<th>',
                                  '<th valign="middle" align="center">')
        tm_html = tm_html.replace('<td>',
                                  '<td><font face="arial" size=4>')
        tm_html = tm_html.replace('</td>',
                                  '</font></td>')
        return tm_html
