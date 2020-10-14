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
    work_name=request.GET.get('work_name')
    type = request.GET.get('type')
    record_name = request.GET.get('record_name')

    # 判断当前是否有任务在进行
    status = models.Data.objects.filter(category_id=type)
    if (status[0].status == 0):
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
        cate_id=cate_id[0].id

    # return HttpResponse(cate_id)
    if (int(type) == 2):
        reture = lagou_action(0, work_name, cate_id, record_id)
        return HttpResponse(reture)

# 爬取lagou
def lagou_action(i,work_name,cate_id,record_id):
    try:
        # 去掉全局安全校验
        ssl._create_default_https_context = ssl._create_unverified_context
        # 先爬取首页python职位的网站以获取Cookie
        url = 'https://www.lagou.com/jobs/list_%E6%9E%B6%E6%9E%84%E5%B8%88?city=%E5%B9%BF%E5%B7%9E&labelWords=&fromSearch=true&suginput='
        # print(url)
        req = request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        })
        response = request.urlopen(req)
        # print(response)
        # 从响应头中提取Cookie
        cookie = ''
        for header in response.getheaders():
            if header[0] == 'Set-Cookie':
                cookie = cookie + header[1].split(';')[0] + '; '
        # 去掉最后的空格
        cookie = cookie[:-1]
        # print(cookie)
        # 爬取职位数据
        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        # 构造请求头，将上面提取到的Cookie添加进去
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Cookie': cookie,
            'Referer': 'https://www.lagou.com/jobs/list_%E6%9E%B6%E6%9E%84%E5%B8%88?city=%E5%B9%BF%E5%B7%9E&labelWords=&fromSearch=true&suginput='
        }
        kd = work_name;
        data = {
            'first': 'true',
            'pn': i,
            'kd': kd
        }

        req = request.Request(url, data=parse.urlencode(data).encode('utf-8'), headers=headers, method='POST')

        response = request.urlopen(req)

        result = response.read().decode('utf-8')
        result = json.loads(result)
    except IOError:
        models.Data.objects.filter(category_id=2).update(status=1)
        return 0



    if (result['content']['positionResult']['resultSize'] == 0):
        models.Data.objects.filter(category_id=2).update(status=1)
        return 1

    # 岗位
    try:
        # print(result)
        for x in range(0, result['content']['positionResult']['resultSize']):
            district = result['content']['positionResult']['result'][x]['city']
            work = result['content']['positionResult']['result'][x]['positionName']
            edu = result['content']['positionResult']['result'][x]['education']
            year = result['content']['positionResult']['result'][x]['workYear']
            money = result['content']['positionResult']['result'][x]['salary']
            company = result['content']['positionResult']['result'][x]['companyFullName']
            create_time = result['content']['positionResult']['result'][x]['createTime']
            data = [work, edu, money, company];

            if district == "广州" or district == "深圳":
                try:
                    salary_money=money.split('-')[1].replace('k', '')
                except BaseException:
                    salary_money = 0
                # 写入数据库
                lagou_data = models.Lagou(work=work, create_time=int(time.time()), edu=edu, compensation=money
                , record_id=record_id, work_type_id=cate_id, company=company, year=year,district=district,salary=salary_money)
                lagou_data.save()
            print(data)
    except IOError:
        models.Data.objects.filter(category_id=2).update(status=1)
        return 0

    sys.stdout.flush()
    time.sleep(random.randint(15, 40))
    return lagou_action(i+1, work_name, cate_id, record_id)