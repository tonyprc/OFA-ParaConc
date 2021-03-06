# OFA-ParaConc

# 傲飞一对多平行检索工具
## English-Chinese One to Many Concordancer
![software_interface](https://github.com/tonyprc/OFA-ParaConc/blob/main/img_storage/software_cover.jpg)

### 软件概况
### GENERAL INFO

傲飞一对多平行检索工具（OFA ParaConc）是一款依托语料库检索便利翻译人进行英汉翻译多版本学习或研究的辅助类开源软件。
本软件编写语言为python 3.8，UTF8编码，采用PyInstaller进行打包。本版本目前可在windows 7+窗口环境下运行(64位)。打包文件内含app_data及savedfiles两个工作目录，请勿擅自增删相关文件，以免影响软件的正常运行。
本软件内嵌英汉文学翻译一对多样本语料库，相关语料内容均取自网络，仅用于说明数据格式及展示检索功能目的。

---

### 基本功能
### FUNCTIONS

1. 界面语言选择
2. 语料加载
3. 语料展示
4. 操作提示
5. 英汉双向检索
6. 指定范围检索
7. 检索结果展示
8. 检索结果输出

#### 界面语言选择
#### CHOOSE INTERFACE LANGUAGE

界面语言选择功能方便用户根据自己的偏好选择合适的界面语言，当前仅支持中英文两种界面语言。

使用方法：界面默认语言为英文，若想更换成中文，请在启动软件前，打开app_data\workfiles\的界面语言配置文件interface_language_setting.txt，并将其内的“en”修改为“zh”，然后关闭该文件，启动软件即可。

#### 语料加载
#### LOAD THE CORPUS

语料加载功能方便用户根据具体需求自定义一对多语料进行检索。
本软件所用的语料基本格式为json，以utf8进行编码，命名方式为*.json。
适用于本软件的json文件基本结构由五级键值构成：

一级键为两个或多个对齐文档的统一源语名称（去空格），如名称中包含副标题，则应予以去除。示例：“TheOldManandtheSea”
二级键为源语与目标语语种。示例：“zh”,“en”
三级键为源语或目标语文档以数字编号为格式的版本号，源语以“s”为前缀，目标语以“t”为前缀，源语默认只有一个版本，数值设为0；目标语版本编号起始值为1，例如“s0”,“t1”,“t2”…… 
四级键为各版本的元信息，具体包括 “title”、“author”、“translator”、“language”、“date”、“genre”及“content”等七项，相应键值（除语言外）以相应版本的语言进行书写。
五级键为各版本正文句段的统一行号。相应键值为该句段的文本内容及篇章标题（以tab标记分隔）。

使用方法：在启动软件前，将符合上述规范的json文件放入本软件的app_data之下的corpus目录即可。

#### 语料展示
#### DISPLAY THE CORPUS

语料展示功能方便用户实时查看加载语料的基本信息及章节内容。软件启动时加载所有数据文件，并将自动提取到的数据文件字典名称展示在语料列表窗口中，将自动生成的作者，译者及类型等列表展示在语料检索各选项的下拉菜单之中。

使用方法：双击左侧语料列表中的某个文件名称，相应语料基本信息将展示在语料概况窗口中，具体信息包括：标题、作者、年代、类型、译本列表、正文内容等六项。在当前语料检索状态下，上述具体信息均为默认检索选项。
双击正文内容窗口中出现的列表项可查看该语料源语全文或章节具体内容。

#### 操作提示
#### OPERATION PROMPTS

操作提示功能方便用户了解界面各组件基本功能及把握检索进程的具体状况。提示信息以悬浮文字及状态栏文字等两种方式进行展示。

使用方法：将鼠标置于某组件之上并停留片刻，即可看到相应组件的基本功能提示信息；在进行具体检索操作时，在底部状态栏左侧位置可看到输入是否合法、检索结果具体组数与条数等各类提示信息。

#### 英汉双向检索
#### E-C/C-E CONCORDANCING

英汉双向检索功能方便用户依据实际需求在中英两种语言之间进行切换查询。本软件会依据用户输入的语言类型调用不同的检索程序进行英汉一对多正向或反向检索。具体的检索方式分普通检索、拓展检索与正则检索等三种：
普通检索：不进行关键词处理，按实际输入检索项进行检索；
拓展检索：对英文输入检索项先进行英文词形还原、大小写转换等预处理后再进行检索；
正则检索：按实际输入的正则表达式进行检索。本软件所处理的语料主体为未进行过分词的生语料，因此在进行中文检索时请勿使用\b或\s等需要寻找词汇边界的正则表达式。

使用方法：先点选左侧中部检索方式之下的普通检索、拓展检索或正则检索按钮，随后在其上的输入框里输入英文或中文检索词汇，然后点击“检索” 按钮 。当输入检索项不符合相应检索模式基本格式时，底部状态栏会出现相应的提示信息。

#### 指定范围检索
#### ASSIGNING THE SEARCH SCOPE

指定范围检索功能方便用户依据实际需求排除不相干的语料，锁定检索范围。

使用方法：点选左侧中下部检索范围内的全部语料、当前语料（全部译本、当前译本）、指定作者、指定译者、指定类型等选项按钮即可。当选择当前语料时可在语料概况窗口内进一步指定要检索的译文版本和/或当前语料的具体章节。单击（或Ctrl+单击）正文内容窗口中出现的一个（或多个）列表项，可指定检索范围为相应章节，

#### 检索结果展示
#### DISPLAY THE RESULTS

检索结果展示功能方便用户实时查看英汉一对多检索结果。
检索结果将以表格形式展示在右侧下方的检索结果窗口内，各检索辞条以原文上译文下的方式进行同组分行排列，
其前标有分组号、原译文版本标记，其内包含作者、译者、章节或书名等语料来源信息。检索结果的页面展示条数为一百组数据；当检索结果组数超过一百条时，检索结果窗口下方的分页展示按钮会亮起。
检索结果中的检索关键词以红色高亮形式突显，如同时展示段落，检索关键词所在句子将以蓝色高亮形式突显。检索结果有两种显示方式可供选择：展示语境选项决定是否在每条数据后展示当前检索辞条所在的原、译文或双语段落具体内容，如果当前检索辞条本身既为段落，或相应数据为不包含段落标志的句对齐语料，
相应段落则不予展示。默认为不展示语境；隐藏语源选项决定是否在每条数据后展示相应的作者、译者或章节等语料来源信息，默认为展示全部语源信息。

使用方法：在开始检索之前根据实际需求点选左侧下方的展示语境选项和或隐藏语源选项，然后点击检索按钮。底部状态栏左侧将实时显示本次检索结果的句组总数与句子总数。当检索结果窗口下方的分页展示按钮亮起时，可通过点击该按扭继续浏览余下检索结果。

#### 检索结果输出
#### OUTPUT THE RESULTS

检索结果输出功能方便用户根据实际需求提取出当前检索结果以供后续的NLP处理或研究使用。检索结果可输出为以tab符分隔的TXT文本文件或以表格方式呈现的HTML网页文件。

使用方法：点击上方菜单栏中的文件，点击下拉菜单中的输出语料，点击输出TXT文件或输出HTML文件。输出提示信息将出现在底部状态栏左侧。如果输出成功，可到savedfiles目录下查看以当前检索词命名并保存的检索结果文件。

### 搭建运行环境
### SET UP THE ENVIRONMENT

#### 第三方库列表
#### THIRD-PARTY PROGRAMS LIST
[requirements.txt](requirements.txt) 

#### 打包软件安装
#### INSTALL PACKING TOOL

`> pip install pyinstaller`

#### 程序打包
#### PACKAGING

`> pyinstaller -F -w main.py`

---
### 致谢
### ACKNOWLEDGEMENT

本软件的完成实在离不开以下人员的关心与帮助，在此一并表示由衷的感谢：
感谢河南城建学院李攀登先生对本人的激励、建议与一贯的支持；
感谢赵SIR对本软件进行的专业化结构调整与打磨；
感谢沈阳药科大学肇彤女士的前期研究成果及支持；
感谢微信公众号版主爱德宝器先生对本人的鼓舞与支持；
感谢“一心一译”翻译组各位师友给予的灵感、信任与关爱；
感谢本系主任张秀红教授对本软件开发的大力支持与长期关切；
同时也向AntConc，BFSU ParaConc及CUC的开发者们致以崇高的敬意。
最后再容我感谢一下我的家人的体谅、支持与期望。
---
### 软件图标
### MY ICON
![](./app_data/workfiles/myIcon.png)  
