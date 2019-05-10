from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Scanner
import requests
import json
import base64

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


# @login_required(login_url='/admin/login/')
# def console(request):
#     interfaces = netifaces.interfaces()
#     jobs = Job.objects.all()
#     return render(request, 'dashboard/html/console.html', context={"interfaces": interfaces})


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
    # scanner_url = "http://" + params["scanner-host"] + ":" + params["scanner-port"]
    scanner_url = "http://" + params["scanner-host"] + ":" + params["scanner-port"]
    # 尝试连接
    try:
        requests.get(url=scanner_url, timeout=(10, 15))
    except Exception as e:
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
    for sc in Scanner.objects.all():
        sc.get_state()
        sc.save()
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
        datas["token"] = str(scanner.scanner_token)
    return JsonResponse(data=datas, status=200)


# 显示一个Scanner的详细信息
@login_required(login_url='/admin/login/')
def scanner(request, ID):
    from dashboard.models import Scanner
    sc = Scanner.objects.get(scanner_id=ID)
    data = {}
    data["id"] = sc.scanner_id
    data["ip"] = sc.scanner_ip
    data["port"] = sc.scanner_port
    data["token"] = sc.scanner_token
    status = {
        0:"shutdown",
        1: "runing",
        2: "unable to connect"
    }
    data["date"] = sc.scanner_date
    data["status"] = status[sc.scanner_status]
    data["eshosts"] = sc.scanner_es_hosts
    data["esport"] = sc.scanner_es_port
    data["esuser"] = sc.scanner_es_user
    data["espasswd"] = sc.scanner_es_pass
    data["borkerhost"] = sc.scanner_borker_host
    data["borkerport"] = sc.scanner_borker_port
    data["borkeruser"] = sc.scanner_borker_user
    data["borkerpass"] = sc.scanner_borker_pass
    data["borkerdb"] = sc.scanner_borker_db
    data["borkertype"] = sc.scanner_borker_type
    data["backendhost"] = sc.scanner_backend_host
    data["backendport"] = sc.scanner_backend_port
    data["backenduser"] = sc.scanner_backend_user
    data["backendpasswd"] = sc.scanner_backend_pass
    data["backenddb"] = sc.scanner_backend_db
    data["backendtype"] = sc.scanner_backend_type
    return render(request, "dashboard/html/scanner.html", context=data)


