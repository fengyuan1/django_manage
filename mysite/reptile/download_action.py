from django.http import HttpResponse
from django.shortcuts import render
import csv
import time
from polls import models

def download_action(request,type_id,record_id):
    return action(record_id,type_id)



def action(record_id,type_id):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['岗位信息', '教育背景', '薪资','公司名称','工作年限','职位类型','地区'])

    if(int(type_id)==1):
        data=models.Liepin.objects.filter(record_id=record_id)
        response['Content-Disposition'] = 'attachment; filename="liepin_"' + time.strftime("%Y-%m-%d",time.localtime()) + '".csv"'
    elif(int(type_id)==2):
        data=models.Lagou.objects.filter(record_id=record_id)
        response['Content-Disposition'] = 'attachment; filename="lagou_"' + time.strftime("%Y-%m-%d",time.localtime()) + '".csv"'
    else:
        data=models.Qiancheng.objects.filter(record_id=record_id)
        response['Content-Disposition'] = 'attachment; filename="qiancheng_"' + time.strftime("%Y-%m-%d",time.localtime()) + '".csv"'

    for x in range(len(data)):
        writer.writerow([data[x].work, data[x].edu, data[x].compensation, data[x].company,data[x].year,data[x].work_type,data[x].district])
    return response
