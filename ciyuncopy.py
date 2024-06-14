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
import matplotlib.pyplot as plt
from wordcloud import WordCloud  
from matplotlib import rcParams 
import numpy as np  
from PIL import Image
# 读取文件内容
stop = []
standard_stop = []
text = []
after_text = []

file_stop = r'baidu_stopwords.txt'
# file_text = r'弹幕.txt'  # 要处理的文本
with open(file_stop,'r',encoding='utf-8-sig') as f:
    lines = f.readlines()
    for line in lines:
        lline = line.strip()#strip()把头尾的空格和换行符给删除掉
        stop.append(lline)
    #导入停用词列表
for i in range(0,len(stop)):
    for word in stop[i].split():
        standard_stop.append(word)

f = open('弹幕.txt',encoding='utf-8')
txt = f.read()
# print(txt)
# print(jieba.lcut(txt))# 利用jieba模块进行分词，此处输出是一个列表
string0 = jieba.lcut(txt)
# print(type(string0))#string是一个列表类型
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
# string2 = ' '.join(after_text)#把列表转换成字符串
# print(type(string2))

# 绘制柱状图  
word_counts = Counter(after_text)  # 假设after_text是一个字符串，我们使用split()来分割成单词  
top_words = word_counts.most_common(10)  
x, y = zip(*top_words)  
  
plt.figure(figsize=(10, 6))  
bars = plt.bar(x, y, color='blue')  
  
# 为每一根柱子添加标签  
def autolabel(bars):  
    for bar in bars:  
        height = bar.get_height()  
        plt.text(bar.get_x() + bar.get_width()/2., height,  
                 f'{height}',  # 直接显示整数词频，如果需要格式化可以添加'%'  
                 ha='center', va='bottom', fontsize=12)  
  
autolabel(bars)  
  
# 设置标题、坐标轴标签和x轴刻度倾斜  
plt.title('词频柱状图', fontsize=14)  
plt.xlabel('词汇', fontsize=12)  
plt.ylabel('词频', fontsize=12)  
plt.xticks(rotation=45)  
  
# 在Streamlit中显示柱状图  
st.pyplot(plt)  
  
# 生成词云  
wordcloud = WordCloud(font_path='simhei.ttf',  # 指定支持中文的字体路径  
                      background_color='white',  
                      width=800,  
                      height=600,  
                      margin=2,  
                      min_font_size=10).generate_from_frequencies(dict(word_counts))  
  
# 将词云转换为numpy数组，然后转换为PIL Image对象  
wordcloud_array = wordcloud.to_array()  
wordcloud_image = Image.fromarray(np.uint8(wordcloud_array))  
  
# 在Streamlit中显示词云  
st.image(wordcloud_image, caption='词云')  