@login_required(login_url='/admin/login/')
def scanner_update(request):
    from dashboard.models import Scanner
    # Judge request method
    if request.method != "POST":
        return JsonResponse(data={"status": "failure", "info": "The failed request method must be POST!!!"}, status=200)
    # Parsing parameters
    params = {
        "scanner-status": "",
        "scanner-id": "",
        "scanner-token": "",
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
    sc = Scanner.objects.get(scanner_id=params["scanner-id"])
    # 修改远程配置
    scanner_url = "http://" + params["scanner-host"] + ":" + params["scanner-port"]
    # 尝试连接
    try:
        requests.get(url=scanner_url, timeout=(10, 15))
    except Exception as e:
        return JsonResponse(data={"status": "failure", "info": "Scanner server connect timeout"}, status=401)

    scanner_url += "/install/update/?es_hosts=%s&es_port=%s&es_user=%s&es_pass=%s&backend_type=%s&backend_user=%s" \
                   "&backend_pass=%s&backend_host=%s&backend_port=%s&backend_db=%s&borker_type=%s&borker_user=%s" \
                   "&borker_pass=%s&borker_host=%s&borker_port=%s&borker_db=%s&token=%s" % (
                       params["es-hosts"], params["es-port"], params["es-user"], params["es-pass"],
                       params["backend-type"],
                       params["backend-user"], params["backend-pass"], params["backend-host"], params["backend-port"],
                       params["backend-db"], params["borker-type"], params["borker-user"], params["borker-pass"],
                       params["borker-host"], params["borker-port"], params["borker-db"], params["scanner-token"])
    try:
        res = requests.get(url=scanner_url)
        data = json.loads(res.text)
        sc.scanner_ip = params["scanner-host"]
        sc.scanner_port = params["scanner-port"]
        sc.scanner_es_hosts = params["es-hosts"]
        sc.scanner_es_port = params["es-port"]
        sc.scanner_es_user = params["es-user"]
        sc.scanner_es_pass = params["es-pass"]
        sc.scanner_borker_host = params["borker-host"]
        sc.scanner_borker_port = params["borker-port"]
        sc.scanner_borker_type = params["borker-type"]
        sc.scanner_borker_user = params["borker-user"]
        sc.scanner_borker_pass = params["borker-pass"]
        sc.scanner_borker_db = params["borker-db"]
        sc.scanner_backend_host = params["backend-host"]
        sc.scanner_backend_port = params["backend-port"]
        sc.scanner_backend_type = params["backend-type"]
        sc.scanner_backend_user = params["backend-user"]
        sc.scanner_backend_pass = params["backend-pass"]
        sc.scanner_backend_db = params["backend-db"]
        sc.save()
        return JsonResponse(data=data, status=res.status_code)
    except Exception as e:
        pass
    return JsonResponse(data={"status": "success", "info": "scanner update"}, status=200)


@login_required(login_url='/admin/login/')
def scanner_oper(request):
    from dashboard.models import Scanner
    id = request.GET.get("id")
    oper_type = request.GET.get("type")
    oper = ["stop", "start", "restart", "flush", "delete"]
    if id == None or oper_type == None or oper_type not in oper:
        return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
    sc = Scanner.objects.get(scanner_id=id)
    if oper_type == "delete":
        Scanner.objects.filter(scanner_id=id).delete()
        return JsonResponse(data={"status": "success", "info": "scanner delete success"}, status=200)
        # res = sc.uninstall()
        # if res["status"] == "success":
        #     Scanner.objects.filter(scanner_id=id).delete()
        #     return JsonResponse(data={"status": "success", "info": "scanner delete success"}, status=200)
        # else:
        #     return JsonResponse(data=res, status=200)
    else:
        if oper_type == "stop":
            res = sc.stop()
        if oper_type == "start":
            res = sc.start()
        if oper_type == "restart":
            res = sc.restart()
        if oper_type == "flush":
            res = sc.get_state()
        sc.save()
        return JsonResponse(data=res, status=200)


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
def zmap_scan_task(request):
    from .models import Scanner
    import timezone_field
    datas = {}
    # 更新所有扫描器状态
    for sc in Scanner.objects.all():
        sc.get_state()
        sc.save()
    # 获取扫描器列表
    scanners = list(Scanner.objects.all())
    # 检查是否有可用的扫描器
    flag = False
    for scanner in scanners:
        flag = True if scanner.scanner_status == 1 else False
    if not flag:
        return render(request, "dashboard/html/scan_task_error.html", context={"msg": "没有可用的扫描器，请先创建。"})
    datas["scanners"] = scanners
    # 获取timezone
    timezone = timezone_field.TimeZoneField()
    timezones = []
    for tz in timezone.flatchoices:
        timezones.append(str(tz[0]))
    datas["timezones"] = timezones
    return render(request, "dashboard/html/zmap_scan_task.html", context=datas)


@login_required(login_url='/admin/login/')
def create_zmap_scan_task(request):
    from dashboard.models import Scanner
    if request.method != "POST":
        return render(request, "dashboard/html/zmap_scan_task.html")
    params = {
        "scanners_id": "",
        "name": "",
        "task_name": "",
        "enable": "",
        "desc": "",
        "every": "",
        "period": "",
        "minute": "",
        "hour": "",
        "dayofweek": "",
        "dayofmonth": "",
        "monthofyear": "",
        "timezone": "",
        "one_of_task": "",
        "port": "",
        "cidr": "",
    }
    for key, vaule in request.POST.items():
        if key == "csrfmiddlewaretoken":
            continue
        if key not in params.keys():
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)

        if vaule == "" and key in ["scanners_id", "name", "task_name", "port", "cidr"]:
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
        params[key] = vaule
    sc = Scanner.objects.get(scanner_id=params["scanners_id"])
    url = sc.get_url()
    if params["every"] == "":
        if params["hour"] == "" or params["minute"] == "" or params["dayofmonth"] == "" or params["dayofweek"] == "" or params["monthofyear"] == "" or params["timezone"] == "":
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
    else:
        params["hour"] = ""
        params["minute"] = ""
        params["dayofmonth"] = ""
        params["dayofweek"] = ""
        params["monthofyear"] = ""
        params["timezone"] = ""
    if params["enable"] == '1':
        params["enable"] = "on"
    else:
        params["enable"] = "off"
    task_name = {
        "0": "scanner_zmap.tasks.syn_scan",
        "1": "scanner_zmap.tasks.udp_scan",
    }
    if params["one_of_task"] == '1':
        params["one_of_task"] = 0
    else:
        params["one_of_task"] = 1
    params["task_name"] = task_name[params["task_name"]]
    params["period"] = params["period"].upper()
    params["name"] = params["name"].encode("UTF-8")
    params["desc"] = params["desc"].encode("UTF-8")
    import requests
    data = "token=%s&name=%s" \
           "&task_name=%s&description=%s&start_time=1&one_of_task=%d&enabled=%s&every=%s" \
           "&period=%s&crontab_minute=%s&crontab_hour=%s&crontab_day_of_week=%s&crontab_day_of_month=%s" \
           "&crontab_month_of_year=%s&crontab_time_zone=%s&ips=%s&port=%s" % \
           (sc.scanner_token, params["name"], params["task_name"], params["desc"], params["one_of_task"],
            params["enable"], params["every"], params["period"], params["minute"], params["hour"], params["dayofweek"],
            params["dayofmonth"], params["monthofyear"], params["timezone"], params["cidr"], params["port"])
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    try:
        res = requests.post(url=url + "/create_zmap/", headers=headers, data=data)
        return JsonResponse(data=json.loads(res.text), status=res.status_code)
    except Exception as e:
        return JsonResponse(data={"status": "failure", "info": "task create failure "}, status=503)


