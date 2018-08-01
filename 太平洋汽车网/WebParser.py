#网页解析器
from bs4 import BeautifulSoup
import re
import jieba
import pandas as pd
import numpy as np


class WebParser():
    def get_data(self,html_data):
        pq_data={}
        data_soup=BeautifulSoup(html_data,'lxml',from_encoding='utf-8')
        # print(data_soup)
        # 标题
        title=data_soup.find('h1',attrs={'class':'artTit'})
        # 作者
        author = re.findall('.*?作者：(.*?)</span>',str(data_soup),re.S)
        author = author[0]
        author = re.findall('[\u4E00-\u9FFF]+', author)
        author = author[0]
        # 类别
        type = data_soup.find_all('div', attrs={'class': 'pos-mark'})
        for i in type:
            type=i.text.replace('\n','')
        # 内容
        content_box=data_soup.find('div',attrs={'class':'artText clearfix'})
        content=content_box.text.replace('\u3000','')
        content = content.replace('\n', '')

        pq_data['title']=title.text
        pq_data['author'] = author
        pq_data['type']=type
        pq_data['content']=content
        return pq_data

    def get_url(self,html_data):
        data_soup = BeautifulSoup(html_data, 'lxml', from_encoding='utf-8')
        # print(data_soup)
        pq_url_box=data_soup.find('ul',attrs={'class':'ulArt clearfix'})
        pq_url=re.findall('<.*?href=".*?//(.*?)".*?>',str(pq_url_box),re.S)
        for i in pq_url:
            pq_url_1='http://'+i
            yield pq_url_1

    def web_parse(self,html_data):
        pq_data=self.get_data(html_data)
        pq_url=self.get_url(html_data)
        return pq_data,pq_url


    def get_imge_urls(self,web_html):
        imge_data_soup = BeautifulSoup(web_html, 'lxml', from_encoding='utf-8')
        # print(imge_data_soup)
        content_box = imge_data_soup.find('div', attrs={'class': 'artText clearfix'})  # 图片所在框架
        # print(content_box)
        imge_urls = re.findall('<.*?href=.*?viewpic_pcauto.htm\?(.*?)&amp.*?>', str(content_box), re.S)  # 图片链接
        return imge_urls


    #词云分析
    def word_numb(self,con_txt):
        fc_data=jieba.lcut(con_txt)
        print(fc_data)
        stopwords = pd.read_csv("stopwords.txt", index_col=False, names=['mystopword'], encoding='utf-8')
        df_data = pd.DataFrame({'tpy_fc':fc_data})
        new_dfdata = df_data[~df_data.tpy_fc.isin(stopwords.mystopword)]
        # print(new_dfdata)
        dfdata_cp = new_dfdata.groupby(by=['tpy_fc'])['tpy_fc'].agg({'计数': np.size})
        dfdata_cp=dfdata_cp.reset_index().sort_values(by=['计数'],ascending=False)
        # print(dfdata_cp)
        return dfdata_cp
