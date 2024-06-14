
import jieba
import requests
import streamlit as st
from streamlit_echarts import st_echarts
from collections import Counter
from streamlit.logger import get_logger
import re
import string
# import nltk
# from nltk.stem import PorterStemmer
# from nltk.corpus import stopwords


LOGGER = get_logger(__name__)

# 定义数据清洗函数
def clean_text(text):
    text = text.replace('\n', '')
    text = text.replace(' ', '')
    text = text.strip()
    return text

# 定义分词函数
def segment(text):
    stopwords = ['的', '了', '在', '是', '我', '你', '他', '她', '它', '们', '这', '那', '之', '与', '和', '或', '虽然', '但是', '然而', '因此']
    # 移除标点符号和换行符
    punctuation = "、，。！？；：“”‘’~@#￥%……&*（）【】｛｝+-*/=《》<>「」『』【】〔〕｟｠«»“”‘’'':;,/\\|[]{}()$^"
    text = text.translate(str.maketrans("", "", punctuation)).replace('\n', '')
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords]
    return words


# Removing punctuation, numbers
def remove_punctuation(text):
  punctuation = string.punctuation
  text = text.translate(str.maketrans('', '', punctuation))  
  return re.sub('\d+', '', text)



def stem_words(words):
  # Stemming words
  from nltk.stem import PorterStemmer
  stemmer = PorterStemmer()
  stemmed = []
  for word in words:
    stemmed.append(stemmer.stem(word))
  return stemmed

def remove_stopwords(words):
  # Filtering stopwords
  from nltk.corpus import stopwords
  stopwords = set(stopwords.words('english')) 
  return [word for word in words if word not in stopwords]
# removing html tags 

def remove_html_tags(text):
  clean = re.compile('<.*?>')
  return re.sub(clean, '', text)


def extract_body_text(html):
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('body').get_text()
    return text

def read_txtfile():
     # streamlit 读取txt文件示例
    st.write('streamlit 读取txt文件示例')
    from pathlib import Path
   
    
    filePath = Path(__file__).parent / "stop_words.txt"
    
    if filePath.is_file():
        with open(filePath, 'r') as f:
            data = f.read()
            st.write(data)
    else:
        st.write("File not found")

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    url = st.text_input('Enter URL:')

    if url:
        r = requests.get(url)
        r.encoding = 'utf-8'
        text = r.text
        text =extract_body_text(text)
        
        text = remove_html_tags(text)
        text = remove_punctuation(text)
        # words = tokenize(text) 
        # # words = stem_words(words)
        # words = remove_stopwords(text.split())

        # # 识别中英文，判断分词方式
        # import chardet
        # encoding = chardet.detect(text)['encoding']
        # if encoding == 'utf-8':
        #     words = jieba.cut(text)
        # else:
        #     words = text.split()

        # words = text.split()
        text = clean_text(text)
        words = segment(text)
        word_counts = Counter(words)
    
        top_words = word_counts.most_common(20)
    
        wordcloud_options = {
          "tooltip": {
            "trigger": 'item',
            "formatter": '{b} : {c}'
          },
          "xAxis": [{
            "type": "category", 
            "data": [word for word, count in top_words],
            "axisLabel": {
              "interval": 0, 
              "rotate": 30
            }
          }],
          "yAxis": [{"type": "value"}],
          "series": [{
            "type": "bar",
            "data": [count for word, count in top_words]
          }]
        }
    
        st_echarts(wordcloud_options, height='500px')
        
    # read_txtfile()




if __name__ == "__main__":
    run()