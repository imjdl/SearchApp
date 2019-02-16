from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import netifaces
from .models import Job
from datetime import datetime
import uuid
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
    return JsonResponse({"msg": 1, "data":data})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
