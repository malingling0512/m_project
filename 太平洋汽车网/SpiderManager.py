#调度器
from 太平洋汽车网 import UrlManager
from 太平洋汽车网 import WebDownloader
from 太平洋汽车网 import WebParser
from 太平洋汽车网 import DataOutput

class SpiderManager():
    def __init__(self):
        self.urls=UrlManager.UrlManager()
        self.downoader=WebDownloader.WebDownloader()
        self.parse=WebParser.WebParser()
        self.output=DataOutput.DataOutput()
    def spider(self,begin):
        self.urls.add_url(begin)
        count = 0
        while self.urls.has_url():
            try:
                count += 1
                if count > 3:
                    break
                print('正在爬取第%s篇文章！'%count)
                pq_url=self.urls.get_url()
                print('第%s篇文章：'%count,pq_url)
                web_html=self.downoader.downloader_html(pq_url)
                # print(web_html)
                par_data, par_urls = self.parse.web_parse(web_html)
                print('标题',par_data['title'])
                img_urls=self.parse.get_imge_urls(web_html)
                #词频统计
                dfdata_cp=self.parse.word_numb(par_data['content'])
                # print(dfdata_cp)
                #得到新网址
                for i in par_urls:
                    # print(i)
                    self.urls.add_url(i)
                #数据输出
                self.output.write_csv(par_data)     #调用存储csv文件函数
                self.output.write_txt(par_data['content'])
                self.output.word_img(dfdata_cp, par_data)
                self.output.down_img(img_urls, par_data)
            except StopIteration as e:
                print(e)

if __name__ == '__main__':
    myspider=SpiderManager()
    pcauto='http://www.pcauto.com.cn/nation/1223/12230215.html'
    myspider.spider(pcauto)


