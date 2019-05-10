from django.db import models

# Create your models here.
import requests
import json
import base64


# 扫描器
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
            url = self.get_url() + "/celery-start/?token=" + self.scanner_token
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
            url = self.get_url() + "/celery-restart/?token=" + self.scanner_token
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
            url = self.get_url() + "/celery-stop/?token=" \
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
        url = self.get_url() + "/celery-status/?token=" + self.scanner_token
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

    def uninstall(self):
        data = {}
        url = self.get_url() + "/delete/?token=" + self.scanner_token
        try:
            req = requests.get(url=url, timeout=(10, 15))
            data = json.loads(req.text)
            if data["info"] == "Celery already runing":
                self.scanner_status = 1
            if data["info"] == "Celery has stopped":
                self.scanner_status = 0
        except Exception as e:
            self.scanner_status = 2
            data["info"] = "scanner unable to connect"
        return data

    def get_url(self):
        return "http://" + self.scanner_ip + ":" + str(self.scanner_port)

    def get_tasks(self):
        data = {}
        url = self.get_url() + "/tasks/?token=" + self.scanner_token
        try:
            req = requests.get(url=url, timeout=(10, 15))
            data = req.json()
            # for name in data["info"]:
            #     name["name"]
        except Exception as e:
            self.scanner_status = 2
            data["status"] = "failure"
            data["info"] = []
        return data

    def get_task_detail(self, id):
        data = {}
        url = self.get_url() + "/get_task_detail/?token=" + self.scanner_token + "&task_id=" + str(id)
        try:
            req = requests.get(url=url, timeout=(10, 15))
            data = req.json()
        except Exception as e:
            self.scanner_status = 2
            data["status"] = "failure"
            data["info"] = []
        return data


class Product(models.Model):
    # product id
    product_id = models.IntegerField(primary_key=True)
    # product name
    procudt_name = models.CharField(max_length=64)
    # product url
    procudt_url = models.CharField(max_length=64)
    # product desc
    product_desc = models.TextField()
    # create date
    product_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.procudt_name


class Vul(models.Model):

    # Vul ID
    vul_id = models.IntegerField(primary_key=True)
    # Vul name
    vul_name = models.CharField(max_length=64)

    def __str__(self):
        return self.vul_name


class PoC(models.Model):
    # Poc ID
    poc_id = models.IntegerField(primary_key=True)

    # PoC Name
    poc_name = models.CharField(max_length=64)

    # PoC Search Keywords
    poc_key = models.CharField(max_length=64)

    # PoC Description
    poc_desc = models.TextField()

    # Product
    poc_product = models.ForeignKey(to=Product, on_delete=models.CASCADE, default="")

    # Vul date
    poc_date = models.DateField()

    # Vul Type
    poc_type = models.ForeignKey(to=Vul, on_delete=models.CASCADE, default="")
    # PoC Code
    poc_code = models.TextField()

    def __str__(self):
        return self.poc_name

    def run(self):
        import random,  requests, json
        # 更新所有节点状态
        for sc in Scanner.objects.all():
            sc.get_state()
            sc.save()
        scanners = Scanner.objects.filter(scanner_status=1)
        if len(scanners) == 0:
            return {"status": "failure", "info": "No scan nodes available"}
        # 随机选取节点
        random.shuffle(scanners)
        scaner = scanners[0]
        url = scaner.get_url() + "/create_vul/"
        # 构造数据
        code = {}
        code["poc_name"] = self.poc_name
        code["poc_code"] = self.poc_code
        code["search_syntax"] = self.poc_key
        code["poc_id"] = self.poc_id
        data = "token=" + scaner.scanner_token + "&code=" + json.dumps(code)
        # post 请求
        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }
        try:
            res = requests.post(url=url, data=data, headers=headers, timeout=(10, 15))
            return json.loads(res.text)
        except Exception as e:
            return {"status": "failure", "info": "task create failure "}

