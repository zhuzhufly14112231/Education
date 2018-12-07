#!/usr/bin/env python
# encoding: utf-8
'''
@file: urls.py
@time: 2018/11/22 15:43
'''
from django.urls import path
from students import views
from django.views.decorators.cache import cache_page

app_name = 'edu_student'
urlpatterns = [
    path(
        'register/',
        views.StudentRegistrationView.as_view(),
        name='student_register'),
    path(
        'enroll-course/',
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course'),
    path(
        'course/',
        views.StudentCourseListView.as_view(),
        name='student_course_list'),
    path(
        'course/<pk>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail'),
    path(
        'course/<pk>/<module_id>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail_module'),
]