@login_required(login_url='/admin/login/')
def nmap_scan_task(request):
    from .models import Scanner
    import timezone_field
    datas = {}
    # 更新所有扫描器状态
    for sc in Scanner.objects.all():
        sc.get_state()
        sc.save()
    # 获取扫描器列表
    scanners = list(Scanner.objects.all())
    # 检查是否有可用的扫描器
    flag = False
    for scanner in scanners:
        flag = True if scanner.scanner_status == 1 else False
    if not flag:
        return render(request, "dashboard/html/scan_task_error.html", context={"msg": "没有可用的扫描器，请先创建。"})
    datas["scanners"] = scanners
    # 获取timezone
    timezone = timezone_field.TimeZoneField()
    timezones = []
    for tz in timezone.flatchoices:
        timezones.append(str(tz[0]))
    datas["timezones"] = timezones
    return render(request, "dashboard/html/nmap_scan_task.html", context=datas)


@login_required(login_url='/admin/login/')
def create_nmap_scan_task(request):
    from dashboard.models import Scanner
    if request.method != "POST":
        return render(request, "dashboard/html/nmap_scan_task.html")
    params = {
        "scanners_id": "",
        "name": "",
        "enable": "",
        "desc": "",
        "every": "",
        "period": "",
        "minute": "",
        "hour": "",
        "dayofweek": "",
        "dayofmonth": "",
        "monthofyear": "",
        "timezone": "",
        "one_of_task": "",
        "type": "",
        "datas": "",
    }
    for key, vaule in request.POST.items():
        if key == "csrfmiddlewaretoken":
            continue
        if key not in params.keys():
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)

        if vaule == "" and key in ["scanners_id", "name", "task_name", "type", "datas"]:
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
        params[key] = vaule
    sc = Scanner.objects.get(scanner_id=params["scanners_id"])
    url = sc.get_url()
    if params["every"] == "":
        if params["hour"] == "" or params["minute"] == "" or params["dayofmonth"] == "" or params["dayofweek"] == "" or params["monthofyear"] == "" or params["timezone"] == "":
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
    else:
        params["hour"] = ""
        params["minute"] = ""
        params["dayofmonth"] = ""
        params["dayofweek"] = ""
        params["monthofyear"] = ""
        params["timezone"] = ""
    if params["enable"] == '1':
        params["enable"] = "on"
    else:
        params["enable"] = "off"
    if params["one_of_task"] == '1':
        params["one_of_task"] = 0
    else:
        params["one_of_task"] = 1
    params["period"] = params["period"].upper()
    params["name"] = params["name"].encode("UTF-8")
    params["desc"] = params["desc"].encode("UTF-8")
    types = {
        "0": "port",
        "1": "cidr",
    }
    params["type"] = types[params["type"]]
    import requests
    data = "token=%s&name=%s" \
           "&description=%s&start_time=1&one_of_task=%d&enabled=%s&every=%s" \
           "&period=%s&crontab_minute=%s&crontab_hour=%s&crontab_day_of_week=%s&crontab_day_of_month=%s" \
           "&crontab_month_of_year=%s&crontab_time_zone=%s&type=%s&vaule=%s" % \
           (sc.scanner_token, params["name"], params["desc"], params["one_of_task"],
            params["enable"], params["every"], params["period"], params["minute"], params["hour"], params["dayofweek"],
            params["dayofmonth"], params["monthofyear"], params["timezone"], params["type"], params["datas"])
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    try:
        res = requests.post(url=url + "/create_nmap/", headers=headers, data=data)
        return JsonResponse(data=json.loads(res.text), status=res.status_code)
    except Exception as e:
        return JsonResponse(data={"status": "failure", "info": "task create failure "}, status=503)


