from django.db import models

# Create your models here.
import requests
import json

class Scanner(models.Model):

    # scanner id
    scanner_id = models.IntegerField(primary_key=True)
    # scanner token
    scanner_token = models.CharField(max_length=24)
    # scanner ip
    scanner_ip = models.GenericIPAddressField(protocol="ipv4")
    # scanner port
    scanner_port = models.IntegerField()
    # create scanner date
    scanner_date = models.DateTimeField(auto_now=True)
    # scanner status 0: shutdown  1: runing 2: not install yet
    status_level = (
        (0, "shutdown"),
        (1, "runing"),
        (2, "unable to connect")
    )
    scanner_status = models.IntegerField(choices=status_level)

    # es server config
    scanner_es_hosts = models.TextField()
    scanner_es_port = models.IntegerField()
    scanner_es_user = models.CharField(max_length=10)
    scanner_es_pass = models.CharField(max_length=64)

    server_type = (
        ("redis", "redis"),
        ("amqp", "amqp")
    )
    # borker server config
    scanner_borker_type = models.CharField(choices=server_type, max_length=5)
    scanner_borker_user = models.CharField(max_length=10)
    scanner_borker_pass = models.CharField(max_length=64)
    scanner_borker_host = models.GenericIPAddressField(protocol="ipv4")
    scanner_borker_port = models.IntegerField()
    scanner_borker_db = models.CharField(max_length=10)

    # backend server config
    scanner_backend_type = models.CharField(choices=server_type, max_length=5)
    scanner_backend_user = models.CharField(max_length=10)
    scanner_backend_pass = models.CharField(max_length=64)
    scanner_backend_host = models.GenericIPAddressField(protocol="ipv4")
    scanner_backend_port = models.IntegerField()
    scanner_backend_db = models.CharField(max_length=10)

    def __str__(self):
        return self.scanner_ip + ":::" + str(self.scanner_port)

    # (0, "shutdown"),
    # (1, "runing"),
    # (2, "unable to connect")
    def start(self):
        # start celery server
        data = {}
        if self.scanner_status == 1:
            data["info"] = "scanner is running"
        elif self.scanner_status == 2:
            data["info"] = "scanner unable to connect"
        else:
            url = "http://" + self.scanner_ip + ":" + str(self.scanner_port) + "/celery-start/?token=" \
                  + self.scanner_token
            try:
                req = requests.get(url=url, timeout=(10, 15))
                data["info"] = json.loads(req.text)["info"]
                self.scanner_status = 1
            except Exception as e:
                self.scanner_status = 2
                data["info"] = "scanner unable to connect"
        return data

    def restart(self):
        data = {}
        if self.scanner_status == 2:
            data["info"] = "scanner unable to connect"
        else:
            url = "http://" + self.scanner_ip + ":" + str(self.scanner_port) + "/celery-restart/?token=" \
                  + self.scanner_token
            try:
                req = requests.get(url=url, timeout=(10, 15))
                data["info"] = json.loads(req.text)["info"]
            except Exception as e:
                self.scanner_status = 2
                data["info"] = "scanner unable to connect"
        return data

    def stop(self):
        data = {}
        if self.scanner_status == 3:
            data["info"] = "scanner is stop"
        elif self.scanner_status == 2:
            data["info"] = "scanner unable to connect"
        else:
            url = "http://" + self.scanner_ip + ":" + str(self.scanner_port) + "/celery-stop/?token=" \
                  + self.scanner_token
            try:
                req = requests.get(url=url, timeout=(10, 15))
                data["info"] = json.loads(req.text)["info"]
                self.scanner_status = 0
            except Exception as e:
                self.scanner_status = 2
                data["info"] = "scanner unable to connect"
        return data

    def get_state(self):
        data = {}
        url = "http://" + self.scanner_ip + ":" + str(self.scanner_port) + "/celery-status/?token=" \
              + self.scanner_token
        try:
            req = requests.get(url=url, timeout=(10, 15))
            data["info"] = json.loads(req.text)["info"]
            if data["info"] == "Celery already runing":
                self.scanner_status = 1
            if data["info"] == "Celery has stopped":
                self.scanner_status = 0
        except Exception as e:
            self.scanner_status = 2
            data["info"] = "scanner unable to connect"
        return data


class Job(models.Model):
    # 任务 id
    uuid = models.CharField(max_length=36)
    # 任务标题
    title = models.CharField(max_length=40)
    # 任务描述
    desc = models.TextField(max_length=200)
    # 目标端口
    dst_port = models.IntegerField()
    # 本地端口
    src_port = models.IntegerField()
    # ip范围(B段或C段)
    subnets = models.CharField(max_length=20)
    # 选择网卡
    network_card = models.CharField(max_length=40)
    # 任务状态 0准备中  1运行中  2运行完成 3超时
    status = models.IntegerField()
    # 执行进度
    progress_rate = models.IntegerField()
    # 创建时间
    start_time = models.DateTimeField()
    # 结束时间
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "[ " + self.title + " ]"
