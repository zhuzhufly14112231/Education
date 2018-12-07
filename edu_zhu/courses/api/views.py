#!/usr/bin/env python
# encoding: utf-8
'''
@file: views.py
@time: 2018/11/26 9:46
'''

from rest_framework import generics
from courses.models import Subject,Course
from courses.api.serializers import SubjectSerializer,CourseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseEnrollView(APIView):
    authentication_classes = (BasicAuthentication,)
    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})













 