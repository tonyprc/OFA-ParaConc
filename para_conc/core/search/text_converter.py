# -*- coding: utf-8 -*-
import re
from para_conc.core.search.search import SearchResult
from para_conc.core.search.search_result_converter import SearchResultConverter


class TextConverter(SearchResultConverter):
    def __init__(self):
        super().__init__()
    def convert(self, list_num,list_lang,list_cont):
        result_list = [str(x) + '\t' + y + '\t' + z for (x, y, z) in zip(list_num,list_lang,list_cont)]
        result='\n'.join(result_list)
        result=re.sub(r'<.*?>','',result)
        return result
