from django.http import HttpResponse
import matplotlib
import time
from polls import models
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from io import BytesIO
import base64
from django.shortcuts import render
matplotlib.use('Agg')

def mate_action(request,type_id,record_id):
    # type = request.GET.get('type')
    # record_id = request.GET.get('record_id')

    if(int(type_id)==1):
        data=liepin_action(int(record_id))
    elif(int(type_id)==2):
        data=lagou_action(int(record_id))
    elif(int(type_id)==3):
        data=qiancheng(int(record_id))

    context={
        "images":data
    }

    return render(request, 'mate_index.html', context)

def liepin_action(record_id):
    analyse_dasa=[]
    year=models.Liepin.objects.values_list('year', flat=True).distinct().filter(record_id=record_id)
    for y in year:
        work_data=models.Liepin.objects.values_list('compensation', flat=True).filter(record_id=record_id,year=y).order_by('-salary')

        #
        deal_d=deal_data(list(work_data))
        print(deal_d)

        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False

        price = deal_d['union_count']
        plt.figure(figsize=(10, 10))
        plt.barh(range(len(price)), price, color='steelblue', alpha=1)  # 从下往上画
        plt.yticks(range(len(price)),deal_d['union'])
        plt.xlim(0, 30)


        # 显示横轴标签
        plt.xlabel("frequency")
        # 显示纵轴标签
        plt.ylabel("salary range")
        # 显示图标题
        plt.title(y+" years work experience Salary frequency distribution histogram")
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)  # 对plot_data进行编码
        ims = imb.decode()
        imd = "data:image/png;base64," + ims
        analyse_dasa.append(imd)
        plt.close()

    return analyse_dasa


def lagou_action(record_id):
    analyse_dasa = []
    year = models.Lagou.objects.values_list('year', flat=True).distinct().filter(record_id=record_id)
    print(year)
    # 进行排序开始
    for y in year:
        work_data = models.Lagou.objects.values_list('compensation', flat=True).filter(record_id=record_id, year=y).order_by('-salary')

        #
        deal_d = deal_data(list(work_data))
        print(deal_d)

        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False

        price = deal_d['union_count']
        plt.figure(figsize=(8, 10))
        plt.barh(range(len(price)), price, color='steelblue', alpha=1)  # 从下往上画
        plt.yticks(range(len(price)), deal_d['union'])
        plt.xlim(0, 35)

        # 显示横轴标签
        plt.xlabel("frequency")
        # 显示纵轴标签
        plt.ylabel("salary range")
        # 显示图标题
        plt.title(y + " years work experience Salary frequency distribution histogram")
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)  # 对plot_data进行编码
        ims = imb.decode()
        imd = "data:image/png;base64," + ims
        analyse_dasa.append(imd)
        plt.close()

    return analyse_dasa

def qiancheng(record_id):
    analyse_dasa = []
    year = models.Qiancheng.objects.values_list('year', flat=True).distinct().filter(record_id=record_id)
    for y in year:
        work_data = models.Qiancheng.objects.values_list('compensation', flat=True).filter(record_id=record_id, year=y).order_by('-salary')

        #
        deal_d = deal_data(list(work_data))
        print(deal_d)

        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False

        price = deal_d['union_count']
        plt.figure(figsize=(12, 10))
        plt.barh(range(len(price)), price, color='steelblue', alpha=1)  # 从下往上画
        plt.yticks(range(len(price)), deal_d['union'])
        plt.xlim(0, 60)

        # 显示横轴标签
        plt.xlabel("frequency")
        # 显示纵轴标签
        plt.ylabel("salary range")
        # 显示图标题
        plt.title(y + " years work experience Salary frequency distribution histogram")
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)  # 对plot_data进行编码
        ims = imb.decode()
        imd = "data:image/png;base64," + ims
        analyse_dasa.append(imd)
        plt.close()

    return analyse_dasa


def deal_data(work_data):
    union=list(set(work_data))
    union.sort(key=work_data.index)
    union_count=[]
    for x in union:
        union_count.append(work_data.count(x))

    return {"union":union,"union_count":union_count}