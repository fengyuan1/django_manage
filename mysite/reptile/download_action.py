from django.http import HttpResponse
from django.shortcuts import render
import csv
import time
import xlwt
from polls import models

def download_action(request,type_id,record_id):
    return action(record_id,type_id)



def action(record_id,type_id):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    # 1.创建 Workbook
    wb = xlwt.Workbook(encoding = 'utf8')

    # 2.创建 worksheet
    ws = wb.add_sheet('test_sheet')

    # writer = csv.writer(response)
    # writer.writerow(['岗位信息', '教育背景', '薪资','公司名称','工作年限','职位类型','地区'])

    ws.write(0, 0, '岗位信息')
    ws.write(0, 1, '教育背景')
    ws.write(0, 2, '薪资')
    ws.write(0, 3, '公司名称')
    ws.write(0, 4, '工作年限')
    ws.write(0, 5, '职位类型')
    ws.write(0, 6, '地区')


    if(int(type_id)==1):
        data=models.Liepin.objects.filter(record_id=record_id)
        response['Content-Disposition'] = 'attachment; filename="liepin_"' + time.strftime("%Y-%m-%d",time.localtime()) + '".xls"'
    elif(int(type_id)==2):
        data=models.Lagou.objects.filter(record_id=record_id)
        response['Content-Disposition'] = 'attachment; filename="lagou_"' + time.strftime("%Y-%m-%d",time.localtime()) + '".xls"'
    else:
        data=models.Qiancheng.objects.filter(record_id=record_id)
        response['Content-Disposition'] = 'attachment; filename="qiancheng_"' + time.strftime("%Y-%m-%d",time.localtime()) + '".xls"'

    # print(data[0].work_type)
    for x in range(len(data)):
        ws.write(x + 1, 0, data[x].work)
        ws.write(x + 1, 1, data[x].edu)
        ws.write(x + 1, 2, data[x].compensation)
        ws.write(x + 1, 3, data[x].company)
        ws.write(x + 1, 4, data[x].year)
        ws.write(x + 1, 5, str(data[x].work_type))
        ws.write(x + 1, 6, data[x].district)
    wb.save(response)
    return response
