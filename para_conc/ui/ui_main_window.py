# -*- coding: utf-8 -*-
# compiled by Tony96163

import os

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QAction, QComboBox,
                             QGroupBox, QPushButton, QLineEdit, QLabel, QRadioButton, QStatusBar,
                             QButtonGroup,QTextBrowser,
                             QCheckBox, QAbstractItemView, QWidget, QListWidget, QMessageBox, QSplitter)

from para_conc.core.search.search import SearchMode, SearchType


class UIMainWindow(QMainWindow):
    save_text = pyqtSignal()
    save_html = pyqtSignal()
    search = pyqtSignal()
    print_result = pyqtSignal()
    load_corpus = pyqtSignal(str)
    view_chapter = pyqtSignal(str, str)  # corpus title, chapter title

    def __init__(self, parent=None):
        super(UIMainWindow, self).__init__(parent)

        # region create window
        aboutAction = QAction('关于本软件', self)
        aboutAction.triggered.connect(self._info)        
        aboutAction.setStatusTip('查看软件制作信息')        
      
        outTxtAction = QAction('输出TXT文件', self) 
        
        outTxtAction.triggered.connect(self.save_text)
        outTxtAction.setStatusTip('将当前检索结果输出为txt文件')
        outHtmlAction = QAction('输出HTML文件', self)
        outHtmlAction.triggered.connect(self.save_html)
        outHtmlAction.setStatusTip('将当前检索结果输出为html文件')

        menubar = self.menuBar()
        menubar.setContextMenuPolicy(Qt.PreventContextMenu)
        fileMenu = menubar.addMenu('文件')
        fileMenu_saveGroup = fileMenu.addMenu('输出语料')
        fileMenu_saveGroup.addAction(outTxtAction)
        fileMenu_saveGroup.addAction(outHtmlAction)
        infoMenu = menubar.addMenu('关于')
        infoMenu.addAction(aboutAction)

        self._left_frame_layout = QVBoxLayout()

        self._left_frame_a = QGroupBox('语料列表')
        self._left_frame_a.setMaximumWidth(250)
        self._left_frame_a_layout = QVBoxLayout()

        self._json_list_window = QListWidget()
        # setStatusTip or setToolTip
        self._json_list_window.setToolTip('双击加载当前语料的语料概况')
        self._json_list_window.setMaximumWidth(240)
        self._json_list_window.setSortingEnabled(True)
        self._json_list_window.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._json_list_window.setContextMenuPolicy(Qt.CustomContextMenu)
        self._left_frame_a_layout.addWidget(self._json_list_window)
        self._left_frame_a.setLayout(self._left_frame_a_layout)

        self._left_frame_b = QGroupBox('检索选项')
        self._left_frame_b.setMaximumWidth(250)
        self._left_frame_b_layout = QVBoxLayout()

        self._input_layout = QHBoxLayout()
        self._input_box = QLineEdit()
        self._input_box.setFixedWidth(150)
        self._input_button = QPushButton('检索')
        self._input_button.clicked.connect(self.search)
        self._input_button.setFixedWidth(80)
        self._input_layout.addWidget(self._input_box)
        self._input_layout.addWidget(self._input_button)

        self._src_mode = QButtonGroup()
        self._src_mode_list = QLabel('检索方式：')
        self._src_mode_1 = QRadioButton('普通检索')
        self._src_mode_1.setToolTip('按输入检索词原样进行精确搜索')
        self._src_mode_2 = QRadioButton('拓展检索')
        self._src_mode_2.setToolTip('对输入词汇进行词形还原、忽略大小写等多重模糊搜索')
        self._src_mode_2.setChecked(True)
        self._src_mode_3 = QRadioButton('正则检索')
        self._src_mode_3.setToolTip('根据输入的正则表达式进行模糊搜索')
        self._src_mode.addButton(self._src_mode_1)
        self._src_mode.addButton(self._src_mode_2)
        self._src_mode.addButton(self._src_mode_3)

        self._src_mode_layout = QGridLayout()
        self._src_mode_layout.addWidget(self._src_mode_list, 0, 0)
        self._src_mode_layout.addWidget(self._src_mode_1, 1, 0)
        self._src_mode_layout.addWidget(self._src_mode_2, 1, 1)
        self._src_mode_layout.addWidget(self._src_mode_3, 1, 2)

        self._src_category = QButtonGroup()

        self._src_scope_list = QLabel('检索范围：')
        self._src_scope_1 = QRadioButton('全部语料')
        self._src_scope_1.setToolTip('对语料列表内所有语料进行检索')
        self._src_scope_1.setChecked(True)
        self._src_scope_2 = QRadioButton('当前语料')
        self._src_scope_2.setToolTip('仅检索语料概况中展示的篇章内容，可通过点选内容列表进一步缩小检索范围')
        self._src_scope_3 = QComboBox()
        self._src_scope_3.setEnabled(False)
        self._src_scope_3.addItem('全部译本')
        self._src_scope_3.addItem('当前译本')
        self._src_scope_3.setCurrentIndex(0)

        self._src_author_btn = QRadioButton('指定作者')
        self._src_author_opt = QComboBox()
        self._src_author_opt.setEnabled(False)

        self._src_translator_btn = QRadioButton('指定译者')
        self._src_translator_opt = QComboBox()
        self._src_translator_opt.setEnabled(False)

        self._src_genre_btn = QRadioButton('指定类型')
        self._src_genre_opt = QComboBox()
        self._src_genre_opt.setEnabled(False)

        self._src_category.addButton(self._src_scope_1)
        self._src_category.addButton(self._src_scope_2)
        self._src_category.addButton(self._src_author_btn)
        self._src_category.addButton(self._src_translator_btn)
        self._src_category.addButton(self._src_genre_btn)

        self._display_context_label = QLabel('显示方式：')
        self._display_context_button = QCheckBox('展示语境')
        self._display_context_button.setToolTip('同时展示检索句所在语段的具体内容')
        self._display_context_button.setChecked(False)
        self._display_context_choice = QComboBox()
        self._display_context_choice.setEnabled(False)
        self._display_context_choice.addItem('原文语境')
        self._display_context_choice.addItem('译文语境')
        self._display_context_choice.addItem('双语语境')
        self._display_context_choice.setCurrentIndex(0)

        self._display_source_button = QCheckBox('隐藏语源')
        self._display_source_button.setToolTip('不展示检索句作（译）者或其他语料来源信息')
        self._display_source_button.setChecked(False)
        self._display_source_choice = QComboBox()
        self._display_source_choice.setEnabled(False)
        self._display_source_choice.addItem('作者')
        self._display_source_choice.addItem('译者')
        self._display_source_choice.addItem('作(译)者')
        self._display_source_choice.addItem('作品名称')
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

        self._json_info_form = QGroupBox('语料概况')
        self._json_info_form.setAlignment(Qt.AlignRight)

        self._book_header_layout = QGridLayout()
        self._ss_book_title = QLabel('标题：')
        self._ss_book_titleBox = QLineEdit()
        self._ss_book_author = QLabel('作者：')
        self._ss_book_authorBox = QLineEdit()
        self._ss_book_date = QLabel('年代：')
        self._ss_book_dateBox = QLineEdit()
        #缩小宽度，以防止contentsBox出现左右拉横条
        self._ss_book_dateBox.setFixedWidth(115)
        self._ss_book_genre = QLabel('类型：')
        self._ss_book_genreBox = QLineEdit()
        #缩小宽度，以防止contentsBox出现左右拉横条
        self._ss_book_genreBox.setFixedWidth(115)
        self._ss_book_contentsBox = QListWidget()
        self._ss_book_contentsBox.setToolTip('双击查看内容，单击或Ctrl+单击可单选或复选检索范围，勿拖选')
        #self.ss_book_contentsBox.setSortingEnabled(True)  # 排序会导致章节排序错误
        #限定高度
        self._ss_book_contentsBox.setFixedHeight(100)
        self._ss_book_contentsBox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._ss_book_contentsBox.setContextMenuPolicy(Qt.CustomContextMenu)

        self._tt_book_list = QLabel('译本：')
        self._tt_book_listBox = QComboBox()
        self._tt_book_listBox.setToolTip('此处选定的译本将做为当前译本参与当前语料检索')
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

        self._src_result_form = QGroupBox('检索结果')
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
        self._next_page_button.setText('>>>>> 点击加载更多检索结果 <<<<<')
        self._next_page_button.clicked[bool].connect(self.print_result)
        self._next_page_button.setDisabled(True)
        self._next_page_button.setToolTip('分页展示每100组检索结果')

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
        self._statusBar.showMessage('欢迎使用 傲飞一对多平行检索工具 V.1.0.0')
        self._copyRightLabel = QLabel("Copyright © OFA ParaConc Since 2020")
        self._statusBar.addPermanentWidget(self._copyRightLabel)
        self.setStatusBar(self._statusBar)

        # ----------设置页面尺寸及标题等----------
        self.setGeometry(200, 50, 900, 610)
        self.setObjectName("MainWindow")
        self.setWindowTitle("OFA ParaConc")
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
                self.set_status_text("当前语料未加载，请先在语列料表中双击某具体语料，再进行当前语料检索。")
                return None, ''
            if '全部译本' == self._src_scope_3.currentText():
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
        QMessageBox.about(self, "About Us",
                          '''<p align='center'>傲飞一对多平行检索工具<br>
                             OFA ParaConc<br>
                            Windows 试用版 V.1.0.0<br>
                          英语快餐厅 版权所有<br>
                          软件制作：张修海 抚顺师范高等专科学校外语系<br>
                          电子邮件：42716403@qq.com</p>''')

    def _json_list_window_item_double_clicked(self, item):
        self.load_corpus.emit(item.text())

    def _ss_book_contentsBox_double_clicked(self, item):
        self.view_chapter.emit(self._corpus.original.title, item.text())

    def _version_change_info(self, i):
        if self._tt_book_listBox.currentIndex() != -1:
            self._src_translator_opt.setCurrentText(self._tt_book_listBox.currentData().translator)
