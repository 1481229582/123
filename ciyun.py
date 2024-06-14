# 导入词云模块
import wordcloud
# 导入jieba分词模块
import jieba
from collections import Counter
import string
import requests
import streamlit as st
from streamlit_echarts import st_echarts
from streamlit.logger import get_logger



# 读取文件内容
stop = []
standard_stop = []
text = []
after_text = []

file_stop = r'baidu_stopwords.txt'
file_text = r'弹幕.txt'  # 要处理的文本
with open(file_stop,'r',encoding='utf-8-sig') as f:
    lines = f.readlines()
    for line in lines:
        lline = line.strip()#strip()把头尾的空格和换行符给删除掉
        stop.append(lline)
    #导入停用词列表
for i in range(0,len(stop)):
    for word in stop[i].split():
        standard_stop.append(word)
print(standard_stop)

f = open('弹幕.txt',encoding='utf-8')
txt = f.read()
# print(txt)
print(jieba.lcut(txt))# 利用jieba模块进行分词，此处输出是一个列表
string0 = jieba.lcut(txt)
print(type(string0))#string是一个列表类型
# string1 = ' '.join(jieba.lcut(txt))# 利用join方法合并成字符串

print("--------------------------------------------------------------------")
for line  in string0:
    # lline = line.strip()
    # print(lline)
    lline = line.split()
    # print(lline)
    for i in lline:
         if i not in  standard_stop:
            after_text.append(i)
print(after_text)
string2 = ' '.join(after_text)#把列表转换成字符串
print(type(string2))

def bizhan_punctuation(text):#除去标点符号
    punctuation = string.punctuation
    for char in text:
        if char in punctuation:
            text = text.replace(char, ' ')
    return text
string3 = bizhan_punctuation(string2)
print(string3)


print("----------------------词频统计----------------------------")
def count_word_frequency(word_list):
    # 使用Counter对词频进行统计
    word_freq = Counter(word_list)

    # 对词频进行降序排列
    sorted_word_freq = sorted(
        word_freq.items(), key=lambda x: x[1], reverse=True)

    return sorted_word_freq

# 统计词频
word_freq = count_word_frequency(string3)
print("词频统计结果:", word_freq)

print("----------------------词频统计----------------------------")

for content in after_text:
    with open('弹幕已清洗.txt',mode='a',encoding='utf-8')as f:
        f.write(content)
        f.write('\n')
    print(content)
print("__________________________________________________________________")
string2 = ' '.join(after_text)

wc = wordcloud.WordCloud(#此处是WordCloud，要是wordcloud（小写）不会自动弹出参数名
    width=700, #宽
    height=700, #高
    background_color='white',#背景颜色
    font_path='msyh.ttc',#设置文字
    scale=20,#规模
    
)
wc.generate(string2)
wc.to_file('弹幕词云.png') 

wordcloud_options = {
    "tooltip": {
        "trigger": 'item',
        "formatter": '{b} : {c}'
    },
    "xAxis": [{
        "type": "category", 
        "data": [word for word, count in string2],
        "axisLabel": {
        "interval": 0, 
        "rotate": 30
        }
    }],
    "yAxis": [{"type": "value"}],
    "series": [{
        "type": "bar",
        "data": [count for word, count in string2]
    }]
        }