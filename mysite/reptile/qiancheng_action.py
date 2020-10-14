from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import csv
import time
import random
import requests
import sys
import operator
import ssl
import json
import random
from urllib import parse
from urllib import request
from polls import models
from urllib.parse import quote
from polls.models import Record

def grad_action(request):
    work_name = request.GET.get('work_name')
    type = request.GET.get('type')
    record_name = request.GET.get('record_name')

   # 判断当前是否有任务在进行
    status=models.Data.objects.filter(category_id=type)
    if(status[0].status==0):
        return HttpResponse(-1)
    models.Data.objects.filter(category_id=type).update(status=0)

    # 插入查找岗位信息记录
    record = Record(record_name=record_name, date=str(int(time.time())), recruit_type=type)
    record.save()
    record_id = record.id

    # 查找职位表是否有这个职位，没有的话就添加
    cate_id = models.Category.objects.filter(name=work_name)

    if (not (cate_id)):
        cate = models.Category(name=work_name, add_time=int(time.time()))
        cate.save()
        cate_id = cate.id
    else:
        cate_id = cate_id[0].id


    if (int(type) == 3):
        # 更新该类目的爬取状态
        reture = qiancheng_action(1,0, work_name, cate_id, record_id)
        return HttpResponse(reture)

# 爬取lagou
def qiancheng_action(i,sleep_count,work_name,cate_id,record_id):
    # 去掉全局安全校验
    # 岗位
    work_name = work_name
    try:
        link = "https://search.51job.com/list/030200,000000,0000,00,9,99," + quote(work_name) + ",2," + str(i) + ".html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        response = requests.get(link, headers=headers)
        code = response.apparent_encoding
        response.encoding = code
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        in_data = []
        out_data = []
        count = 0

        sojob_result = soup.find_all("script", type='text/javascript')

    except BaseException:
        if (sleep_count > 9):
            print("亲，我都试了45分钟了，还是无法请求网络成功，请你稍后重试或寻求专业人士帮助")
            print("亲，抱歉，程序结束")
            models.Data.objects.filter(category_id=3).update(status=1)
            return 0
        print("抱歉，爬取异常，原因可能是需要验证操作或您的网络不佳，我先休息五分钟再来试试把")
        print("开始休眠5分钟")
        sleep_count = sleep_count + 1
        sys.stdout.flush()
        time.sleep(300)
        return qiancheng_action(i, sleep_count,work_name,cate_id,record_id)

    try:
        a = str(sojob_result[2])

        json_str = json.loads(a[60:-9], strict=False)

        list = json_str['engine_search_result']
    except BaseException:
        sys.stdout.flush()
        time.sleep(3)
        return qiancheng_action(i+1, sleep_count, work_name, cate_id, record_id)

    if (len(list) == 0):
        print("恭喜你,本次爬取数据任务已完成啦")
        models.Data.objects.filter(category_id=3).update(status=1)
        return 1
    try:
        for x in range(1, len(list)):
            work = list[x]['job_name']
            company = list[x]['company_name']
            address = list[x]['workarea_text']
            money = list[x]['providesalary_text']
            attribute_text = list[x]['attribute_text']
            public_time = list[x]['issuedate']
            data = [work, company, address, money, attribute_text, public_time]
            year=attribute_text[1]
            print(data)
            if("经验" in year):
                year=attribute_text[1]
            else:
                year='不限'

            if(money!=''):
                try:
                    salary=money.split('-')[1][-3:]
                    if(salary=='万/月'):
                        salary_money=money.split('-')[1].replace('万/月','')
                    elif(salary=='万/年'):
                        salary_money = money.split('-')[1].replace('万/年', '')
                    else:
                        salary_money = money.split('-')[1].replace('千/月', '')
                except BaseException:
                    salary_money = 0
            else:
                salary_money=0

            qiancheng = models.Qiancheng(work=work, create_time=int(time.time()), edu=str(attribute_text), compensation=money
            , record_id=record_id, work_type_id=cate_id, company=company, year=year,district=address,salary=salary_money)
            qiancheng.save()

            in_data = data

            work_data = models.Data.objects.filter(category_id=3)
            out_data = work_data[0].work_name

            in_data = str(in_data)
            if (operator.eq(in_data, out_data)):
                    count = work_data[0].count
                    count = int(count)

    except BaseException:
        sys.stdout.flush()
        time.sleep(random.randint(3, 7))
        qiancheng_action(i + 1, sleep_count, work_name, cate_id, record_id)

    sys.stdout.flush()
    time.sleep(random.randint(3, 7))
    if (count > 12):
        print("恭喜你,本次爬取数据任务已完成啦")
        models.Data.objects.filter(category_id=3).update(status=1)
        return 1
    sleep_count = 0

    models.Data.objects.filter(category_id=3).update(work_name=str(in_data))
    models.Data.objects.filter(category_id=3).update(count=str(i))

    return qiancheng_action(i + 1, sleep_count, work_name, cate_id, record_id)