#!/usr/bin/env python3
# coding = utf-8
__all__ = ["ElastciSearch"]
__doc__ = """

ElasticSearch 的操作
os:linux;app:wordpress;ip:210.43.32.32/16;
"""

from elasticsearch import Elasticsearch
from config.baseconfig import ELASTICSEARCH_HOST_LIST, VUL_DOC_TYPE, VUL_INDEX_NAME


class ElastciSearch(object):

    def __init__(self):
        self.es = Elasticsearch(hosts=ELASTICSEARCH_HOST_LIST)
        self.index_name = VUL_INDEX_NAME
        self.doc_type = VUL_DOC_TYPE

    def search(self, poc_id):
        data = {
              "query": {
                    "match": {
                      "POCID": str(poc_id)
                    }
              }
        }
        res = self.es.search(index=self.index_name, doc_type=self.doc_type, body=data, scroll='1m')
        hits = []
        hits += res["hits"]["hits"]
        scroll_id = res["_scroll_id"]
        while True:
            hit = self.es.scroll(scroll_id=scroll_id, scroll="1m")["hits"]["hits"]
            hits += hit
            if hit == []:
                break
        return hits


def main():
    es = ElastciSearch()
    res = es.search(1)
    print(res)


if __name__ == '__main__':
    main()
