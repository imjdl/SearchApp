from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from esapi.ElasticSearch import ElastciSearch
from search.models import SearchLog
import time

es = ElastciSearch()
# Create your views here.


def index(request):
    return render(request, 'search/index.html')


def results(request):
    '''
    展示搜索的结果
    统计搜索
    :param request:
    :return:
    '''
    msg = request.GET.get("search_msg", None)
    page = request.GET.get("page", 1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    if msg == '':
        return render(request, 'search/error.html', context={"msg": msg})
    start_time = time.time()
    res, keys = es.search(msg, page)
    if not isinstance(keys, list):
        keys = [keys]
    end_time = time.time()
    s = SearchLog()
    if "HTTP_X_FORWARDED_FOR" in request.META.keys():
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    s.searcher_IP = ip
    s.searcher_content = msg
    s.save()
    colors = ["badge-danger", "badge-info", "badge-light", "badge-primary", "badge-warning"]
    if res:
        datas = []
        for i in res["hits"]:
            data = {}
            data["HOST"] = i["_source"]["HOST"]
            try:
                data["PROTOCOL"] = i["_source"]["PROTOCOL"].split(":")[1]
            except Exception as e:
                data["PROTOCOL"] = i["_source"]["PROTOCOL"]
            data["TITLE"] = i["_source"]["TITLE"]
            data["PORT"] = str(i["_source"]["PORT"])
            data["DATE"] = i["_source"]["DATE"]
            data["VENDOR"] = i["_source"]["VENDOR"].strip()
            data["OS"] = i["_source"]["OS"]
            data["SERVER"] = i["_source"]["SERVER"]
            data["SERVER_VERSION"] = i["_source"]["SERVER_VERSION"]
            data["EXTRAINFO"] = i["_source"]["EXTRAINFO"]
            data["BANNER"] = i["_source"]["BANNER"]
            data["STATE_CODE"] = i["_source"]["STATE_CODE"]
            print(i["_source"]["HEADERS"])
            data["HEADERS"] = i["_source"]["HEADERS"]
            data["CONTENT"] = i["_source"]["CONTENT"]
            # data["LOCATION"] = i["_source"]["date"]
            data["TIME_ZONE"] = i["_source"]["TIME_ZONE"]
            data["CONTINENT"] = i["_source"]["CONTINENT"]
            data["COUNTRY"] = i["_source"]["COUNTRY"]
            data["PROVINCE"] = i["_source"]["PROVINCE"]
            data["CITY"] = i["_source"]["CITY"]
            if "http" in data["PROTOCOL"]:
                data["URI"] = "http://" + data["HOST"] + ":" + data["PORT"]
            else:
                data["URI"] = ""
            datas.append(data)
        pages = Paginator([x for x in range(res["total"])], 10)

        if page > pages.num_pages:
            page = pages.num_pages
        if page < 1:
            page = 1
        try:
            articles_page = pages.page(page)
        except NameError:
            articles_page = pages.page(1)

        return render(request, 'search/html/showdata.html',
                      context={"msg": msg, "total": res["total"], "time": end_time - start_time, "datas": datas,
                               'articles_page': articles_page, 'pages': getpages(pages.num_pages, page), "keys": keys,
                               "colors": colors})
    else:
        # 处理不存在的数据
        return render(request, 'search/html/showdata.html',
                      context={"msg": msg, "total": 0, "time": end_time - start_time, "datas": None,
                               'articles_page': None, 'pages': None, "keys": keys, "colors": colors})


def result(request, IP):
    '''
    展示一个具体的结果
    :param request:
    {
        "IP":"",
        "LN":"",
        "LE":"",
        "OS":"",
        "TIME_ZONE":"",
        "CONTINENT":"",
        "COUNTRY":"",
        "PROVINCE":"",
        "CITY":"",
        "PORTS":[]
        "INFO":[
            {
                "PORT":"",
                "PROTOCOL": [],
                "SERVER": "",
                "SERVER_VERSION": "",
                "BANNER":"",
                "HEADERS":"",
                "CONTENT":"",
                "EXTRAINFO":"",
            },
        ]
    }
    :return:
    '''
    res = es.getipmsg(IP)
    total = res["total"]
    if total != 0:
        data = {}
        data["IP"] = res["hits"][0]["_source"]["HOST"]
        data["LN"] = res["hits"][0]["_source"]["LOCATION"]["LATITUDE"]
        data["LE"] = res["hits"][0]["_source"]["LOCATION"]["LOGITUDE"]
        if  res["hits"][0]["_source"]["EXTRAINFO"]:
            data["OS"] = res["hits"][0]["_source"]["EXTRAINFO"] + "," + res["hits"][0]["_source"]["OS"]
        else:
            data["OS"] = res["hits"][0]["_source"]["OS"]

        data["TIME_ZONE"] = res["hits"][0]["_source"]["TIME_ZONE"]
        data["CONTINENT"] = res["hits"][0]["_source"]["CONTINENT"]
        data["COUNTRY"] = res["hits"][0]["_source"]["COUNTRY"]
        data["PROVINCE"] = res["hits"][0]["_source"]["PROVINCE"]
        data["CITY"] = res["hits"][0]["_source"]["CITY"]
        data["PORTS"] = []
        data["INFO"] = []
        for ip in res["hits"]:
            port_info = {}
            port_info["PORT"] = ip["_source"]["PORT"]
            port_info["PROTOCOL"] = ip["_source"]["PROTOCOL"].split(":")
            port_info["SERVER"] = ip["_source"]["SERVER"]
            port_info["SERVER_VERSION"] = ip["_source"]["SERVER_VERSION"]
            port_info["BANNER"] = ip["_source"]["BANNER"]
            port_info["HEADERS"] = ip["_source"]["HEADERS"]
            port_info["CONTENT"] = ip["_source"]["CONTENT"]
            data["INFO"].append(port_info)
            data["PORTS"].append(ip["_source"]["PORT"])
        print(data)
        return render(request, 'search/html/data.html', context=data)
    else:
        return render(request, "search/html/data.html", context={})


def getpages(val, nowpage):
    if val < 10:
        return [x for x in range(1, val + 1)]
    else:
        if nowpage - 1 <= 4:
            page_list = list(range(1, nowpage+3))
            page_list.append('...')
            page_list.append(val)
            return page_list
        elif val - nowpage <= 4:
            page_list = list(range(nowpage - 2, val+1))
            return [1] + ['...'] + page_list
        else:
            page_list = list(range(nowpage - 2, nowpage + 3))
            return [1] + ['...'] + page_list + ['...'] + [val]
