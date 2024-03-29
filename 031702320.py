import re
# cooding=utf-8


import cpca
import json


import pandas as pd
import numpy as np

def getname(str):
    name = re.search('[^,]+', str[2:])
    return name.group()

def getphone(str):
    phone = re.search('\d{11}', str)
    return phone.group()

def getaddr(str):

    Match1 = re.search('[^,]+$', str)
    str_step1 = Match1.group()
    str_step2 = re.sub('\d{11}|', '', str_step1)
    Match2 = re.sub('\.', '', str_step2)
    if Match2[0:2]=='吉林':
        Match2=Match2[2:]
        if Match2[0]=='省':
            Match2=Match2[1:]
    str_step3 = cpca.transform([Match2], cut=False, open_warning=False)  # 调用cpca模块分出地址簿前三级
    list1 = str_step3.values.tolist()
    if (list1[0][0][0:2] == Match2[0:2]):
        list2 = list1[0]

    else:
        str_step3 = cpca.transform([Match2], open_warning=False)  # 调用cpca模块分出地址簿前三级
        list1 = str_step3.values.tolist()
        list2 = list1[0]

    str_step4 = list2[-1]
    str_step5 = re.search(re.compile(r'街道+|镇+|乡+|苏木+|开发区|合作区|管委会|园区'), str_step4)  # 分离出第四级
    if str_step5 == None:
        list4 = ['']
        list5 = [str_step4]
    else:
        x = str_step5.span()
        list4 = [str_step4[0:x[1]]]  # 把关键词之前的地址分成第四级给list4
        list5 = [str_step4[x[1]:]]
        if list4[0][-1]!='镇':
            if list5[0][0]=='道':
                list5=[str_step4]
                list4=['']
    #if list2[0][0:2] not in str_step2:
        #list2[0]=''
    if list2[1][0:2] not in str_step2:
        list2[1]=''
    if list2[2][0:3] not in str_step2:
        list2[2] = ''
    if str[0] != '1':  # 是否需要继续往下分级
        str_step6 = list5[-1]
        Match4 = re.search('[路巷街村]+', str_step6)

        if Match4 == None:
            list6 = ['']
            list7 = list5
        else:
            x = Match4.span()
            list6 = [str_step6[0:x[1]]]
            list7 = [str_step6[x[1]:]]

        str_step7 = list7[0]  # 分出第七级
        Match5 = re.search('[号弄]', str_step7)

        if Match5 == None:
            list8 = ['']
            list9 = list7
        else:
            x = Match5.span()
            list8 = [str_step7[0:x[1]]]
            list9 = [str_step7[x[1]:]]
        list5 = list6 + list8 + list9

    del list2[-1]
    list2 = list2 + list4
    list2 = list2 + list5
    
    if list2[0][0:2] == '上海':
        list2[0] = list2[0][0:2]
        list2[1]='上海市'
    if list2[0][0:2] == '天津':
        list2[0] = list2[0][0:2]
        list2[1] = '天津市'
    if list2[0][0:2] == '重庆':
        list2[0] = list2[0][0:2]
        list2[1] = '重庆市'
    if list2[0][0:2] == '北京' :
        list2[0] = list2[0][0:2]
        list2[1] = '北京市'
    return list2

while(1):
    
    str=input()
    if(str=="END"):
            break
    
    
    name=getname(str)
    phone=getphone(str)
    addr=getaddr(str)
    dict = {"姓名": name, "手机": phone, "地址": addr}
    json_dict = json.dumps(dict, ensure_ascii=False)
    print(json_dict)
