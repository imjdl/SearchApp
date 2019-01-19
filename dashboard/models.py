from django.db import models

# Create your models here.


class Job(models.Model):
    """
    一个任务
    """
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
