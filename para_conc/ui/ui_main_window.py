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

import os,json

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QAction, QComboBox,
                             QGroupBox, QPushButton, QLineEdit, QLabel, QRadioButton, QStatusBar,
                             QButtonGroup,QTextBrowser,
                             QCheckBox, QAbstractItemView, QWidget, QListWidget, QMessageBox, QSplitter)

from para_conc.core.search.search import SearchMode, SearchType

class UIMainWindow(QMainWindow):
    #set_lang = pyqtSignal()
    save_text = pyqtSignal()
    save_html = pyqtSignal()
    search = pyqtSignal()
    print_result = pyqtSignal()
    load_corpus = pyqtSignal(str)
    view_chapter = pyqtSignal(str, str)  # corpus title, chapter title    

    def __init__(self, parent=None):
        super(UIMainWindow, self).__init__(parent)
        currentDir = os.getcwd()
        dataDir = os.path.join(currentDir, "app_data")
        workFileDir = os.path.join(dataDir, "workfiles")
        self._interface_lang_file = os.path.join(workFileDir,'interface_language_setting.txt')
        self._interface_lang_dict = os.path.join(workFileDir,'interface_language_dict.json')
        self.fc_lg, self.fc_dict = self.set_lang()
    
        # region create window
        aboutAction = QAction(self.fc_dict['menu_about_item'][self.fc_lg], self)
        aboutAction.triggered.connect(self._info)        
        aboutAction.setStatusTip(self.fc_dict["menu_about_tip"][self.fc_lg])        
      
        outTxtAction = QAction(self.fc_dict["menu_output_txt"][self.fc_lg], self) 
        
        outTxtAction.triggered.connect(self.save_text)
        outTxtAction.setStatusTip(self.fc_dict["menu_output_txt_tip"][self.fc_lg])
        outHtmlAction = QAction(self.fc_dict["menu_output_html"][self.fc_lg], self)
        outHtmlAction.triggered.connect(self.save_html)
        outHtmlAction.setStatusTip(self.fc_dict["menu_output_html_tip"][self.fc_lg])

        menubar = self.menuBar()
        menubar.setContextMenuPolicy(Qt.PreventContextMenu)
        fileMenu = menubar.addMenu(self.fc_dict['menu_file'][self.fc_lg])
        fileMenu_saveGroup = fileMenu.addMenu(self.fc_dict["menu_output"][self.fc_lg])
        fileMenu_saveGroup.addAction(outTxtAction)
        fileMenu_saveGroup.addAction(outHtmlAction)
        infoMenu = menubar.addMenu(self.fc_dict['menu_about'][self.fc_lg])
        infoMenu.addAction(aboutAction)

        self._left_frame_layout = QVBoxLayout()

        self._left_frame_a = QGroupBox(self.fc_dict["corpora_list"][self.fc_lg])
        self._left_frame_a.setMaximumWidth(250)
        self._left_frame_a_layout = QVBoxLayout()

        self._json_list_window = QListWidget()
        # setStatusTip or setToolTip
        self._json_list_window.setToolTip(self.fc_dict["corpora_list_tip"][self.fc_lg])
        self._json_list_window.setMaximumWidth(240)
        self._json_list_window.setSortingEnabled(True)
        self._json_list_window.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._json_list_window.setContextMenuPolicy(Qt.CustomContextMenu)
        self._left_frame_a_layout.addWidget(self._json_list_window)
        self._left_frame_a.setLayout(self._left_frame_a_layout)

        self._left_frame_b = QGroupBox(self.fc_dict["conc_options"][self.fc_lg])
        self._left_frame_b.setMaximumWidth(250)
        self._left_frame_b_layout = QVBoxLayout()

        self._input_layout = QHBoxLayout()
        self._input_box = QLineEdit()
        self._input_box.setFixedWidth(150)
        self._input_button = QPushButton(self.fc_dict["src_button"][self.fc_lg])
        self._input_button.clicked.connect(self.search)
        self._input_button.setFixedWidth(80)
        self._input_layout.addWidget(self._input_box)
        self._input_layout.addWidget(self._input_button)

        self._src_mode = QButtonGroup()
        self._src_mode_list = QLabel(self.fc_dict["conc_mode"][self.fc_lg])
        self._src_mode_1 = QRadioButton(self.fc_dict["conc_mode_gm"][self.fc_lg])
        self._src_mode_1.setToolTip(self.fc_dict["conc_mode_gm_tip"][self.fc_lg])
        self._src_mode_2 = QRadioButton(self.fc_dict["conc_mode_em"][self.fc_lg])
        self._src_mode_2.setToolTip(self.fc_dict["conc_mode_em_tip"][self.fc_lg])
        self._src_mode_2.setChecked(True)
        self._src_mode_3 = QRadioButton(self.fc_dict["conc_mode_regex"][self.fc_lg])
        self._src_mode_3.setToolTip(self.fc_dict["conc_mode_regex_tip"][self.fc_lg])
        self._src_mode.addButton(self._src_mode_1)
        self._src_mode.addButton(self._src_mode_2)
        self._src_mode.addButton(self._src_mode_3)

        self._src_mode_layout = QGridLayout()
        self._src_mode_layout.addWidget(self._src_mode_list, 0, 0)
        self._src_mode_layout.addWidget(self._src_mode_1, 1, 0)
        self._src_mode_layout.addWidget(self._src_mode_2, 1, 1)
        self._src_mode_layout.addWidget(self._src_mode_3, 1, 2)

        self._src_category = QButtonGroup()

        self._src_scope_list = QLabel(self.fc_dict["conc_scope"][self.fc_lg])
        self._src_scope_1 = QRadioButton(self.fc_dict["conc_scope_all"][self.fc_lg])
        self._src_scope_1.setToolTip(self.fc_dict["conc_scope_all_tip"][self.fc_lg])
        self._src_scope_1.setChecked(True)
        self._src_scope_2 = QRadioButton(self.fc_dict["conc_scope_this"][self.fc_lg])
        self._src_scope_2.setToolTip(self.fc_dict["conc_scope_this_tip"][self.fc_lg])
        self._src_scope_3 = QComboBox()
        self._src_scope_3.setEnabled(False)
        self._src_scope_3.addItem(self.fc_dict["conc_scope_tls"][self.fc_lg])
        self._src_scope_3.addItem(self.fc_dict["conc_scope_this_tl"][self.fc_lg])
        self._src_scope_3.setCurrentIndex(0)

        self._src_author_btn = QRadioButton(self.fc_dict["conc_author"][self.fc_lg])
        self._src_author_opt = QComboBox()
        self._src_author_opt.setEnabled(False)

        self._src_translator_btn = QRadioButton(self.fc_dict["conc_translator"][self.fc_lg])
        self._src_translator_opt = QComboBox()
        self._src_translator_opt.setEnabled(False)

        self._src_genre_btn = QRadioButton(self.fc_dict["conc_genre"][self.fc_lg])
        self._src_genre_opt = QComboBox()
        self._src_genre_opt.setEnabled(False)

        self._src_category.addButton(self._src_scope_1)
        self._src_category.addButton(self._src_scope_2)
        self._src_category.addButton(self._src_author_btn)
        self._src_category.addButton(self._src_translator_btn)
        self._src_category.addButton(self._src_genre_btn)

        self._display_context_label = QLabel(self.fc_dict["display_opt"][self.fc_lg])
        self._display_context_button = QCheckBox(self.fc_dict["display_opt_context"][self.fc_lg])
        self._display_context_button.setToolTip(self.fc_dict["display_opt_context_tip"][self.fc_lg])
        self._display_context_button.setChecked(False)
        self._display_context_choice = QComboBox()
        self._display_context_choice.setEnabled(False)
        self._display_context_choice.addItem(self.fc_dict["display_opt_context_sl"][self.fc_lg])
        self._display_context_choice.addItem(self.fc_dict["display_opt_context_tl"][self.fc_lg])
        self._display_context_choice.addItem(self.fc_dict["display_opt_context_bi"][self.fc_lg])
        self._display_context_choice.setCurrentIndex(0)

        self._display_source_button = QCheckBox(self.fc_dict["hide_source"][self.fc_lg])
        self._display_source_button.setToolTip(self.fc_dict["hide_source_tip"][self.fc_lg])
        self._display_source_button.setChecked(False)
        self._display_source_choice = QComboBox()
        self._display_source_choice.setEnabled(False)
        self._display_source_choice.addItem(self.fc_dict["hide_source_ar"][self.fc_lg])
        self._display_source_choice.addItem(self.fc_dict["hide_source_tr"][self.fc_lg])
        self._display_source_choice.addItem(self.fc_dict["hide_source_ar_tr"][self.fc_lg])
        self._display_source_choice.addItem(self.fc_dict["hide_source_title"][self.fc_lg])
        self._display_source_choice.setCurrentIndex(0)

        self._src_scope_layout = QGridLayout()
        self._src_scope_layout.addWidget(self._src_scope_list, 0, 0)
        self._src_scope_layout.addWidget(self._src_scope_1, 1, 0)
        self._src_scope_layout.addWidget(self._src_scope_2, 1, 1)
        self._src_scope_layout.addWidget(self._src_scope_3, 1, 2)
        self._src_scope_layout.addWidget(self._src_author_btn, 2, 0)
        self._src_scope_layout.addWidget(self._src_author_opt, 2, 1, 1, 2)
        self._src_scope_layout.addWidget(self._src_translator_btn, 3, 0)
        self._src_scope_layout.addWidget(self._src_translator_opt, 3, 1, 1, 2)
        self._src_scope_layout.addWidget(self._src_genre_btn, 4, 0)
        self._src_scope_layout.addWidget(self._src_genre_opt, 4, 1, 1, 2)
        self._src_scope_layout.addWidget(self._display_context_label, 5, 0)
        self._src_scope_layout.addWidget(self._display_context_button, 5, 1)
        self._src_scope_layout.addWidget(self._display_context_choice, 5, 2)
        self._src_scope_layout.addWidget(self._display_source_button, 6, 1)
        self._src_scope_layout.addWidget(self._display_source_choice, 6, 2)

        self._left_frame_b_layout.addLayout(self._src_mode_layout)
        self._left_frame_b_layout.addLayout(self._src_scope_layout)
        self._left_frame_b.setLayout(self._left_frame_b_layout)

        self._left_frame_layout.addWidget(self._left_frame_a)
        self._left_frame_layout.addLayout(self._input_layout)
        self._left_frame_layout.addWidget(self._left_frame_b)

        self._json_info_form = QGroupBox(self.fc_dict["corpus_pro"][self.fc_lg])
        self._json_info_form.setAlignment(Qt.AlignRight)

        self._book_header_layout = QGridLayout()
        self._ss_book_title = QLabel(self.fc_dict["corpus_pro_title"][self.fc_lg])
        self._ss_book_titleBox = QLineEdit()
        self._ss_book_author = QLabel(self.fc_dict["corpus_pro_author"][self.fc_lg])
        self._ss_book_authorBox = QLineEdit()
        self._ss_book_date = QLabel(self.fc_dict["corpus_pro_date"][self.fc_lg])
        self._ss_book_dateBox = QLineEdit()
        #缩小宽度，以防止contentsBox出现左右拉横条
        self._ss_book_dateBox.setFixedWidth(115)
        self._ss_book_genre = QLabel(self.fc_dict["corpus_pro_genre"][self.fc_lg])
        self._ss_book_genreBox = QLineEdit()
        #缩小宽度，以防止contentsBox出现左右拉横条
        self._ss_book_genreBox.setFixedWidth(115)
        self._ss_book_contentsBox = QListWidget()
        self._ss_book_contentsBox.setToolTip(self.fc_dict["corpus_pro_content_tip"][self.fc_lg])
        #self.ss_book_contentsBox.setSortingEnabled(True)  # 排序会导致章节排序错误
        #限定高度
        self._ss_book_contentsBox.setFixedHeight(100)
        self._ss_book_contentsBox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._ss_book_contentsBox.setContextMenuPolicy(Qt.CustomContextMenu)

        self._tt_book_list = QLabel(self.fc_dict["corpus_pro_tlvn"][self.fc_lg])
        self._tt_book_listBox = QComboBox()
        self._tt_book_listBox.setToolTip(self.fc_dict["corpus_pro_tlvn_tip"][self.fc_lg])
        self._book_header_layout.addWidget(self._ss_book_title, 0, 0)
        self._book_header_layout.addWidget(self._ss_book_titleBox, 0, 1, 1, 3)
        self._book_header_layout.addWidget(self._ss_book_author, 1, 0)
        self._book_header_layout.addWidget(self._ss_book_authorBox, 1, 1, 1, 3)
        self._book_header_layout.addWidget(self._ss_book_date, 2, 0)
        self._book_header_layout.addWidget(self._ss_book_dateBox, 2, 1)
        self._book_header_layout.addWidget(self._ss_book_genre, 2, 2)
        self._book_header_layout.addWidget(self._ss_book_genreBox, 2, 3)
        self._book_header_layout.addWidget(self._tt_book_list, 3, 0)
        self._book_header_layout.addWidget(self._tt_book_listBox, 3, 1, 1, 3)
        self._book_header_layout.addWidget(self._ss_book_contentsBox, 0, 4, 4, 1)
        self._json_info_form.setLayout(self._book_header_layout)

        self._src_result_form = QGroupBox(self.fc_dict["conc_result"][self.fc_lg])
        self._src_result_form.setAlignment(Qt.AlignCenter)
        # 用QTextBrowser取代QWebEngineView以减小软件体积
        # self._result_window = QWebEngineView(parent)
        self._result_window = QTextBrowser(parent)
        self._result_window.setFrameStyle(0)
        # FrameStyle: NoFrame = 0 Box = 1  Panel = 2 WinPanel = 3 HLine = 4
        # VLine = 5 StyledPanel = 6 Plain = 16 Raised = 32 Sunken = 48

        self._src_result_formLayout = QHBoxLayout()
        self._src_result_formLayout.addWidget(self._result_window)
        self._src_result_form.setLayout(self._src_result_formLayout)

        self._next_page_button=QPushButton()
        self._next_page_button.setText(self.fc_dict["next_button"][self.fc_lg])
        self._next_page_button.clicked[bool].connect(self.print_result)
        self._next_page_button.setDisabled(True)
        self._next_page_button.setToolTip(self.fc_dict["next_button_tip"][self.fc_lg])

        info_splitter = QSplitter(Qt.Vertical)
        info_splitter.addWidget(self._json_info_form)
        info_splitter.addWidget(self._src_result_form)
        info_splitter.addWidget(self._next_page_button)
        info_splitter.setStretchFactor(1, 1)
        info_splitter.setCollapsible(0, False)
        info_splitter.setCollapsible(1, False)
        info_splitter.setCollapsible(0, False)

        mainWidget = QWidget()
        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setSpacing(2)
        mainLayout.addLayout(self._left_frame_layout)
        mainLayout.addWidget(info_splitter)
        self.setCentralWidget(mainWidget)

        # ----------创建主窗口状态栏----------
        self._statusBar = QStatusBar()
        self._statusBar.showMessage(self.fc_dict["info_welcome"][self.fc_lg])
        self._copyRightLabel = QLabel(self.fc_dict["info_copyright"][self.fc_lg])
        self._statusBar.addPermanentWidget(self._copyRightLabel)
        self.setStatusBar(self._statusBar)

        # ----------设置页面尺寸及标题等----------
        self.setGeometry(200, 50, 900, 610)
        self.setObjectName("MainWindow")
        self.setWindowTitle(self.fc_dict["info_title"][self.fc_lg])
        currentDir = os.getcwd()
        # self.setWindowIcon(QIcon("./app_data/workfiles/myIcon.png"))
        self.setWindowIcon(QIcon(currentDir + "/app_data/workfiles/myIcon.png"))
        self.setIconSize(QSize(100, 40))
        # endregion 创建窗口

        # region 关联事件
        self._src_scope_2.toggled.connect(self._src_scope_3.setEnabled)
        self._src_author_btn.toggled.connect(self._src_author_opt.setEnabled)
        self._src_translator_btn.toggled.connect(self._src_translator_opt.setEnabled)
        self._src_genre_btn.toggled.connect(self._src_genre_opt.setEnabled)
        self._display_context_button.toggled.connect(self._display_context_choice.setEnabled)
        self._display_source_button.toggled.connect(self._display_source_choice.setEnabled)

        self._tt_book_listBox.currentIndexChanged.connect(self._version_change_info)
        self._json_list_window.itemDoubleClicked.connect(self._json_list_window_item_double_clicked)
        self._ss_book_contentsBox.itemDoubleClicked.connect(self._ss_book_contentsBox_double_clicked)
        # endregion 关联事件

        self._corpus = None

        self._left_frame_a.setMaximumWidth(350)
        self._json_list_window.setMaximumWidth(340)
        self._left_frame_b.setMaximumWidth(350)
        
    def set_lang(self):
        with open (self._interface_lang_file, mode = 'r', encoding = 'utf-8-sig') as f:
            default_lg = f.read().strip()
        with open (self._interface_lang_dict, mode = 'r', encoding = 'utf-8-sig') as f:
            lg_dict = json.loads(f.read())
        return default_lg, lg_dict

    def load_result_window(self, img):        
        html='''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>index</title>\
                <style>body{text-align:center;background-color:WhiteSmoke}</style></head>\
                <body><img src="frontPage.png"/></body></html>'''
        html=html.replace('frontPage.png',img)
        self._result_window.setHtml(html)

    # 设置语料列表
    def set_titles(self, titles: []):
        self._json_list_window.clear()
        self._json_list_window.addItems(titles)
        self._corpus = None

    # 设置作者列表
    def set_authors(self, authors: []):
        self._src_author_opt.clear()
        self._src_author_opt.addItems(authors)

    # 设置译者列表
    def set_translators(self, translators: []):
        self._src_translator_opt.clear()
        self._src_translator_opt.addItems(translators)

    # 设置类型列表
    def set_genres(self, genres: []):
        self._src_genre_opt.clear()
        self._src_genre_opt.addItems(genres)

    # 设置状态栏文本
    def set_status_text(self, text):
        self._statusBar.showMessage(text, 10000)

    def set_corpus(self, corpus):
        self._corpus = corpus
        self._ss_book_titleBox.setText(corpus.original.title)
        self._ss_book_authorBox.setText(corpus.original.author)
        self._ss_book_dateBox.setText(corpus.original.date if corpus.original.date else 'unknown')
        self._ss_book_genreBox.setText(corpus.original.genre)
        self._src_genre_opt.setCurrentText(corpus.original.genre)
        self._ss_book_contentsBox.clear()
        for chapter in corpus.original.chapters:
            self._ss_book_contentsBox.addItem(chapter.title)
        self._tt_book_listBox.clear()
        for i, article in enumerate(corpus.translations):
            text = str(i + 1) + '：《' + article.title + '》' + article.translator + '译'
            if article.date:
                text += '（' + article.date + '年）'
            self._tt_book_listBox.addItem(text, userData=article)

    # 检索方式
    def search_mode(self) -> SearchMode:
        if self._src_mode_1.isChecked():
            return SearchMode.NORMAL
        if self._src_mode_3.isChecked():
            return SearchMode.REGEX
        return SearchMode.EXTENDED

    def search_text(self):
        return self._input_box.text()

    def search_type(self) -> ():
        # 全部语料
        if self._src_scope_1.isChecked():
           return SearchType.CORPUS_KEY, ''
        # 当前语料
        if self._src_scope_2.isChecked():
            if self._corpus is None:
                self.set_status_text(self.fc_dict["no_corpus_tip"][self.fc_lg])
                return None, ''
            if self.fc_dict["conc_scope_tls"][self.fc_lg] == self._src_scope_3.currentText():
                return SearchType.CORPUS_KEY, self._corpus.key
            else:
                chapter_titles = []
                if self._ss_book_contentsBox.count() > 1:
                    chapter_titles = list(a.text() for a in self._ss_book_contentsBox.selectedItems())
                return SearchType.ARTICLE_KEY, (self._corpus.key, self._tt_book_listBox.currentData().key, chapter_titles)
        # 指定作者
        if self._src_author_btn.isChecked():
            return SearchType.AUTHOR, self._src_author_opt.currentText()
        # 指定译者
        if self._src_translator_btn.isChecked():
            return SearchType.TRANSLATOR, self._src_translator_opt.currentText()
        # 指定类型
        if self._src_genre_btn.isChecked():
            return SearchType.GENRE, self._src_genre_opt.currentText()

        return None, ''

    def set_result_html(self, html):
        self._result_window.setHtml(html)

    def display_context(self):
        return self._display_context_choice.currentText() if self._display_context_button.isChecked() else ''

    def display_source(self):
        return self._display_source_choice.currentText() if self._display_source_button.isChecked() else ''

    def _info(self):
        QMessageBox.about(self, self.fc_dict["about_us_window_title"][self.fc_lg],
                          self.fc_dict["aboout_us_window_words"][self.fc_lg])

    def _json_list_window_item_double_clicked(self, item):
        self.load_corpus.emit(item.text())

    def _ss_book_contentsBox_double_clicked(self, item):
        self.view_chapter.emit(self._corpus.original.title, item.text())

    def _version_change_info(self, i):
        if self._tt_book_listBox.currentIndex() != -1:
            self._src_translator_opt.setCurrentText(self._tt_book_listBox.currentData().translator)
