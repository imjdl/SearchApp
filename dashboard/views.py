from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

import netifaces
from .models import Job, Scanner
from datetime import datetime
import uuid
import requests
import json

# Create your views here.


@login_required(login_url='/admin/login/')
def index(requset):
    return render(requset, 'dashboard/index.html')


def login(request):
    if request.method == "GET":
        next_url = request.GET.get("next", "/")
        return render(request, 'dashboard/html/login.html', context={"next": next_url})
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        next_url = request.POST.get("next", "/")
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            return render(request, 'dashboard/html/login.html', context={"msg": "用户名或密码错误", "next": next_url})


@login_required(login_url='/admin/login/')
def console(request):
    interfaces = netifaces.interfaces()
    jobs = Job.objects.all()
    return render(request, 'dashboard/html/console.html', context={"interfaces": interfaces})


@login_required(login_url='/admin/login/')
def create_scanner(request):
    '''
    create scanner
    :param request:
    :return: json
    '''
    # Judge request method
    if request.method != "POST":
        return render(request, "dashboard/html/create_scanner.html")
    # Parsing parameters
    params = {
        "scanner-host": "",
        "scanner-port": 8080,
        "es-hosts": "",
        "es-port": 9200,
        "es-user": "",
        "es-pass": "",
        "borker-type": "",
        "borker-user": "",
        "borker-pass": "",
        "borker-host": "",
        "borker-port": 0,
        "borker-db": "",
        "backend-type": "",
        "backend-user": "",
        "backend-pass": "",
        "backend-host": "",
        "backend-port": 0,
        "backend-db": "",
    }
    for key, vaule in request.POST.items():
        if key == "csrfmiddlewaretoken":
            continue
        if key not in params.keys():
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)

        # 必要关键字不能为空 ampq时borker_user 和 backend_user不能为空
        if vaule == "" and key not in ["es-user", "es-pass", "borker-user", "backend-user"]:
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
        params[key] = vaule
    scanner_url = "http://" + params["scanner-host"] + ":" + params["scanner-port"]
    # 尝试连接
    try:
        requests.get(url=scanner_url, timeout=(10, 15))
    except Exception as e:
        print(e)
        return JsonResponse(data={"status": "failure", "info": "Scanner server connect timeout"}, status=401)

    scanner_url += "/install/?es_hosts=%s&es_port=%s&es_user=%s&es_pass=%s&backend_type=%s&backend_user=%s" \
                   "&backend_pass=%s&backend_host=%s&backend_port=%s&backend_db=%s&borker_type=%s&borker_user=%s" \
                   "&borker_pass=%s&borker_host=%s&borker_port=%s&borker_db=%s" % (
        params["es-hosts"], params["es-port"], params["es-user"], params["es-pass"], params["backend-type"],
        params["backend-user"], params["backend-pass"], params["backend-host"], params["backend-port"],
        params["backend-db"], params["borker-type"], params["borker-user"], params["borker-pass"],
        params["borker-host"], params["borker-port"], params["borker-db"])
    # Create scanner & write configuration
    try:
        res = requests.get(url=scanner_url)
        data = json.loads(res.text)
        if res.status_code == 200:
            # Save to database
            s = Scanner()
            s.scanner_token = data["info"]
            s.scanner_ip = params["scanner-host"]
            s.scanner_port = int(params["scanner-port"])
            s.scanner_status = 1
            s.scanner_es_hosts = params["es-hosts"]
            s.scanner_es_port = int(params["es-port"])
            s.scanner_es_user = params["es-user"]
            s.scanner_es_pass = params["es-pass"]

            s.scanner_borker_type = params["borker-type"]
            s.scanner_borker_user = params["borker-user"]
            s.scanner_borker_pass = params["borker-pass"]
            s.scanner_borker_host = params["borker-host"]
            s.scanner_borker_port = int(params["borker-port"])
            s.scanner_borker_db = params["borker-db"]

            s.scanner_backend_type = params["backend-type"]
            s.scanner_backend_user = params["backend-user"]
            s.scanner_backend_pass = params["backend-pass"]
            s.scanner_backend_host = params["backend-host"]
            s.scanner_backend_port = int(params["backend-port"])
            s.scanner_backend_db = params["backend-db"]
            s.save()
        return JsonResponse(data=data, status=res.status_code)
    except Exception as e:
        return JsonResponse(data={"status": "failure", "info": "Scanner server connect timeout"}, status=401)