@login_required(login_url='/admin/login/')
def scan_task_list(request):
    from dashboard.models import Scanner
    scanners = Scanner.objects.all()
    pages = len(scanners)
    page = request.GET.get("page")
    if page == None:
        page = 1
    else:
        page = int(page)
    if page <= 0:
        page = 1
    elif page > pages:
        page = pages
    node_task = []
    if pages == 0:
        return render(request, "dashboard/html/task_list.html", context={"node_task": []})
    scanners = scanners[(page - 1) * 10: page * 10]
    for scanner in scanners:
        data = {}
        data["scanner"] = str(scanner)
        data["scanner_id"] = scanner.scanner_id
        task = scanner.get_tasks()
        if task["status"] == "success":
            data["info"] = task["info"]
        else:
            data["info"] = []
        node_task.append(data)
    return render(request, "dashboard/html/task_list.html", context={"node_task": node_task})


@login_required(login_url='/admin/login/')
def get_task_detail(request):
    from dashboard.models import Scanner
    task_id = request.GET.get("task_id")
    scanner_id = request.GET.get("scanner_id")
    if task_id == None or scanner_id == None:
        return render(request, "dashboard/html/task_detail.html", context={"status": "failure", "info": "params is error"})
    try:
        scanner = Scanner.objects.get(scanner_id=scanner_id)
    except Exception as e:
        return render(request, "dashboard/html/task_detail.html", context={"status": "failure", "info": "params is error"})
    res = scanner.get_task_detail(task_id)
    return render(request, "dashboard/html/task_detail.html", context=res)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url='/admin/login/')
