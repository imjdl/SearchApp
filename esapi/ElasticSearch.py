#!/usr/bin/env python3
# coding = utf-8
__all__ = ["ElastciSearch"]
__doc__ = """

ElasticSearch 的操作
os:linux;app:wordpress;ip:210.43.32.32/16;
"""

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import ConnectionError, ConnectionTimeout
from config.baseconfig import ELASTICSEARCH_HOST_LIST, ES_MAPPING, ES_INDEX_NAME, ES_DOC_TYPE
import re

class ElastciSearch(object):

    def __init__(self):
        self.es = Elasticsearch(hosts=ELASTICSEARCH_HOST_LIST)
        self.index_name = ES_INDEX_NAME
        self.doc_type = ES_DOC_TYPE
        if not self.es.indices.exists(index=self.index_name):
            self.create_mapping()
        self.search_type = ["os", "ip", "app", "title", "port", "code", "domain"]
        self.switch = {
            "os": self.getos,
            "app": self.getapp,
            "ip": self.getip,
            "title": self.gettitle,
            "port": self.getport,
            "code": self.getstatecode,
            "domain": self.getinfofordomain,
        }

    def create_mapping(self):

        """
        创建mapping
        """
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, body=ES_MAPPING)
        except ConnectionError as e:
            print("ConnectionERROR: 请检查你的配置文件")

    def bulk(self, datas):
        """
        批量导入
        """
        # 判断 index 是否存在
        if not self.es.indices.exists(self.index_name):
            print("索引不存在，请先创建索引")
            return False
        actions = []
        for data in datas:
            action = {
                "_index": self.index_name,
                "_type": self.doc_type,
                "_id": data["ip"] + ":" + str(data["port"]),
                "ip": data["ip"],
                "state_code": data["state_code"],
                "body": data["body"],
                "date": data["date"],
                "title": data["title"],
                "server": data["server"],
                "x-powered-by": data["x-powered-by"],
                "header": data["header"],
                "web_type": data["web_type"],
                "port": data["port"],
            }
            actions.append(action)

        bulk(client=self.es, actions=actions, index=self.index_name, doc_type=self.doc_type)

    def search(self, datas, page):
        """
        datas is like os:linux;app:wordpress;ip:210.43.32.30/26;
        or os:linux;app:wordpress;ip:210.43.32.30/26
        """
        if page < 0:
            page = 1
        return self.analysis(datas, page)

    def analysis(self, datas, page):
        """
        分析搜索语句，返回es搜索的json
        :param datas:str
        :return: dict
        """
        datas = datas.lower()
        if "=" not in datas:
            return self.getall(datas, page)
        datas = datas.split(":")
        if "" in datas:
            datas.remove("")
        keys = []
        values = []
        for data in datas:
            key, value = data.split("=")
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
                    "fields": ["server^3", "title^2"]
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
                            "ip": ips
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
                    "fields": ["web_type^5", "x-powered-by^4", "server^3", "title^2", "body^1"]
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
                    "title": value
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
                    "fields": ["title^5", "server^4", "x-powered-by^3", "web_type^2", "body^1"]
                }
            },
            "from": (page-1)*10,
            "size": 10
        }
        res = self.es.search(index=self.index_name, doc_type=self.doc_type, body=data)
        return res["hits"]

    def getport(self, value, page):
        data = {
            "query": {
                "match": {
                    "port": value
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
                    "state_code": value
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return data

    def getinfofordomain(self, value, page):
        import socket
        ip = socket.gethostbyname(value)
        print(ip)
        return self.getip(ip, page)

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
    # es.create_mapping()
    # datas = [{
    #     "ip": "210.43.32.30",
    #     "state_code": 200,
    #     "body": "a",
    #     "header": "aa",
    # }]
    # es.bulk(index_name="searchwebapp", datas=datas)
    # print(es.analysis("ip:210.43.32.30"))
    # print(es.analysis("ip:210.43.32.1/24"))
    es.analysis("ip:47.94.1.1/16;os:linux", 1)


if __name__ == '__main__':
    main()
