import os

ELASTICSEARCH_HOST_LIST = [{"host": "192.168.151.128", "port": 9200}]
ES_INDEX_NAME = "searchdb"
ES_DOC_TYPE = "search"
VUL_INDEX_NAME = "searchvul"
VUL_DOC_TYPE = "search"


def get_poc_tpl():
    path = os.path.dirname(os.path.abspath(__file__)) + "/PoC_tpl.txt"
    with open(path, "r") as f:
        return f.read()
