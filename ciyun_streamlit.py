import pandas as pd  
import streamlit as st  
from collections import Counter  
from wordcloud import WordCloud  
import matplotlib.pyplot as plt  
import matplotlib as mpl  
from matplotlib.patches import Rectangle  
from jieba import cut  
import jieba
  
# 假设的文本处理函数  
# 处理文本（分词、去停用词）  
def process_text(text, stop_words):  
    seg_list = jieba.cut(text, cut_all=False)  
    filtered_words = [word for word in seg_list if word not in stop_words and len(word) > 1]  
    return ' '.join(filtered_words)  
  
# 加载停用词  
def load_stopwords(stopwords_file):  
    with open(stopwords_file, 'r', encoding='utf-8') as f:  
        stop_words = f.read().splitlines()  
    return set(stop_words)  

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
  
# 生成词汇频率的柱状图  
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
  
# 处理CSV文件  
def process_file(filename, output_prefix):  
    df = pd.read_csv(filename, encoding='utf-8')  # 假设csv文件使用utf-8编码  
    comments = df['句子'].tolist()  # 假设'句子'是包含评论的列名  
  
    stop_words = load_stopwords('huizong_stopword.txt')  # 加载停用词  
  
    processed_comments = [process_text(comment, stop_words) for comment in comments]  
  
    combined_text = ' '.join(processed_comments)  
  
    # 生成词云 (Streamlit 会显示)  
    with st.beta_container():  
        st.subheader(f"{output_prefix} 词云")  
        wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400, background_color='white', stopwords=None, min_font_size=10).generate(combined_text)  
        plt.figure(figsize=(8, 4), facecolor=None)  
        plt.imshow(wordcloud, interpolation='bilinear')  
        plt.axis("off")  
        plt.tight_layout(pad=0)  
        st.pyplot(plt)  
  
    # 统计词汇频率并生成柱状图 (Streamlit 会显示)  
    word_counts = Counter(combined_text.split())  
    with st.beta_container():  
        st.subheader(f"{output_prefix} 词汇频率")  
        generate_word_frequency_bar(word_counts, '')  # 不需要输出前缀，因为Streamlit直接显示  
  
# Streamlit 应用入口点  
def main():  
    filenames = ['正面评论.csv', '负面评论.csv', '中性评论.csv']  # 假设你有三个文件  
    for filename in filenames:  
        output_prefix = filename.split('_')[0]  
        process_file(filename, output_prefix)  
  
if __name__ == "__main__":  
    main()  
  
# 当您使用Streamlit运行此脚本时，它会自动调用 main 函数