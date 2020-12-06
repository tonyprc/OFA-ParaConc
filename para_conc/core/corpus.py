# -*- coding: utf-8 -*-
# compiled by Tony96163

class Paragraph:
    def __init__(self, chapter, key):
        self.chapter = chapter
        self.key = key
        self.lines = []

class Chapter:
    def __init__(self, article):
        self.article = article
        self.title = ''
        self.paragraphs = []

    def lines(self) -> []:
        result = []
        for p in self.paragraphs:
            result += p.lines
        return result

class Article:
    def __init__(self, key, data: dict) -> None:
        self.key = key
        self.title = data.get('title', '').strip()
        self.author = data.get('author', '').strip()
        self.translator = data.get('translator', '').strip()
        self.date = data.get('date', '').strip()
        self.genre = data.get('genre', '').strip()
        self.chapters = []
        self._paragraph_map = {}
        chapter = None
        last_chapter_title = None
        for k, v in data.get('content', {}).items():
            temp = v.split('\t')
            text = temp[0].strip()
            chapter_title = temp[1].strip()
            if chapter_title != last_chapter_title:
                chapter = Chapter(self)
                chapter.title = chapter_title
                self.chapters.append(chapter)
                last_chapter_title = chapter_title
            paragraph = Paragraph(chapter, k)
            paragraph.lines = text.split('|')
            chapter.paragraphs.append(paragraph)
            self._paragraph_map[k] = paragraph
        if len(self.chapters) == 1:
            if self.chapters[0].title == self.title:
                self.chapters[0].title = 'FULL TEXT'
            else: pass

    def lines(self, chapter_title) -> []:
        chapter = None
        for c in self.chapters:
            if chapter_title == c.title:
                chapter = c
        if chapter is None:
            chapter = self.chapters[0]
        return chapter.lines() if chapter is not None else []

    def get_paragraph(self, paragraph_key):
        return self._paragraph_map.get(paragraph_key, None)


class Corpus:
    def __init__(self, data: dict) -> None:
        self.key = ''
        self.original: Article    # source language version
        self.translations = []    # target language version list
        self.translators = set()  # translators list from all tl versions
        for k, v in data.items():
            self.key = k
            for ek, ev in v['en'].items():
                self.original = Article(ek, ev)
                break  # sl version is supposed to be a single one
            for zk, zv in v['zh'].items():
                self.translations.append(Article(zk, zv))
        for translation in self.translations:
            self.translators.add(translation.translator)

    def original_lines(self, chapter_title) -> []:
        return self.original.lines(chapter_title)

