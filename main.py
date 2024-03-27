from pypinyin import pinyin, Style
from markov import starting, transition, emission


def viterbi(pinyin_list, star_list, tran_list, emis_list):
    result = []
    temp = []
    depth = len(pinyin_list)
    start = {}
    for i in star_list.keys():
        if i in emis_list.keys() and pinyin_list[0] in emis_list[i]:
            s = emis_list[i][pinyin_list[0]]+0.01
            start.update({i: abs(star_list[i]*s)})
            result.append(i)
            temp.append(i)

    for i in range(1, depth):
        temp0 = []
        temp_dict = {}
        for j in star_list.keys():
            if j in emis_list.keys() and pinyin_list[i] in emis_list[j]:
                compare_list = []
                for x in temp:
                    if j in tran_list[x[-1]]:
                        s1 = emis_list[j][pinyin_list[i]]+0.01
                        temp1 = [x+j, abs(start[x]*tran_list[x[-1]][j]*s1)]
                    else:
                        s2 = emis_list[j][pinyin_list[i]]+0.01
                        temp1 = [x+j, abs(star_list[j]*s2)]
                    compare_list.append(temp1)
                compare_list.sort(key=lambda x: x[1])
                if compare_list:
                    temp0.append(compare_list[0][0])
                    temp_dict.update({compare_list[0][0]: compare_list[0][1]})
        temp = temp0
        start = temp_dict

    return temp


while True:
    pinyin_str = input().split()
    print(viterbi(pinyin_str, starting, transition, emission))
