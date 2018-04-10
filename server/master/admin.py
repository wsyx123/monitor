# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import MonitorTemplate,MonitorHost,MonitorNotifyDetail,\
MonitorProblem,MonitorNotifyPolicy,MonitorItem

    
class MonitorTemplateAdmin(admin.ModelAdmin):
    list_display = ('name','get_item','interval','cpu','memory','disk','network')  
    def get_item(self,MonitorItem):
        return "\n".join([p.name for p in MonitorItem.objects.all()])

class MonitorItemAdmin(admin.ModelAdmin):
    list_display = ('name','value')
    
class MonitorHostAdmin(admin.ModelAdmin):
    list_display = ('name','address','port','template','status','agent')  
    
class MonitorNotifyPolicyAdmin(admin.ModelAdmin):
    list_display = ('name','warning_threshold','danger_threshold','promote')
    
class MonitorProblemAdmin(admin.ModelAdmin):
    list_display = ('name','time','address','level','status')
    
class MonitorNotifyDetailAdmin(admin.ModelAdmin):
    list_display = ('mode','theme','content','send_to','status')


admin.site.register(MonitorTemplate,MonitorTemplateAdmin)
admin.site.register(MonitorHost,MonitorHostAdmin)
admin.site.register(MonitorNotifyPolicy,MonitorNotifyPolicyAdmin)
admin.site.register(MonitorProblem,MonitorProblemAdmin)
admin.site.register(MonitorNotifyDetail,MonitorNotifyDetailAdmin)
admin.site.register(MonitorItem,MonitorItemAdmin)