@login_required(login_url='/admin/login/')
def scanner_list(request):
    return render(request, "dashboard/html/scanner_list.html")


@login_required(login_url='/admin/login/')
def scanner_list_api(request):
    '''
    get scanner list
    :param request:
    :return:
    '''
    scanners = Scanner.objects.all()
    datas = {"datas": []}
    for scanner in scanners:
        data = {}
        data["id"] = scanner.scanner_id
        data["ip"] = scanner.scanner_ip
        data["port"] = str(scanner.scanner_port)
        data["status"] = str(scanner.scanner_status)
        datas["datas"].append(data)
    return JsonResponse(data=datas, status=200)


@login_required(login_url='/admin/login/')
def search_log(request):
    return render(request, "dashboard/html/search_log.html")


@login_required(login_url='/admin/login/')
def search_log_api(request):
    page = request.GET.get("page", 1)
    query = request.GET.get("query", None)
    try:
        page = int(page)
    except ValueError:
        page = 1
    from search.models import SearchLog
    if query == None:
        search_log_count = SearchLog.objects.count()
        pages = Paginator([x for x in range(search_log_count)], 10)
        if page > pages.num_pages:
            page = pages.num_pages
        if page < 1:
            page = 1
        search_logs = SearchLog.objects.order_by("-searcher_ID")[(page-1) * 10: page * 10]
    else:
        search_logs = SearchLog.objects.filter(searcher_content__icontains=query)
        search_log_count = len(search_logs)
        pages = Paginator([x for x in range(search_log_count)], 10)
        if page > pages.num_pages:
            page = pages.num_pages
        if page < 1:
            page = 1
        search_logs = search_logs[(page-1) * 10: page * 10]
    logs = {"logs": [], "page": page, "paginator": getpages(pages.num_pages, page)}
    for log in search_logs:
        data = {}
        data["id"] = log.searcher_ID
        data["ip"] = log.searcher_IP
        data["date"] = log.searcher_date
        data["content"] = log.searcher_content
        logs["logs"].append(data)
    return JsonResponse(data=logs, status=200)


@login_required(login_url='/admin/login/')
def deletelog(request):
    from search.models import SearchLog
    id = request.GET.get("id", None)
    if id == None:
        return JsonResponse(data={"status": False})
    try:
        id = int(id)
    except Exception as e:
        return JsonResponse(data={"status": False})
    try:
        SearchLog.objects.get(searcher_ID=id).delete()
        return JsonResponse(data={"status": True})
    except Exception as e:
        return JsonResponse(data={"status": False})


@login_required(login_url='/admin/login/')
def create(request):
    title = request.POST.get("title", None)
    desc = request.POST.get("desc", None)
    dst_port = request.POST.get("dst_port", None)
    src_port = request.POST.get("src_port", None)
    ip = request.POST.get("ip", None)
    networkcard = request.POST.get("networkcard", None)
    src_ip = netifaces.ifaddresses(networkcard)[2][0]["addr"]
    try:
        dst_port = int(dst_port)
        src_port = int(src_port)
    except ValueError:
        return JsonResponse({"msg": 0})
    uuid_job = str(uuid.uuid1())
    job = Job.objects.create(uuid=uuid_job, title=title, desc=desc, dst_port=dst_port, src_port=src_port, subnets=ip, network_card=networkcard, status=0, progress_rate=0, start_time=datetime.now())
    job.save()
    data = []
    data.append(job.uuid)
    data.append(job.title)
    data.append(job.dst_port)
    data.append(job.src_port)
    data.append(job.subnets)
    data.append(job.network_card)
    data.append(src_ip)
    data.append(job.start_time.strftime('%Y/%m/%d/%H:%M:%S'))
    data.append(job.status)
    data.append(job.progress_rate)
    return JsonResponse({"msg": 1, "data": data})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def getpages(val, nowpage):
    if val < 10:
        return [x for x in range(1, val+1)]
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
