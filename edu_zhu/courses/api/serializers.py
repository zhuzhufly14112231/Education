#!/usr/bin/env python
# encoding: utf-8
'''
@file: serializers.py
@time: 2018/11/26 9:30
'''

from rest_framework import serializers
from courses.models import Subject,Course

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['owner', 'subject', 'title', 'slug']



 