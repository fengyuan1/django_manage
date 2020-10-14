from django.db import models

# Create your models here.
# models.py
from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=20)


class Category(models.Model):
    # id = models.CharField(u'实例ID', max_length=32, blank=False, primary_key=True)
    name = models.CharField(u'岗位', max_length=50)
    add_time= models.CharField(u'添加时间', max_length=50)
    class Meta:
        verbose_name = '职位分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Record(models.Model):
    # id = models.CharField(u'实例ID', max_length=32, blank=False, primary_key=True)
    record_name=models.CharField(u'记录名称', max_length=50)
    date=models.CharField(u'记录日期', max_length=50)
    recruit_type=models.CharField(u'记录类型', max_length=50)
    class Meta:
        verbose_name = '爬取记录'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.date

class Liepin(models.Model):
    # id = models.CharField(u'实例ID', max_length=32, blank=False, primary_key=True)
    work=models.CharField(u'岗位',max_length=50)
    edu=models.CharField(u'教育背景',max_length=50)
    district=models.CharField(u'地区',max_length=50)
    compensation=models.CharField(u'薪酬',max_length=50)
    company=models.CharField(u'公司',max_length=50)
    year = models.CharField(u'工作年限', max_length=50)
    create_time = models.CharField(u'创建时间', max_length=50)
    work_type = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='分类')
    record = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name='记录')
    salary = models.CharField(u'收入后一位', max_length=10)

    class Meta:
        verbose_name = '猎聘数据'
        verbose_name_plural = verbose_name

class Qiancheng(models.Model):
    # id = models.CharField(u'实例ID', max_length=32, blank=False, primary_key=True)
    work = models.CharField(u'岗位', max_length=50)
    edu = models.CharField(u'教育背景', max_length=50)
    district = models.CharField(u'地区', max_length=50)
    compensation = models.CharField(u'薪酬', max_length=50)
    company = models.CharField(u'公司', max_length=50)
    year = models.CharField(u'工作年限', max_length=50)
    create_time = models.CharField(u'创建时间', max_length=50)
    work_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name='记录')
    salary = models.CharField(u'收入后一位', max_length=10)

    class Meta:
        verbose_name = '前程数据'
        verbose_name_plural = verbose_name


class Lagou(models.Model):
    # id = models.CharField(u'实例ID', max_length=32, blank=False, primary_key=True)
    work=models.CharField(u'岗位',max_length=50)
    edu=models.CharField(u'教育背景',max_length=50)
    district=models.CharField(u'地区',max_length=50)
    compensation=models.CharField(u'薪酬',max_length=50)
    company=models.CharField(u'公司',max_length=50)
    year = models.CharField(u'工作年限', max_length=50)
    create_time = models.CharField(u'创建时间', max_length=50)
    work_type=models.ForeignKey(Category,on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name='记录')
    salary= models.CharField(u'收入后一位', max_length=10)

    class Meta:
        verbose_name = '拉钩数据'
        verbose_name_plural = verbose_name


class Data(models.Model):
    id = models.CharField(u'实例ID', max_length=32, blank=False, primary_key=True)
    count = models.CharField(u'次数', max_length=50)
    work_name = models.CharField(u'工作名称', max_length=50)
    category_id = models.CharField(u'分类id', max_length=50)
    status = models.CharField(u'分类id', max_length=20)

    class Meta:
        verbose_name = '临时存储数据'
        verbose_name_plural = verbose_name


