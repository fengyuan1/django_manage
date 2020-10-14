from django.http import HttpResponse
from django.shortcuts import render

from polls import models

def grad_index(request,type_id):
    if(type_id==1):
        type_name = "猎聘网"
    elif(type_id==2):
        type_name = "拉勾网"
    elif (type_id == 3):
        type_name = "前程无忧网"

    #查询状态
    status = models.Data.objects.filter(category_id=type_id)

    if(status[0].status==1):
        status_msg="未有任务在进行"
    else:
        status_msg="有任务在进行中"


    # 把查询到的对象，封装到上下文
    context = {
        'type_name': type_name,
        'type_id': type_id,
        'status_msg':status_msg
    }
    # 把上传文传到模板页面index.html里

    return render(request, 'grad_index.html', context)
