# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone

# Create your models here.

class MonitorTemplate(models.Model):
    name =  models.CharField(max_length=20,unique=True,verbose_name='名称')
    items = models.ManyToManyField('MonitorItem',verbose_name='监控项')
    policy = models.ManyToManyField('MonitorNotifyPolicy',verbose_name='告警策略')
    interval = models.CharField(max_length=5,verbose_name='监控频率')
    cpu = models.CharField(max_length=64,null=True,blank=True,verbose_name='cpu')
    memory = models.CharField(max_length=64,null=True,blank=True,verbose_name='memory')
    disk = models.CharField(max_length=225,null=True,blank=True,verbose_name='disk')
    network = models.CharField(max_length=64,null=True,blank=True,verbose_name='network')
    
    def __unicode__(self):
        return '%s' %(self.name)

class MonitorItem(models.Model):
    name =  models.CharField(max_length=20,unique=True,verbose_name='名称')
    value = models.CharField(max_length=255,verbose_name='键值')
    def __unicode__(self):
        return '%s' %(self.name)
    
class MonitorHost(models.Model):
    name = models.CharField(max_length=64,unique=True,verbose_name='名称')
    address = models.CharField(max_length=32,unique=True,verbose_name='IP地址')
    port = models.CharField(max_length=32,unique=True,verbose_name='端口')
    template = models.ForeignKey('MonitorTemplate',on_delete=models.PROTECT,verbose_name='模版')
    status = models.CharField(max_length=15,default='enabled',verbose_name='状态')
    agent = models.CharField(max_length=5,default='down',verbose_name='Agent状态')
    
    def __unicode__(self):
        return '%s' %(self.name)

class MonitorProblem(models.Model):
    name = models.CharField(max_length=255,verbose_name='名称')
    time = models.DateTimeField(default = timezone.now,verbose_name='时间')
    address = models.CharField(max_length=32,verbose_name='主机')
    level = models.CharField(max_length=16,verbose_name='级别')
    status = models.CharField(max_length=16,default='unconfirmed',verbose_name='状态')
    
    def __unicode__(self):
        return '%s' %(self.name)
    
class MonitorNotifyDetail(models.Model):
    mode = models.CharField(max_length=10,verbose_name='通知方式')
    theme = models.CharField(max_length=32,verbose_name='主题')
    content = models.TextField(verbose_name="内容")
    send_to = models.CharField(max_length=64,verbose_name="接收人")
    status = models.CharField(max_length=10,default='send',verbose_name="发送状态")
    
    def __unicode__(self):
        return '%s' %(self.theme)
    
class MonitorNotifyPolicy(models.Model):
    name = models.CharField(max_length=255,verbose_name='名称')
    warning_threshold = models.CharField(max_length=255,verbose_name='warning阀值')
    danger_threshold = models.CharField(max_length=255,verbose_name='danger阀值')
    promote = models.CharField(max_length=255,verbose_name='告警升级/次')
    
    def __unicode__(self):
        return '%s' %(self.name)
        
