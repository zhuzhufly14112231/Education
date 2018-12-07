#!/usr/bin/env python
# encoding: utf-8
'''
@file: urls.py
@time: 2018/11/21 10:34
'''
from django.urls import path
from courses import views


urlpatterns = [
    path(
        'mine/',
        views.ManageCourseListView.as_view(),
        name='manage_course_list'),
    path(
        'create/',
        views.CourseCreateView.as_view(),
        name='course_create'),
    path(
        '<pk>/edit/',
        views.CourseUpdateView.as_view(),
        name='course_update'),
    path(
        '<pk>/delete/',
        views.CourseDeleteView.as_view(),
        name='course_delete'),
    path(
        '<pk>/module/',
        views.CourseModuleView.as_view(),
        name='course_module'),
    path(
        'module/<int:module_id>/content/<model_name>/create/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_create'),
    path(
        'module/<int:module_id>/content/<model_name>/<id>/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_update'),
    path(
        'content/<int:id>/delete/',
        views.ContentDeleteView.as_view(),
        name='module_content_delete'),
    path(
        'module/<int:module_id>/',
        views.ModuleContentListView.as_view(),
        name='module_content_list'),
    path(
        'subject/<slug:subject>/',
        views.CourseListView.as_view(),
        name='course_list_subject'),
    path(
        '<slug:slug>/',
        views.CourseDetailView.as_view(),
        name='course_detail'),
]
