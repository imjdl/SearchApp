from django.db import models

# Create your models here.


class SearchLog(models.Model):
    # 一条搜索记录
    # id
    searcher_ID = models.IntegerField(primary_key=True)
    # 访问者IP
    searcher_IP = models.GenericIPAddressField(protocol="ipv4")
    # 搜索时间
    searcher_date = models.DateTimeField(auto_now=True)
    # 搜索语法
    searcher_content = models.TextField()

    def __str__(self):
        return self.searcher_IP + ":::" + self.searcher_conten