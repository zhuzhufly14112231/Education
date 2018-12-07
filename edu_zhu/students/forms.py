#!/usr/bin/env python
# encoding: utf-8
'''
@file: forms.py
@time: 2018/11/22 15:58
'''

from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)

















 