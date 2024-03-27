from pypinyin import pinyin, Style
from math import log
import os

text_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source/baike_qa_valid.json')
initing_title = []
initing_text = []
initing_texts = []
count = 0
count1 = 0


def check_contain_chinese(check_str):  # 检测字符是否是中文
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        else:
            return False


def bianli_text():  # 遍历语料库提取汉字
    for filename in os.listdir("source/AA"):
        with open("source/AA/" + filename, 'r', encoding='utf8') as fp:
            x = fp.readlines()
            global count
            global count1
            for x0 in x:
                x1 = eval(x0)
                initing_title.append(x1["title"])
                initing_text.append(x1["text"])
                count += len(x1["title"])
    for i in initing_text:
        temp = []
        for j in i:
            if check_contain_chinese(j):
                temp.append(j)
                count1 += 1
        initing_texts.append(temp)


def start_matrix(count0):  # 计算初始概率矩阵
    temp = {}
    for i in initing_title and initing_text:
        if i[0] not in temp.keys():
            temp.update({i[0]: 1})
        else:
            temp[i[0]] += 1
    for i in temp.keys():
        temp[i[0]] = log(temp[i[0]] / count0)
    return temp


def trans_matrix(count0, count2):  # 计算转移矩阵
    result = {}
    for i in initing_title and initing_texts:
        for j in range(len(i) - 1):
            if i[j] not in result.keys():
                result.update({i[j]: {}})
            if i[j + 1] not in result[i[j]].keys():
                result[i[j]].update({i[j + 1]: 1})
            else:
                result[i[j]][i[j + 1]] += 1
    for i in result:
        for j in result[i]:
            result[i][j] = log(result[i][j] / (count0+count2))
    return result


def emit_matrix():  # 计算发射矩阵
    result = {}
    count_list = {}
    for i in initing_title:
        pinyins = pinyin(i, style=Style.NORMAL, errors='ignore')
        temp = [x for x in i if check_contain_chinese(x)]
        for j in range(len(temp)):
            if temp[j] not in count_list:
                count_list.update({temp[j]: 1})
                result.update({temp[j]: {pinyins[j][0]: 1}})
            elif temp[j] in count_list:
                count_list[temp[j]] += 1
                if pinyins[j][0] not in result[temp[j]]:
                    result[temp[j]].update({pinyins[j][0]: 1})
                else:
                    result[temp[j]][pinyins[j][0]] += 1
    for i in initing_texts:
        for j in i:
            pinyin1 = pinyin(j, style=Style.NORMAL, heteronym=True)
            if j in result:
                pass
            else:
                temp = {}
                for x in pinyin1:
                    for y in x:
                        temp.update({y: 1})
                    count_list.update({j: len(x)})
                    result.update({j: temp})
    for i in result:
        for j in result[i]:
            result[i][j] = log(result[i][j]/count_list[i])
    return result


bianli_text()
starting = start_matrix(count)
transition = trans_matrix(count, count1)
with open("source/总词库.txt", 'r', encoding="utf-8") as ff:
    x = ff.readlines()
    emission = {}
    for x0 in x:
        emission.update(eval(x0))
