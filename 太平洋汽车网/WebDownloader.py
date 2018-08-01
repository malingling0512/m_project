#网页下载器
import urllib.request
class WebDownloader():
    #下载网页源代码
    def downloader_html(self,url):
        res=urllib.request.urlopen(url)
        # if res.getcode == 200:
        return res.read()    #.decode('utf-8')
        # else:return None

    #下载图片网页源代码
    def downloader_imag_html(self,url):
        res=urllib.request.urlopen(url)
        # if res.getcode == 200:
        return res.read()    #.decode('utf-8')
        # else:return None

