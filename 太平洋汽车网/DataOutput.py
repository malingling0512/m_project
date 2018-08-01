#数据输出器
import csv
import re
import os
import urllib.request
from wordcloud import WordCloud,ImageColorGenerator
from scipy.misc import imread
import matplotlib.pyplot as plt

class DataOutput():
    count=0
    def write_csv(self,parse_data):
        csv_name='太平洋汽车网.csv'
        with open('F:/project/太平洋汽车网/data/%s'%csv_name,'a',encoding='gb18030',newline='') as f:
            mycsv=csv.DictWriter(f,['标题','作者','类别','内容'])
            if self.count==0:
                mycsv.writeheader()
            mycsv.writerows([{'标题':parse_data['title'],'作者':parse_data['author'],'类别':parse_data['type'],'内容':parse_data['content']}])
            self.count += 1

    def write_txt(self,content):
            txt_name="太平洋汽车网____新车点评.txt"
            with open('F:/project/太平洋汽车网/data/%s'%txt_name,'a',encoding='gb18030',newline='') as f:
                f.write(content)

    def down_img(self, img_urls, par_data):
        count=0
        while img_urls:
            count += 1
            if count > len(img_urls):
                break
            name = par_data['title']
            new_name = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", name)
            tpyqc_image_path = 'F:\project\太平洋汽车网\data\image\%s\\' % new_name
            if not os.path.exists(tpyqc_image_path):   #os.path.exists判断变量、文件等是否存在
                os.mkdir(tpyqc_image_path)              #os.mkdir创建一级目录
            for i in img_urls:
                img_url = i
                img_name = tpyqc_image_path + par_data['title'] + str(count)+'.jpg'
                urllib.request.urlretrieve(img_url, img_name)   #从远程下载数据

    def word_img(self,dfdata_cp,par_data):
        # 词云【-
        word_img = imread('tu6.jpg')
        mywordcloud = WordCloud(font_path='simhei.ttf',
                                background_color='white',
                                max_words=100,  # 词云显示的最大词数
                                mask=word_img,  # 背景图片
                                max_font_size=500,  # 最大字体尺寸
                                random_state=42,  # 随机状态
                                width=1000,  # 图片的默认大小宽度
                                height=600,  # 图片的默认大小高度
                                margin=2  # 词语边缘间距
                                )
        word_frequence = {w[0]: w[1] for w in dfdata_cp.head(100).values}
        print(word_frequence)
        mywordcloud.generate_from_frequencies(word_frequence)
        img_color = ImageColorGenerator(word_img)
        mywordcloud.recolor(color_func=img_color)
        jpg_name=par_data['title']
        if '\\' in jpg_name:
            jpg_name=jpg_name.replace('\\','')
        mywordcloud.to_file('F:/project/太平洋汽车网/data/wordcloud_image/%s.jpg'%jpg_name)
        plt.imshow(mywordcloud)
        plt.axis("off")
        plt.show()