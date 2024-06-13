#实现项目的步骤
#             哔站在线课程资源的评价
#  1.爬取视频的弹幕（发送请求、获取数据、解析数据、保存数据）
#  2.弹幕数据清洗（去HTML标签、去标点符号、去停用词）
#  3.数据可视化（数据分析、数据可视化）

# 导入请求模块
import requests
# 导入正则模块
import re
import jieba#导入分词模块
# 请求网址
url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=351767814'
# 请求头
headers = {
    # user-agent 用户代理 表示浏览器基本身份标识
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0'
}
# 发送请求
response = requests.get(url=url,headers=headers)
# 解决网页数据乱码
response.encoding = 'utf-8'
# 获取数据
# print(response.text)
# 解析数据
content_list = re.findall('<d p=".*?">(.*?)</d>',response.text)
print(content_list)

# for 循环遍历输出内容
for content in content_list:
    with open('弹幕.txt',mode='a',encoding='utf-8')as f:
        f.write(content)
        f.write('\n')
    print(content)