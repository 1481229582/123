import pandas as pd  
import jieba  
from collections import Counter  
from wordcloud import WordCloud  
import matplotlib.pyplot as plt  
from matplotlib import rcParams 
import streamlit as st
import os
import matplotlib as mpl  
  
# 加载停用词  
def load_stopwords(stopwords_file):  
    with open(stopwords_file, 'r', encoding='utf-8') as f:  
        stop_words = f.read().splitlines()  
    return set(stop_words)  
  
# 处理文本（分词、去停用词）  
def process_text(text, stop_words):  
    seg_list = jieba.cut(text, cut_all=False)  
    filtered_words = [word for word in seg_list if word not in stop_words and len(word) > 1]  
    return ' '.join(filtered_words)  
def autolabel(ax, rects, xpos='center'):  
    """  
    Attach a text label above each bar in *rects*, displaying its height.  
  
    *xpos* indicates which side to place the text w.r.t. the center of  
    the bar. It can be one of the following {'center', 'right', 'left'}.  
    """  
  
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}  
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off  
  
    for rect in rects:  
        height = rect.get_height()  
        ax.annotate('{}'.format(height),  
                    xy=(rect.get_x() + rect.get_width() * offset[xpos], height),  
                    xytext=(0, 3),  # 3 points vertical offset  
                    textcoords="offset points",  
                    ha=ha[xpos], va='bottom')  
        
# 确保matplotlib使用支持中文的字体  
mpl.font_manager.fontManager.addfont('simhei.ttf')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 替换为你的字体文件，如果SimHei不可用  
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号    

  
# 生成词云  
def generate_wordcloud(text, output_prefix):  
    word_counts = Counter(text.split())  
    wordcloud = WordCloud(font_path='simhei.ttf',  # 指定中文字体，确保词云可以显示中文  
                          width=800,  
                          height=400,  
                          background_color='white',  
                          stopwords=None,  
                          min_font_size=10).generate_from_frequencies(word_counts)  
  
    plt.figure(figsize=(8, 4), facecolor=None)  
    plt.imshow(wordcloud)  
    plt.axis("off")  
    plt.tight_layout(pad=0)  
  
    output_filename = f"{output_prefix}_wordcloud.png"  
    plt.savefig(output_filename, dpi=100)  
   
  
# 生成词汇频率的柱状图  
def generate_word_frequency_bar(word_counts, output_prefix):  
    # 获取频率最高的前N个词  
    N = 10  # 您可以根据需要修改这个数字  
    top_words, top_counts = zip(*word_counts.most_common(N))  
  
    # 绘制柱状图  
    plt.figure(figsize=(10, 6))  
    rects = plt.bar(range(N), top_counts, color='blue')  # 获取矩形对象  
    plt.title('词汇频率')  
    plt.xlabel('词汇')  
    plt.ylabel('频率')  
    plt.xticks(range(N), top_words, rotation=45)  # 设置x轴标签为词汇  
    plt.tight_layout()  
  
    # 添加标签到柱状图上  
    autolabel(plt.gca(), rects)  # 使用当前的axes和矩形对象  
  
    output_filename = f"{output_prefix}_word_frequency.png"  
    plt.savefig(output_filename, dpi=100)  
    # 在Streamlit中显示柱状图  
    st.pyplot(plt)  

  
# 处理CSV文件  
def process_file(filename, output_prefix):  
    df = pd.read_csv(filename, encoding='utf-8')  # 假设csv文件使用utf-8编码  
    comments = df['句子'].tolist()  # 假设'comment'是包含评论的列名  
  
    stop_words = load_stopwords('huizong_stopword.txt')  # 加载停用词  
  
    processed_comments = [process_text(comment, stop_words) for comment in comments]  
  
    # 合并处理后的评论为一个长文本  
    combined_text = ' '.join(processed_comments)  
  
    # 生成词云  
    wordcloud_filename = generate_wordcloud(combined_text, output_prefix)  
    # 确保文件存在，然后在Streamlit中显示它  
    if os.path.exists(wordcloud_filename):  
        st.image(wordcloud_filename)  
    else:  
        st.error("无法生成或找到词云图像")
  
    # 统计词汇频率  
    word_counts = Counter(combined_text.split())  
  
    # 生成词汇频率的柱状图  
    generate_word_frequency_bar(word_counts, output_prefix)  
  
# 对每个文件调用process_file函数  
filenames = ['正面评论.csv', '负面评论.csv', '中性评论.csv']  # 假设你有三个文件  
for filename in filenames:  
    process_file(filename, output_prefix=filename.split('_')[0])  # 根据文件名生成输出前缀