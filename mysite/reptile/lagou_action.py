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
    cookie=request.GET.get('cookie')
    # 判断当前是否有任务在进行
    status = models.Data.objects.filter(category_id=type)
    if (status[0].status == 0):
        return HttpResponse(-1)
    models.Data.objects.filter(category_id=type).update(status=0)

    if(cookie==''):
        return HttpResponse(-3)

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
        reture = lagou_action(0, work_name, cate_id, record_id,cookie)
        return HttpResponse(reture)

# 爬取lagou
def lagou_action(i,work_name,cate_id,record_id,cookie):
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
        # cookie = ''

        # 去掉最后的空格
        # coo
        # kie = 'user_trace_token=20200827151121-d8e0e75c-8d8e-4ce4-a7cc-553946b50295; _ga=GA1.2.61474767.1598512282; LGUID=20200827151123-d683b99e-6534-4924-ab76-358648a78a90; RECOMMEND_TIP=true; index_location_city=%E5%B9%BF%E5%B7%9E; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1609817343,1609817423,1609923485,1610420074; JSESSIONID=ABAAABAABAGABFA946C8EBA359E5611624482A4C89B221C; WEBTJ-ID=20210112105437-176f484457a137-0b873ffb03133d-31346d-1327104-176f484457bff; sensorsdata2015session=%7B%7D; _gid=GA1.2.74952155.1610420078; gate_login_token=13fd736d24f10d1f12537134478eb4b2c87a0eb86319094c5c4ecf1c2bd6b7a4; _putrc=1BDD24CCDD69F9DA123F89F2B170EADC; login=true; unick=%E5%86%AF%E5%85%83; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=14; privacyPolicyPopup=false; TG-TRACK-CODE=jobs_code; SEARCH_ID=376271b1aee54ea99d2a638bb7f66507; X_HTTP_TOKEN=bf8092b4e02c19c138345401616bf6892f44bf4113; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20210112202623-cb07d94c-6644-4c23-8b91-21b88b00d13e; PRE_SITE=https%3A%2F%2Fwww.lagou.com; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211463512%22%2C%22%24device_id%22%3A%221742ec1f697aa4-050b514b85b73-e343166-2073600-1742ec1f69ab19%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2287.0.4280.141%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22first_id%22%3A%221742ec1f697aa4-050b514b85b73-e343166-2073600-1742ec1f69ab19%22%7D; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1610454383; LGRID=20210112202623-0c6b9b6a-79c9-4b60-a706-19198d5c71bf'
        # print(cookie)
        # 爬取职位数据
        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        # 构造请求头，将上面提取到的Cookie添加进去
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Cookie': cookie,
            'Referer': 'https://www.lagou.com/jobs/list_%E6%9E%B6%E6%9E%84%E5%B8%88?city=%E5%B9%BF%E5%B7%9E&labelWords=&fromSearch=true&suginput='
        }
        kd = work_name
        data = {
            'first': 'true',
            'pn': i,
            'kd': kd
        }

        req = request.Request(url, data=parse.urlencode(data).encode('utf-8'), headers=headers, method='POST')

        response = request.urlopen(req)
        print(response)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        print(result)
    except BaseException:
        models.Data.objects.filter(category_id=2).update(status=1)
        return 0

    try:
        if (result['content']['positionResult']['resultSize'] == 0):
            models.Data.objects.filter(category_id=2).update(status=1)
            return 1
    except BaseException:
        models.Data.objects.filter(category_id=2).update(status=1)
        return 0
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
    time.sleep(random.randint(60, 90))
    return lagou_action(i+1, work_name, cate_id, record_id,cookie)