from django.http import HttpResponse
from django.shortcuts import render

from polls import models


def recruit_record(request,type_id):

    record_index=models.Record.objects.filter(recruit_type=type_id).order_by('-id')
    if(type_id==1):
        type_name="猎聘网爬取记录"
    elif(type_id==2):
        type_name = "拉钩网爬取记录"
    elif(type_id==3):
        type_name = "前程无忧网爬取记录"

    # 把查询到的对象，封装到上下文
    context = {
        'allarticle': record_index,
        'type_name':type_name,
        'type_id':type_id
    }
    # 把上传文传到模板页面index.html里
    return render(request, 'recruit_record.html', context)


def recruit_index(request,type_id,id):
    if(type_id==1):
        recruit_index=models.Liepin.objects.filter(record_id=id)
        type_name = "猎聘网爬取数据"
    elif(type_id==2):
        recruit_index = models.Lagou.objects.filter(record_id=id)
        type_name = "拉钩网爬取数据"
    elif(type_id==3):
        recruit_index = models.Qiancheng.objects.filter(record_id=id)
        type_name = "前程无忧网爬取数据"

    context = {
        'allcontent': recruit_index,
        'type_name':type_name
    }
    # 把上传文传到模板页面index.html里
    return render(request, 'recruit_index.html', context)