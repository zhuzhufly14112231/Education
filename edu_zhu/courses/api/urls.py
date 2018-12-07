#!/usr/bin/env python
# encoding: utf-8
'''
@file: urls.py
@time: 2018/11/26 9:50
'''

from django.urls import path
from courses.api import views

app_name = 'api'
urlpatterns = [
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/<pk>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),
]






 