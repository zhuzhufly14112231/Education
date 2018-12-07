#!/usr/bin/env python
# encoding: utf-8
'''
@file: forms.py
@time: 2018/11/21 16:16
'''
from django import forms
from django.forms.models import inlineformset_factory
from courses.models import Course,Module

# inlineformset_factory() 内联表单工厂函数,是在普通表单集之上的一个抽象
# 这个函数允许我们动态的通过与Course模型关联的module模型创建表单集
# fields表示表单集中的每个表单的字段
# extra 设置每次表单集的表单数量
# can-delete 为每个表单内包含一个bool字段,用户可以选中需要删除的表单
ModuleFormSet = inlineformset_factory(Course,Module,
                                      fields=['title','description'],
                                      extra=2,
                                      can_delete=True)











 