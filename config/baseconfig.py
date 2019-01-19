import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
    'Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 '
    'Safari/537.17',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 '
    'Safari/537.36',
    'curl/7.58.0',
]


def random_header():
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    return headers


ELASTICSEARCH_HOST_LIST = [{"host": "127.0.0.1", "port": 9200}]


# 可以在这里写mapping信息
ES_INDEX_NAME = "searchwebapp"
ES_DOC_TYPE = "search"

ES_MAPPING = {
"settings": {
    "number_of_replicas": 1,
    "number_of_shards": 5
  },
  "mappings": {
    ES_DOC_TYPE : {
      "properties": {
        "ip":{
          "type": "keyword"
        },
        "state_code":{
          "type": "integer"
        },
        "header":{
          "type": "text",
          "analyzer": "ik_max_word"
        },
        "body":{
          "type": "text",
          "analyzer": "ik_max_word"
        },
        "date":{
          "type": "date",
          "format": "yyyy年MM月dd日HH时mm分ss秒"
        },
        "title":{
          "type": "text",
          "analyzer": "ik_max_word"
        },
        "server":{
          "type": "text",
          "analyzer": "ik_max_word"
        },
        "x-powered-by":{
          "type": "text",
          "analyzer": "ik_max_word"
        },
        "web_type":{
          "type": "text",
          "analyzer": "ik_max_word"
        },
        "port":{
          "type": "integer"
        }
      }
    }
  }
}
