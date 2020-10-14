from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import os

def index(request):
    sitename = 'Django中文网'
    url = 'www.django.cn'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 新加一个列表
    list = [
        '开发前的准备',
        '项目需求分析',
        '数据库设计分析',
        '创建项目',
        '基础配置',
        '欢迎页面',
        '创建数据库模型',
    ]
    context = {
        'static':BASE_DIR+"\static",
        'sitename': sitename,
        'url':url,
        'list':list, #把list封装到context
    }
    # return HttpResponse(context)
    return render(request,'index.html',context)