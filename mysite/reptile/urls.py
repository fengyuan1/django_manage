"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views,recruit_view,grad_view,grad_action,lagou_action,qiancheng_action,download_action,mate_action

urlpatterns = [
    path("index/",views.index, name='index' ),
    path("recruit_view/<int:type_id>", recruit_view.recruit_record, name='index'),
    path("recruit_view/recruit_index/<int:type_id>/<int:id>", recruit_view.recruit_index, name='index'),
    path("download_action/<int:type_id>/<int:record_id>", download_action.download_action, name='index'),
    path("grad_view/<int:type_id>", grad_view.grad_index, name='index'),
    path("grad_action/", grad_action.grad_action, name='index'),
    path("lagou_action/", lagou_action.grad_action, name='index'),
    path("qiancheng_action/", qiancheng_action.grad_action, name='index'),
    path("mate_action/<int:type_id>/<int:record_id>", mate_action.mate_action, name='index'),

]
