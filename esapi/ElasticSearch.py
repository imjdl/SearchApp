#!/usr/bin/env python3
# coding = utf-8
__all__ = ["ElastciSearch"]
__doc__ = """

ElasticSearch 的操作
os:linux;app:wordpress;ip:210.43.32.32/16;
"""

from elasticsearch import Elasticsearch
from config.baseconfig import ELASTICSEARCH_HOST_LIST, ES_INDEX_NAME, ES_DOC_TYPE
import re


class ElastciSearch(object):

    def __init__(self):
        self.es = Elasticsearch(hosts=ELASTICSEARCH_HOST_LIST)
        self.index_name = ES_INDEX_NAME
        self.doc_type = ES_DOC_TYPE
        # if not self.es.indices.exists(index=self.index_name):
        #     self.create_mapping()
        self.search_type = ["os", "ip", "app", "title", "port", "statecode", "protocol", "domain"]
        self.switch = {
            "os": self.getos,
            "app": self.getapp,
            "ip": self.getip,
            "title": self.gettitle,
            "port": self.getport,
            "statecode": self.getstatecode,
            "protocol": self.getprotocolmsg,
            "domain": self.getinfofordomain,
        }

    def search(self, datas, page):
        """
        datas is like os:linux & app:wordpress & ip:210.43.32.30/26;
        or os:linux & app:wordpress & ip:210.43.32.30/26
        """
        if page < 0:
            page = 1
        return self._analysis(datas, page)

    def _analysis(self, datas, page):
        """
        分析搜索语句，返回es搜索的json
        :param datas:str
        :return: dict
        """
        datas = datas.lower()
        if ":" not in datas:
            return self.getall(datas, page)
        datas = datas.split("&")
        if "" in datas:
            datas.remove("")
        keys = []
        values = []
        for data in datas:
            key, value = data.split(":")
            key = key.strip()
            value = value.strip()
            if key not in self.search_type:
                return False, None
            keys.append(key)
            values.append(value)
        data = {}
        # 简单查询
        if len(keys) == 1:
            data = self.switch[keys[0]](values[0], page)
        else:
            # 组合查询
            # ip os app port code title 以后可以加一个非 ！ 取反的判断，这个版本先不加
            datas = {}
            for i in range(len(keys)):
                datas[keys[i]] = values[i]
            data = self.combination(datas=datas, page=page)
        if data:
            res = self.es.search(index=self.index_name, doc_type=self.doc_type, body=data)
            return res["hits"], keys
        else:
            return False, keys

    def getos(self, value, page):
        data = {
            "query": {
                "multi_match": {
                    "query": value,
                    "fields": ["OS^4", "SERVER^3", "TITLE^2", "CONTENT^1"]
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return data

    def getip(self, value, page):
        if "/" in value:
            pattern = re.compile('(([25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}([25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\/(16|24)')
            if pattern.match(value):
                cidr = value.split("/")[-1]
                ips = []
                if cidr == "16":
                    ip = ".".join(value.split(".")[:2]) + "."
                    for i in range(0, 256):
                        for j in range(0, 256):
                            ips.append(ip + str(i) + "." + str(j))
                elif cidr == "24":
                    ip = ".".join(value.split(".")[:3]) + "."
                    for i in range(0,256):
                        ips.append(ip + str(i))
                data = {
                    "query": {
                        "terms": {
                            "HOST": ips
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10
                }
                return data
            else:
                return False
        else:
            pattern = re.compile('(([25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}([25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))')
            if pattern.match(value):
                data = {
                    "query": {
                        "term": {
                            "ip": value
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10
                }
                return data
            else:
                return False

    def getapp(self, value, page):
        data = {
            "query": {
                "multi_match": {
                    "query": value,
                    "fields": ["BANNER^5", "SERVER^4", "TITLE^3", "CONTENT^2"]
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return data

    def gettitle(self, value, page):
        data = {
            "query": {
                "match": {
                    "TITLE": value
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return data

    def getall(self, value, page):
        data = {
            "query": {
                "multi_match": {
                    "query": value,
                    "fields": ["TITLE^6", "HEADERS^5", "CONTENT^4", "SERVER^3", "BANNER^2", "EXTRAINFO^1"]
                }
            },
            "from": (page-1)*10,
            "size": 10
        }
        res = self.es.search(index=self.index_name, doc_type=self.doc_type, body=data)
        return res["hits"], value

    def getport(self, value, page):
        data = {
            "query": {
                "match": {
                    "PORT": value
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return data

    def getstatecode(self, value, page):
        data = {
            "query": {
                "match": {
                    "STATE_CODE": value
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return data

    def getinfofordomain(self, value, page):
        import socket
        ip = socket.gethostbyname(value)
        return self.getip(ip, page)

    def getprotocolmsg(self, value, page):
        data = {
            "query": {
                "match": {
                    "PROTOCOL": value
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return data

    # 获取一个ip的所有信息
    def getipmsg(self, value):
        data = {
             "query": {
                "term": {
                    "ip": {
                        "value": value
                    }
                }
            }
        }
        res = self.es.search(index=self.index_name, doc_type=self.doc_type, body=data)
        return res["hits"]

    def combination(self, datas=None, page=None):
        """
        组合查询
        """
        must = []
        for key, value in datas.items():
            must.append(self.switch[key](value, page)["query"])
        fiter = must.pop()
        data = {
            "query": {
                "bool": {
                    "must": must
                    ,
                    "filter": fiter
                }
            }
        }
        return data


    def delete(self, datas):
        pass


def main():
    es = ElastciSearch()
    # res = es.search("statecode:200", 1)
    res = es.search("linux", 1)
    print(res)


if __name__ == '__main__':
    main()