def poc(request):
    from config.baseconfig import get_poc_tpl
    from dashboard.models import PoC
    from dashboard.models import Product
    from dashboard.models import Vul
    if request.method == "GET":
        poc_tpl = get_poc_tpl()
        products = Product.objects.all()
        vuls = Vul.objects.all()
        return render(request, "dashboard/html/poc_add.html", context={"poc_tpl": poc_tpl, "products": products, "vuls": vuls})
    else:
        poc_name = request.POST.get("poc_name")
        keywords = request.POST.get("keywords")
        description = request.POST.get("description")
        product = request.POST.get("product")
        vul = request.POST.get("vul")
        date = request.POST.get("date")
        code = request.POST.get("code")
        if poc_name == "" or keywords == "" or deletelog == "" or product == "" or vul == "" or date == "" \
                or description == "" or code == "":
            return JsonResponse({"status": "failure", "info": "params is error"})
        poc = PoC()
        product = Product.objects.get(product_id=int(product))
        vul = Vul.objects.get(vul_id=int(vul))
        poc.poc_name = poc_name
        poc.poc_key = keywords
        poc.poc_desc = description
        poc.poc_product = product
        poc.poc_type = vul
        poc.poc_date = date
        code = code
        # code = base64.b64encode(code.encode("UTF-8")).decode("UTF-8")
        poc.poc_code = code
        poc.save()
        return JsonResponse(data={"status": "success", "info": "PoC added successfully"})


@login_required(login_url='/admin/login/')
def poc_list(request):
    from dashboard.models import PoC
    pocs = PoC.objects.all()
    return render(request, "dashboard/html/poc_list.html", context={"pocs": pocs})


@login_required(login_url='/admin/login/')
def poc_edit(request):
    from dashboard.models import PoC, Product, Vul
    if request.method == "GET":
        poc_id = request.GET.get("poc_id")
        if poc_id == "":
            return render(request, "dashboard/html/poc_edit.html", context={"pocs": ""})
        try:
            poc = PoC.objects.get(poc_id=poc_id)
            poc.poc_date = str(poc.poc_date)
            products = Product.objects.all()
            vuls = Vul.objects.all()
        except Exception as e:
            return render(request, "dashboard/html/poc_edit.html", context={"poc": ""})
        return render(request, "dashboard/html/poc_edit.html", context={"poc": poc, "products": products, "vuls": vuls})
    else:
        poc_id = request.POST.get("poc_id")
        poc_name = request.POST.get("poc_name")
        keywords = request.POST.get("keywords")
        description = request.POST.get("description")
        product = request.POST.get("product")
        vul = request.POST.get("vul")
        date = request.POST.get("date")
        code = request.POST.get("code")
        if poc_id == "" or poc_name == "" or keywords == "" or deletelog == "" or product == "" or vul == "" or date == "" \
                or description == "" or code == "":
            return JsonResponse({"status": "failure", "info": "params is error"})
        poc = PoC.objects.get(poc_id=poc_id)
        product = Product.objects.get(product_id=int(product))
        vul = Vul.objects.get(vul_id=int(vul))
        poc.poc_name = poc_name
        poc.poc_key = keywords
        poc.poc_desc = description
        poc.poc_product = product
        poc.poc_type = vul
        poc.poc_date = date
        poc.poc_code = code
        poc.save()
        return JsonResponse(data={"status": "success", "info": "PoC update successfully"})


@login_required(login_url='/admin/login/')
def poc_detail(request):
    from dashboard.models import PoC
    from esapi.Elasticsearch_vul import ElastciSearch
    from urllib import parse
    poc_id = request.GET.get("poc_id")
    if poc_id == "":
        return render(request, "dashboard/html/poc_detail.html", context={"poc": "", "res": ""})
    try:
        poc = PoC.objects.get(poc_id=poc_id)
        # 获取PoC的执行结果
        res = ElastciSearch().search(poc_id)
        hits = []
        locations = []
        for data in res:
            value = {}
            location = {}
            value["date"] = data["_source"]["DATE"]
            value["IP"] = parse.urlparse(data["_source"]["HOST"]).hostname
            value["PORT"] = parse.urlparse(data["_source"]["HOST"]).port
            print(data["_source"]["CITY"])
            location["city"] = data["_source"]["CITY"]
            location["LOGITUDE"] = data["_source"]["LOCATION"]["LOGITUDE"]
            location["LATITUDE"] = data["_source"]["LOCATION"]["LATITUDE"]
            locations.append(location)
            hits.append(value)
        return render(request, "dashboard/html/poc_detail.html", context={"poc": poc, "hits": hits, "locations": locations})
    except Exception as e:
        return render(request, "dashboard/html/poc_detail.html", context={"poc": "", "res": ""})


