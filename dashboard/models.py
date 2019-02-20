from django.db import models

# Create your models here.


class Scanner(models.Model):

    # scanner token
    scanner_token = models.CharField(max_length=24, primary_key=True)
    # scanner ip
    scanner_ip = models.GenericIPAddressField(protocol="ipv4")
    # scanner port
    scanner_port = models.IntegerField()
    # create scanner date
    scanner_date = models.DateTimeField()
    # scanner status 0: shutdown  1: runing 2: not install yet
    status_level = (
        (0, "shutdown"),
        (1, "runing"),
        (2, "not install yet")
    )
    scanner_status = models.IntegerField(choices=status_level)

    # es server config
    scanner_es_host = models.GenericIPAddressField(protocol="ipv4")
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
        return self.scanner_token


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
