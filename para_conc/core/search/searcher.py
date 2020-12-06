# -*- coding: utf-8 -*-

import re
#from langid import langid

from para_conc.core.corpus import Corpus, Article, Chapter
from para_conc.core.search.search import SearchRequest, SearchResultItem, SearchMode, SearchType, \
    SearchResult, MatchResult, ArticleResult


class Searcher:
    def __init__(self):
        self.en_lemma_dict = {}

    def search(self, corpora: [], req: SearchRequest) -> SearchResult:
        q = req.q
        if self.detect_lang(q) == 'zh':
            return self._search_zh(corpora, req)
        return self._search_en(corpora, req)

    def _search_en(self, corpora: [], req: SearchRequest) -> SearchResult:
        # 搜索只返回数据结构，不包含展示样式
        # 这样才能使得展示方式的变动（html -> rtf）不会影响搜索代码
        # 要返回的检索结果，结构为self.items列表，列表内部为原文articleResult()与译文结果列表
        # ArticelResult为单个语料的键名，标题，作译者，句子列表，匹配结果列表
        result = SearchResult()
        # 依据检索模式处理检索词
        query = self._build_query(req.q, req.mode)
        for corpus in corpora:
            # 遍历语料库，如果语料不符合检索条件，返回值为假，则跳过
            # 判断 corpus 是否符合搜索范围，不符合直接判断下一个
            # 重点：不看 _match_corpus 的实现代码，把 corpus 判断抽取为独立方法就是为了在阅读整体逻辑时不用去考虑实现细节
            if not self._match_corpus(corpus, req):
                continue
            # 提取单一语料原文
            article = corpus.original            
            # 遍历原文各章节
            # 判断原文 chapter 是否符合搜索条件
            # 同样，在这时候不要去看 _match_chapter 的具体实现
            for chapter in article.chapters:
                # 章节不符合检索条件，跳过
                if not self._match_chapter(chapter, req):
                    continue
                # 遍历章节中的段落
                # 之前的每行文本，这里对应为 paragraph
                # 每行使用竖线(|)，标记文本对齐。这里已经提前将文本按照竖线做过拆分，拆分后的每一项放入 paragraph.lines
                for paragraph in chapter.paragraphs:
                    # 遍历段落中的句子
                    for i_line in range(len(paragraph.lines)):
                        # 按句子键取出句子
                        line = paragraph.lines[i_line]
                        # region 遍历搜索
                        # 这里的 # region 是 PyCharm 做文本折叠的标记。左边行号右边有个折叠标签，对应下面 # endregion
                        # 折叠的目的是为了看代码时能够把不关心的东西先隐藏起来
                        # 对句子进行检索
                        for match in re.finditer(query, line):
                            # 执行到这里说明：原文和译文同时满足搜索条件，并且原文的 line 匹配到搜索词
                            # 这时，创建一个搜索结果项目 SearchResultItem
                            result_item = SearchResultItem()
                            # 放入当前语料原文（包括键名，标题，作译者）
                            result_item.original.assign_from(article)
                            # 放入当前语料篇章标题
                            result_item.original.chapter_title = chapter.title
                            # 按段内句子数编号，将句子键值对放入相应段落句子列表
                            for i in range(len(paragraph.lines)):
                                # 遍历原文 paragraph 的每一行，放入结果的 original.lines。这个作为原文的语境
                                # 不管显示方式是否选择了“显示语境”，统一放进去，searcher 不关心这些。converter 根据显示方式来拼接 html
                                result_item.original.lines.append(paragraph.lines[i])
                                # 如果当前句号与本段第一句，放入对齐句坐标，否则略过
                                # 如果当前行是搜索词匹配的行，就放入一个 MatchResult，这个用来记录匹配词在 line 中的位置，start, end
                                if i == i_line:
                                    result_item.original.matches.append(MatchResult(match.start(), match.end()))
                                else:
                                    # 如果当前行不是搜索词匹配的行，就放入一个 None，这样保证 result_item.original.matches 的长度与 lines 相同
                                    # converter 在判断 line 是否有匹配词的时候只需要判断对应的 matches 是否为 None 就可以，不需要额外记录匹配词所在的 line
                                    result_item.original.matches.append(None)
                            # 对于当前句检索结果，遍历所有译本，不符合译本检索条件的略过
                            # 译文是否符合搜索条件
                            for translation in corpus.translations:
                                if not self._match_translation(translation, req):
                                    continue
                                try:
                                    # 利用原文段键尝试提取相应译文段
                                    # 译文对应的原文 paragraph
                                    trans_paragraph = translation.get_paragraph(paragraph.key)
                                    if trans_paragraph is not None:
                                        # 如果存在，建立译文单篇检索结果对象
                                        # 译文如果没有翻译原文对应的这一个 paragraph，则 trans_paragraph 为 None
                                        trans_result = ArticleResult()
                                        # 放入译本信息（包括键名，标题，作译者）
                                        trans_result.assign_from(translation)
                                        # 放入译本章节标题
                                        trans_result.chapter_title = trans_paragraph.chapter.title
                                        # 遍历译本段落内所有句子
                                        for i in range(len(trans_paragraph.lines)):
                                            # 为每句建立行号与句子键值
                                            # 译文语境，不管显示方式，统一放入
                                            trans_line = trans_paragraph.lines[i]
                                            # 将按行号提取出的句子放入各段的句子列表
                                            trans_result.lines.append(trans_line)
                                            # 如果行号与原文行号相同，放入句子匹配结果坐标(0,句长），否则略过
                                            # 如果译文当前 line 是原文匹配词出现的 line，则添加一个 MatchResult
                                            # 中文不能判断词出现的位置，MatchResult 简化为全行匹配
                                            if i == i_line:
                                                # trans_result.matches.append(MatchResult(0, len(trans_line)))
                                                # trans_result.matches.append(None)
                                                trans_result.matches.append(MatchResult(0, 0))
                                            else:
                                                trans_result.matches.append(None)
                                        # 如果存在翻译检索索句子列表，向单项检索结果列表中填加译本检索结果
                                        # 如果原文根据搜索条件没有相应的译文，就忽略这个搜索结果
                                        # 如果译文有匹配，就加到结果中
                                        if len(trans_result.lines):
                                            result_item.translations.append(trans_result)
                                except Exception as e:
                                    print(e)
                            # 如果译本检索结果项存在，将所有检索结果项填加给检索结果
                            if len(result_item.translations):  # 没有译文的跳过
                                result.items.append(result_item)
                        # endregion
        return result

    # 中文检索程序
    def _search_zh(self, corpora: [], req: SearchRequest) -> SearchResult:
        result = SearchResult()
        query = self._build_reverse_query(req.q, req.mode)
        for corpus in corpora:
            if not self._match_corpus(corpus, req):
                continue
            for translation in corpus.translations:
                if not self._match_translation(translation, req):
                    continue
                for chapter in translation.chapters:
                    if not self._match_chapter(chapter, req):
                        continue
                    for paragraph in chapter.paragraphs:
                        for i_line in range(len(paragraph.lines)):
                            line = paragraph.lines[i_line]
                            for match in re.finditer(query, line):
                                result_item = SearchResultItem()
                                trans_result = ArticleResult()
                                trans_result.assign_from(translation)
                                trans_result.chapter_title = chapter.title
                                for i in range(len(paragraph.lines)):
                                    trans_result.lines.append(paragraph.lines[i])
                                    if i == i_line:
                                        trans_result.matches.append(MatchResult(match.start(), match.end()))
                                    else:
                                        trans_result.matches.append(None)
                                if len(trans_result.lines):
                                    result_item.translations.append(trans_result)
                                    # result_item.original = trans_result
                                article=corpus.original
                                ori_paragraph = article.get_paragraph(paragraph.key)
                                if ori_paragraph is not None:
                                    ori_result = ArticleResult()
                                    ori_result.assign_from(article)
                                    ori_result.chapter_title = ori_paragraph.chapter.title
                                    for i in range(len(ori_paragraph.lines)):
                                        ori_line = ori_paragraph.lines[i]
                                        ori_result.lines.append(ori_line)
                                        if i == i_line:
                                            ori_result.matches.append(MatchResult(0, 0))
                                            # ori_result.matches.append(MatchResult(0, len(ori_line)))
                                        else:
                                            ori_result.matches.append(None)
                                    if len(ori_result.lines):
                                        result_item.original = ori_result
                                        # result_item.translations.append(ori_result)
                                if len(result_item.original.lines):
                                    result.items.append(result_item)
                                
        return result

    # 语言检测，检测输入是中文还是英文
    def detect_lang(self, text):
        target_lang = 'en'
        for word in text:
            if '\u4e00' <= word <= '\u9fa5' or '\u3400' <= word <= '\u4DB5':
                target_lang = 'zh'
                break
        return target_lang

    @staticmethod
    def _match_corpus(corpus: Corpus, req: SearchRequest) -> bool:
        # 检索范围如果是所有语料，当前语料值或为空或语料键名
        if req.type == SearchType.CORPUS_KEY:
            return req.type_value == '' or req.type_value == corpus.key
        # 检索范围如果是当前语料，当前语料键名，当前译本，篇章标题取值
        if req.type == SearchType.ARTICLE_KEY:
            corpus_key, article_key, chapter_titles = req.type_value
            if corpus_key != corpus.key:
                return False
            if article_key == '':
                return True
            # 存在篇章标题：
            if len(chapter_titles):
                for chapter in corpus.original.chapters:
                    if chapter.title in chapter_titles:
                        return True
            # 原文与译文键名相同：
            for translation in corpus.translations:
                if article_key == translation.key:
                    return True
        # 检索作者且作者值等于当前语料作者
        if req.type == SearchType.AUTHOR and req.type_value == corpus.original.author:
            return True
        # 检索译者：当前语料所有译本如果值为当前作者
        if req.type == SearchType.TRANSLATOR:
            for translation in corpus.translations:
                if req.type_value == translation.translator:
                    return True
        # 检索类型：语料类型且为当前语料类型
        if req.type == SearchType.GENRE and req.type_value == corpus.original.genre:
            return True
        return False

    @staticmethod
    def _match_chapter(chapter: Chapter, req: SearchRequest) -> bool:
        # 如果检索范围为当前语料，提取语料键，原译文键，篇章标题，返回0（全文）或各章标题
        if SearchType.ARTICLE_KEY == req.type:
            corpus_key, article_key, chapter_titles = req.type_value
            return len(chapter_titles) == 0 or chapter.title in chapter_titles
        return True

    @staticmethod
    def _match_translation(translation: Article, req: SearchRequest) -> bool:
        # 如果检索范围为当前语料，提取语料键，原译文键，篇章标题，文章空键或译本键）
        if SearchType.ARTICLE_KEY == req.type:
            corpus_key, article_key, chapter_titles = req.type_value
            return article_key == '' or article_key == translation.key
        # 如果检索类型为译者，返回空值或译者名）
        if SearchType.TRANSLATOR == req.type:
            return req.type_value == '' or req.type_value == translation.translator
        return True

    # 英文检索词封装
    def _build_query(self, q, mode: SearchMode):
        result = ''
        if mode == SearchMode.NORMAL:
            result = r'\b' + q + r'\b'
        if mode == SearchMode.REGEX:
            result = re.compile(r"{}".format(q))
        if mode == SearchMode.EXTENDED:
            src_word_list = []
            src_wrd_list = q.split()
            for word in src_wrd_list:
                if word.isalpha() and word != word.upper():
                    lower_word = word.lower()
                    capitalize_word = word.capitalize()
                    if word == lower_word or word == capitalize_word:  # 检索词全部小写或首字母大写，改为大小写均搜索
                        if lower_word in self.en_lemma_dict.keys():  # 用户输入检索词存在于词性还原字典键内的情况
                            t = [v + '|' + v.capitalize() for v in self.en_lemma_dict[lower_word]]
                            src_word_list.append(
                                r'\b(' + lower_word + r'|' + capitalize_word + '|' + '|'.join(t) + r')\b')
                        else:
                            t = []
                            for key, value in self.en_lemma_dict.items():  # 用户输入检索词存在于词性还原字典值内的情况
                                if lower_word in value:
                                    t.extend([v + '|' + v.capitalize() for v in value if v != lower_word])
                                    t.append(key + '|' + key.capitalize())
                                else:
                                    pass
                            if t:
                                src_word_list.append(
                                    r'\b(' + lower_word + '|' + capitalize_word + '|' + '|'.join(t) + r')\b')
                            else:
                                src_word_list.append(r'\b(' + lower_word + '|' + capitalize_word + r')\b')
                    else:
                        src_word_list.append(r'(\b' + word + r'\b)')
                else:
                    src_word_list.append(r'(\b' + word + r'\b)')
            if len(src_word_list) == 1:
                result = '\s'.join(src_word_list)
            elif len(src_word_list) > 1:
                result = r'(' + '\s'.join(src_word_list) + r')'
        return result

    # 中文检索词封装，与英文不同处是前两种模式下中文不能加边界或空格
    def _build_reverse_query(self, q, mode: SearchMode):
        result = ''
        if mode == SearchMode.REGEX:
            result = re.compile(r"{}".format(q))
        else:
            result = q
        return result