@login_required(login_url='/admin/login/')
def poc_delete(request):
    from dashboard.models import PoC
    poc_id = request.GET.get("poc_id")
    if poc_id == "":
        return JsonResponse({"status": "failure", "info": "params is error"})
    try:
        PoC.objects.filter(poc_id=poc_id).delete()
        return JsonResponse({"status": "success", "info": "PoC delete successfully"})
    except Exception as e:
        return JsonResponse({"status": "failure", "info": "PoC update failure"})


@login_required(login_url='/admin/login/')
def poc_run(request):
    from dashboard.models import PoC
    poc_id = request.GET.get("poc_id")
    if poc_id == "":
        return JsonResponse({"status": "failure", "info": "params is error"})
    try:
        poc = PoC.objects.get(poc_id=poc_id)
        res = poc.run()
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({"status": "failure", "info": "PoC run failure"})


@login_required(login_url='/admin/login/')
def add_vul_type(request):
    from dashboard.models import Vul
    if request.method == "GET":
        return render(request, "dashboard/html/vul_type_add.html")
    else:
        typename = request.POST.get("typename")
        if  typename == "":
            return JsonResponse({"status": "failure", "info": "params is error"})
        vul = Vul()
        vul.vul_name = typename
        vul.save()
        return JsonResponse(data={"status": "success", "info": "Type added successfully"})


@login_required(login_url='/admin/login/')
def product(request):
    return render(request, "dashboard/html/product_add.html")


@login_required(login_url='/admin/login/')
def add_product(request):
    product_name = request.POST.get("productname")
    prduct_url = request.POST.get("url")
    product_desc = request.POST.get("description")
    if product_name == "" or prduct_url == "" or product_desc == "":
        return JsonResponse({"status": "failure", "info": "params is error"})
    from dashboard.models import Product
    product = Product()
    product.procudt_name = product_name
    product.procudt_url = prduct_url
    product.product_desc = product_desc
    product.save()
    return JsonResponse(data={"status": "success", "info": "Product added successfully"})


@login_required(login_url='/admin/login/')
def product_update(request):
    product_id = request.POST.get("product_id")
    product_name = request.POST.get("productname")
    prduct_url = request.POST.get("url")
    product_desc = request.POST.get("description")
    if product_id == "" or product_name == "" or prduct_url == "" or product_desc == "":
        return JsonResponse({"status": "failure", "info": "params is error"})
    from dashboard.models import Product
    product = Product.objects.get(product_id=product_id)
    product.procudt_name = product_name
    product.procudt_url = prduct_url
    product.product_desc = product_desc
    product.save()
    return JsonResponse(data={"status": "success", "info": "Product update successfully"})


@login_required(login_url='/admin/login/')
def product_edit(request):
    product_id = request.GET.get("product_id")
    if product_id == "":
        return render(request, "dashboard/html/product_edit.html", context={"products": ""})
    from dashboard.models import Product
    try:
        product = Product.objects.get(product_id=product_id)
    except Exception as e:
        return render(request, "dashboard/html/product_edit.html", context={"products": ""})

    return render(request, "dashboard/html/product_edit.html", context={"products": product})


@login_required(login_url='/admin/login/')
def product_list(request):
    from dashboard.models import Product
    products = Product.objects.all()
    return render(request, "dashboard/html/product_list.html", context={"products": products})


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


def create_request(url, params):
    """
    做对scanner zmap  namp  vul 的请求处理
    :return:{}
    """
    import requests
    data = ""
    for param in params:
        data += (param + "&")
    print(data)

