# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from zuofan_scrapy.items import ZuofanItem

class ZuofanSpider(scrapy.Spider):
    name = 'zuofan'
    allowed_domains = ['www.zuofan.cn']
    start_urls = ['http://www.zuofan.cn/cx/chuancai/']

    def parse(self, response):
        count=0
        while True:
            count+=1
            if count>5:
                break
            ahrefs = response.css(".wrap .w1180 .cp_list .center dt a")
            for a in ahrefs:
                imgurl = a.css("img::attr(src)").extract_first("")
                aaurl = a.css("::attr(href)").extract_first("")
                aurl = 'http://www.zuofan.cn{page}'.format(page=aaurl)

                print(imgurl, "————", aurl)
                yield Request(url=aurl, meta={"myimg_url": imgurl}, callback=self.parsedetail)
                # yield Request(url=parse.urljoin(response.url,aurl), meta={"myimg_url":imgurl},callback=self.parsedetail)

            next = response.css("div.page ::attr(href)").extract()[4]
            next_page = 'http://www.zuofan.cn{page}'.format(page=next)
            print("正在爬去第%s页："%count, next_page)
            if next_page:
                yield Request(url=next_page, callback=self.parse)



    def parsedetail(self,response):
        title = response.xpath('/html/body/div[4]/div/div[2]/div[2]/h1/text()').extract()[0]
        print("标题:", title)

        time = response.xpath('/html/body/div[4]/div/div[2]/div[2]/div[2]/span[1]/text()').extract()[0]
        time_new1=time.strip().replace("时间：","")
        time_new=time_new1.split(' ')[0]
        print("创建时间：",time_new)

        cook_o=response.xpath('/ html / body / div[4] / div / div[2] / div[2] / div[2] / span[2]/text()').extract()[0]
        cook = cook_o.strip().replace("厨师：", "")
        print("厨师：",cook)

        source_o=response.xpath('/html/body/div[4]/div/div[2]/div[2]/div[2]/span[3]/text()').extract()[0]
        source=source_o.strip().replace("出处：", "")
        print("出处：",source)

        look=response.xpath('/html/body/div[4]/div/div[2]/div[2]/div[2]/span[4]/text()').extract()[0]
        look_num=look.strip().replace("人做过这道菜", "")
        print('浏览量：',look_num)

        abstract = response.css("div.efficacy ::text").extract()[2]
        print('摘要：',abstract)

        list_yuanliao=response.css("div.yuanliao li::text").extract()
        str_yl = [i for i in list_yuanliao]
        str_yl = ' '.join(str_yl)
        str_yl=str_yl.replace("\t", "")
        str_yl = str_yl.replace("\n", "")
        print("原料：",str_yl)

        list_tiaoliao=response.css("div.tiaoliao li::text").extract()
        str_tl = [i for i in list_tiaoliao]
        str_tl = ' '.join(str_tl)
        str_tl = str_tl.replace("\t", "")
        str_tl = str_tl.replace("\n", "")
        print("调料：", str_tl)

        jiqiao=response.xpath('/html/body/div[4]/div/div[2]/div[2]/div[6]/p/text()').extract()
        str_jq = [i for i in jiqiao]
        str_jq = '，'.join(str_jq)
        print("小技巧：",str_jq)

        buzhou=response.css("div.zuofa p::text").extract()
        str_bz = [i for i in buzhou]
        str_bz = '——'.join(str_bz)
        print("步骤：",str_bz)

        # 下载标题图片
        titleimage = response.meta.get("myimg_url", "")    #meta是Request函数中传入的参数值，传递到下一个函数
        print("标题图片：",titleimage)

        print('-'*50)

        # 标题:title    创建时间：time_new    "厨师：",cook   "出处：",source
        # '浏览量：',look_num   '摘要：',abstract    "原料：",str_yl   "调料：", str_tl
        # "小技巧：",str_jq     "步骤：",str_bz
    # 将数据存入item对象
        zfiem=ZuofanItem()
        zfiem['title']=title
        zfiem['time_new']=time_new
        zfiem['cook']=cook
        zfiem['source']=source
        zfiem['look_num']=look_num
        zfiem['abstract']=abstract
        zfiem['str_yl']=str_yl
        zfiem['str_tl']=str_tl
        zfiem['str_jq']=str_jq
        zfiem['str_bz']=str_bz
        zfiem['titleimage']=[titleimage]

        # 将item传给pipelines
        yield zfiem



