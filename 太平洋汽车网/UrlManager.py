#地址管理器
class UrlManager():
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    # 添加新的
    def add_url(self, url):
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

     #检查是否存在
    def has_url(self):
        if len(self.new_urls) != 0:
            return True
        else:
            return False

    #将新得到的添加
    def get_url(self):
        url_temp = self.new_urls.pop()
        self.old_urls.add(url_temp)
        return url_temp