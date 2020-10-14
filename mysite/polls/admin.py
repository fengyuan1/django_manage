from django.contrib import admin

# Register your models here.
from django.contrib import admin
from polls.models import Test,Liepin,Lagou,Category,Qiancheng,Record
from django.core.paginator import Paginator

class LiepinAdmin(admin.ModelAdmin):
    list_display = ('work', 'edu', 'district','company','compensation','year','work_type','record')  # list
    search_fields = ('work',)
    # 分页，每页显示条数
    list_per_page = 10
    paginator = Paginator
class LagouAdmin(admin.ModelAdmin):
    list_display = ('work', 'edu', 'district', 'company', 'compensation','year','work_type','record')  # list
    search_fields = ('work',)
    # 分页，每页显示条数
    list_per_page = 10
    paginator = Paginator

class QianchengAdmin(admin.ModelAdmin):
    list_display = ('work', 'edu', 'district', 'company', 'compensation','year','work_type','record')  # list
    search_fields = ('work',)
    # 分页，每页显示条数
    list_per_page = 10
    paginator = Paginator

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','add_time')
    list_per_page=10
    paginator = Paginator

class RecordAdmin(admin.ModelAdmin):
    list_display=('date','recruit_type')
    list_per_page=10
    paginator = Paginator

admin.site.register(Liepin,LiepinAdmin)
admin.site.register(Lagou,LagouAdmin)
admin.site.register(Qiancheng,QianchengAdmin)
admin.site.register(Record,RecordAdmin)
admin.site.register(Category,CategoryAdmin)