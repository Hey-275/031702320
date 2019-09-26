#coding=utf-8

import re
import cpca
piattern = re.compile(r'街道')
str=re.search(piattern,'鼓西街道湖滨路110号街湖滨大厦道一层')
print(piattern,str)