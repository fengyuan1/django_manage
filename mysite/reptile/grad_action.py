from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import csv
import time
import random
import requests
import sys
import operator
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
    record=Record(record_name=record_name,date=str(int(time.time())),recruit_type=type)
    record.save()
    record_id=record.id

    # 查找职位表是否有这个职位，没有的话就添加
    cate_id=models.Category.objects.filter(name=work_name)


    if(not(cate_id)):
        cate=models.Category(name=work_name,add_time=int(time.time()))
        cate.save()
        cate_id=cate.id
    else:
        cate_id=cate_id[0].id
    # return HttpResponse(1)
    if(int(type)==1):
        reture=liepin_action(0,0,work_name,cate_id,record_id)
        return HttpResponse(reture)



# 爬取liepin
def liepin_action(i,sleep_count,work_name,cate_id,record_id):
    # 岗位
    work_name = work_name
    link = "https://www.liepin.com/zhaopin/?industries=040&subIndustry=&dqs=050020&salary=&jobKind=&pubTime=&compkind=&compscale=&searchType=1&isAnalysis=&sortFlag=15&d_headId=aaa42964a7680110daf82f6e378267d9&d_ckId=ff5c36a41d1d524cff2692be11bbe61f&d_sfrom=search_prime&d_pageSize=40&siTag=_1WzlG2kKhjWAm3Yf9qrog%7EqdZCMSZU_dxu38HB-h7GFA&key=" + quote(
        work_name) + "&curPage=" + str(i)
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    ]
    headers = {"User-Agent": random.choice(user_agent_list)}

    try:
        response = requests.get(link, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        sojob_result = soup.find("div", class_='sojob-result')
        list_r = sojob_result.find_all("li")
    except BaseException:
        if (sleep_count > 9):
            print("亲，我都试了45分钟了，还是无法请求网络成功，请你稍后重试或寻求专业人士帮助")
            print("亲，抱歉，程序结束")
            models.Data.objects.filter(category_id=1).update(status=1)
            return 0
        print("抱歉，爬取异常，原因可能是需要验证操作或您的网络不佳，我先休息五分钟再来试试把")
        print("开始休眠5分钟")
        sleep_count = sleep_count + 1
        sys.stdout.flush()
        time.sleep(300)
        return liepin_action(i, sleep_count,work_name,cate_id,record_id)

    if (len(list_r) == 0):
        print("恭喜你,本次爬取数据任务已完成啦")
        models.Data.objects.filter(category_id=1).update(status=1)
        return 1
    # 岗位
    sleep_count = 0
    in_data = []
    out_data = []

    for x in range(0, len(list_r)):
        address = ''
        work = list_r[x].find("a").get_text().strip()
        edu = list_r[x].find("span", class_='edu').get_text().strip()
        year = list_r[x].find("span", class_='edu').find_next_sibling("span").get_text().strip()
        money = list_r[x].find("span", class_='text-warning').get_text().strip()
        company = list_r[x].find("p", class_='company-name').get_text().strip()
        data = {'work': work, 'edu':edu, 'compensation':money, 'company':company, 'year':year, 'district':address}

        work_data = models.Data.objects.filter(category_id=1)
        in_data = data
        out_data = work_data[0].work_name

        in_data = str(in_data)
        if (operator.eq(in_data, out_data)):

            count = work_data[0].count
            count = int(count)

            if (count > 12):
                print("恭喜你,本次爬取数据任务已完成啦")
                models.Data.objects.filter(category_id=1).update(status=1)
                return 1

        if (money != '面议'):
            try:
                salary = money.split('-')[1][-5:]
                salary_money = money.split('-')[1].replace(salary, '')
            except BaseException:
                salary_money = 0
        else:
            salary_money = 0
        # 写入数据库
        liepin_data = models.Liepin(work=work, create_time=int(time.time()),edu=edu,compensation=money
        ,record_id=record_id,work_type_id=cate_id,company=company,year=year,district=address,salary=salary_money)
        liepin_data.save()

        print(data)

    models.Data.objects.filter(category_id=1).update(work_name=str(in_data))
    models.Data.objects.filter(category_id=1).update(count=str(i))

    sys.stdout.flush()
    time.sleep(random.randint(7, 16))
    return liepin_action(i + 1, sleep_count,work_name,cate_id,record_id)



