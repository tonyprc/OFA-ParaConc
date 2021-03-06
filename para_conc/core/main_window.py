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

import os,re,json

from para_conc.core.para_conc import ParaConc
from para_conc.core.search.pandas_html_converter import PandasHtmlConverter
from para_conc.core.search.search import SearchRequest, SearchMode, SearchResult
from para_conc.core.search.text_converter import TextConverter
from para_conc.ui.ui_main_window import UIMainWindow
from para_conc.ui.ui_sub_window import SubWindow
import time

class MainWindow:
    def __init__(self):
        
        currentDir = os.getcwd()
        dataDir = os.path.join(currentDir, "app_data")
        workFileDir = os.path.join(dataDir, "workfiles")
        self._outPutDir = os.path.join(currentDir, "savedfiles")
        self._starter_page_img = os.path.join(workFileDir, 'frontPage.png')
        self._interface_lang_file = os.path.join(workFileDir,'interface_language_setting.txt')
        self._interface_lang_dict = os.path.join(workFileDir,'interface_language_dict.json')
        self.fc_lg, self.fc_dict = self.set_lang()           

        # input filter
        self._stopchar_en_list = "\,\.\:\"\'\*\^\# \$\@\!~\(\)\_\-\+\=\{\}\[\]\?\/\<\>\&\%\;\\"
        self._stopchar_zh_list = "，。：、；“”’！…—（）《》｛｝【】？"
        self._regex_char_regex=r"\*|\^|\# |\$|\@|\!|\(|\)|\-|\+|\=|\{|\}|\[|\]|\?|\<|\>|\\|\|"

        # recieve signals
        self._ui = UIMainWindow()
        self._ui.save_text.connect(self.saveTxt)
        self._ui.save_html.connect(self.saveHtml)
        self._ui.search.connect(self.startConc)

        self._ui.print_result.connect(self.print_result)
        self._ui.load_corpus.connect(self.bi_dict_info)
        self._ui.view_chapter.connect(self.view_chapter)

        # data preparation
        self._paraConc = ParaConc()
        self.data_preload()
        self.resetWindow()
        self._current_corpus = None
        self._text_converter = TextConverter()
        self._html_converter = PandasHtmlConverter()

        self._search_result = None
        self._show_context_original = False
        self._show_context_translation = False
        self._show_source_author = True
        self._show_source_translator = True
        self._show_source_title = True
        
        # for result output
        self._page_i=0
        self._custom_set=100
        self._list_num=[]
        self._list_lang=[]
        self._list_cont=[]
        #self.set_lang()
        self._ui.show()

    def set_lang(self):
        with open (self._interface_lang_file, mode = 'r', encoding = 'utf-8-sig') as f:
            default_lg = f.read().strip()
        with open (self._interface_lang_dict, mode = 'r', encoding = 'utf-8-sig') as f:
            lg_dict = json.loads(f.read())
        return default_lg, lg_dict

    def resetWindow(self):
        self._ui.load_result_window(self._starter_page_img)

    def data_preload(self):
        self._ui.set_titles(self._paraConc.titles)
        self._ui.set_authors(self._paraConc.authors)
        self._ui.set_translators(self._paraConc.translators)
        self._ui.set_genres(self._paraConc.genres)

    def view_chapter(self, corpus_title, chapter_title):
        corpus = self._current_corpus
        text = '\n'.join(corpus.original_lines(chapter_title))
        sub_window = SubWindow(self._ui)
        title_part = chapter_title + ' from' if chapter_title != 'FULL TEXT' else ''
        sub_window.set_title(f'Full Text of {title_part} {corpus.original.title}')
        sub_window.set_text(text)
        sub_window.show()

    def bi_dict_info(self, corpus_title):
        corpus = self._paraConc.corpus(corpus_title)
        if corpus is None:
            return
        self._current_corpus = corpus
        self._ui.set_corpus(corpus)

    def inputCheck(self):
        # don't strip here for the sake of regex input
        srcWord = self._ui.search_text()
        search_mode = self._ui.search_mode()
        if srcWord == "":
            self._ui.set_status_text(self.fc_dict["src_wrd_warning_blank"][self.fc_lg])
            inputWord = ""
        elif SearchMode.REGEX == search_mode:
            inputWord = srcWord
        else:
            # to ensure no regex appeared in other mode
            m=re.search(self._regex_char_regex,srcWord)
            if m:
                self._ui.set_status_text(self.fc_dict["src_wrd_warning_regex"][self.fc_lg])
                inputWord=""
            else:
                # strip here to remove spaces
                srcWord=srcWord.strip()
                if srcWord[0] in self._stopchar_en_list:
                    self._ui.set_status_text(self.fc_dict["src_wrd_warning_punc"][self.fc_lg])
                    inputWord = ""
                elif srcWord[0] in self._stopchar_zh_list:
                    self._ui.set_status_text(self.fc_dict["src_wrd_warning_punc_zh"][self.fc_lg])
                    inputWord = ""
                else:
                    inputWord = srcWord
        return inputWord

    def _build_search_request(self):
        input_word = self.inputCheck()
        if input_word == '':
            return None

        req = SearchRequest()
        req.q = input_word
        req.mode = self._ui.search_mode()
        req.type, req.type_value = self._ui.search_type()
        if req.type is None:
            return None
        return req
    
    # core program
    def startConc(self):        
        self._page_i=0
        search_request = self._build_search_request()
        if search_request is None:
            return
        self._search_result = self._paraConc.search(search_request)
        # context display options
        self._show_context_original = False
        self._show_context_translation = False
        display_context = self._ui.display_context()
        if display_context == self.fc_dict["display_opt_context_sl"][self.fc_lg]:
            self._show_context_original = True
        if display_context == self.fc_dict["display_opt_context_tl"][self.fc_lg]:
            self._show_context_translation = True
        if display_context == self.fc_dict["display_opt_context_bi"][self.fc_lg]:
            self._show_context_original = True
            self._show_context_translation = True
        # hide source options
        self._show_source_author = True
        self._show_source_translator = True
        self._show_source_title = True
        display_source = self._ui.display_source()
        if display_source == self.fc_dict["hide_source_ar"][self.fc_lg]:
            self._show_source_author = False
        if display_source == self.fc_dict["hide_source_tr"][self.fc_lg]:
            self._show_source_translator = False
        if display_source == self.fc_dict["hide_source_ar_tr"][self.fc_lg]:
            self._show_source_author = False
            self._show_source_translator = False
        if display_source == self.fc_dict["hide_source_title"][self.fc_lg]:
            self._show_source_title = False
        # result display
        if len(self._search_result.items):
            self.resetWindow()
            # prepare three lists
            self._list_num, self._list_lang, self._list_cont = self._html_converter.convert_to_list(self._search_result,
                                                                                  self._show_context_original,
                                                                                  self._show_context_translation,
                                                                                  self._show_source_author,
                                                                                  self._show_source_translator,
                                                                                  self._show_source_title)

            # devide lists into pages
            startNum = self._page_i
            startSetNum = self._list_num[startNum]
            endSetNum = startSetNum + self._custom_set
            list_limit = max(self._list_num)
            if endSetNum <= list_limit:
                endNum = self._list_num.index(endSetNum)
                self._page_i = endNum
            else:
                endNum = -1
                self._page_i = 0
            # put lists into html produced by pandas
            if endNum == -1:
                html = self._html_converter.convert_to_pd(self._list_num[startNum:], self._list_lang[startNum:],
                                                          self._list_cont[startNum:])
            else:
                html = self._html_converter.convert_to_pd(self._list_num[startNum:endNum], self._list_lang[startNum:endNum],
                                                          self._list_cont[startNum:endNum])
            # html output
            self._ui.set_result_html(''.join(html))
            # activate the next page button
            if self._page_i != 0:
                self._ui._next_page_button.setDisabled(False)
            else:
                self._ui._next_page_button.setDisabled(True)
            # current concordance report
            total_sents = str(len(self._list_num))
            total_set = str(self._list_num[-1])
            if self.fc_lg == 'en':
                self._ui.set_status_text(f"{total_set} pairs of bi-text and {total_sents} sents of results are found")
            else:
                self._ui.set_status_text(f"本次检索共得到{total_set} 组 {total_sents}条结果")
        else:
            self.resetWindow()
            self._ui.set_status_text(self.fc_dict["src_record_null"][self.fc_lg])

    # next page function
    def print_result(self):
        if self._page_i !=0:
            self.resetWindow()
            startNum = self._page_i  # 指定本次打印起始行号
            startSetNum = self._list_num[startNum]
            endSetNum = startSetNum + self._custom_set
            list_limit = max(self._list_num)
            if endSetNum <= list_limit:
                endNum = self._list_num.index(endSetNum)
                self._page_i = endNum
            else:
                endNum = -1
                self._page_i = 0
            if endNum == -1:
                start_time=time.time()
                html = self._html_converter.convert_to_pd(self._list_num[startNum:], self._list_lang[startNum:],
                                                          self._list_cont[startNum:])
            else:
                start_time=time.time()
                html = self._html_converter.convert_to_pd(self._list_num[startNum:endNum], self._list_lang[startNum:endNum],
                                                          self._list_cont[startNum:endNum])
            self._ui.set_result_html(''.join(html))
            total_sents = str(len(self._list_num))
            total_set = str(self._list_num[-1])
            if self._page_i != 0:
                self._ui._next_page_button.setDisabled(False)
            else:
                self._ui._next_page_button.setDisabled(True)
            if self.fc_lg == 'en':
                self._ui.set_status_text(f"{total_set} pairs of bi-text and {total_sents} sents of results are found")
            else:
                self._ui.set_status_text(f"本次检索共得到{total_set} 组 {total_sents}条结果")
        else:
            self.resetWindow()
            self._ui.set_result_html('')
            self._ui.set_status_text(self.fc_dict["src_record_null"][self.fc_lg])

    # output to txt
    def saveTxt(self):
        if self._search_result is not None and len(self._search_result.items):
            srcInput = self._ui.search_text().strip()
            file_id = os.path.join(self._outPutDir, srcInput + '_output.txt')
            lines = self._text_converter.convert(self._list_num, self._list_lang, self._list_cont)
            with open(file_id, 'w', encoding='utf-8') as f:
                f.write(lines)
            self._ui.set_status_text(self.fc_dict["output_report_ok_txt"][self.fc_lg])
        else:
            self._ui.set_status_text(self.fc_dict["output_report_fail"][self.fc_lg])

    # output to html
    def saveHtml(self):
        if self._search_result is not None and len(self._search_result.items):
            srcInput = self._ui.search_text().strip()
            file_id = os.path.join(self._outPutDir, srcInput + '_output.html')
            tm_html = self._html_converter.convert_to_pd(self._list_num, self._list_lang, self._list_cont)
            # encoding is indispensible here.
            with open(file_id, 'w', encoding='utf-8') as f:
                f.write(tm_html)
            self._ui.set_status_text(self.fc_dict["output_report_ok_html"][self.fc_lg])
        else:
            self._ui.set_status_text(self.fc_dict["output_report_fail"][self.fc_lg])
