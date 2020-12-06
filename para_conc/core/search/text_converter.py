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
