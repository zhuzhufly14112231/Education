from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from students.forms import CourseEnrollForm
from courses.models import Course
# Create your views here.

class StudentRegistrationView(CreateView):
    # 需要渲染的模板位置
    template_name = 'students/register.html'
    # form_class 必须是ModelForm对象,这里用的是django内置的建立新用户的表单
    form_class = UserCreationForm
    # 成功后跳转到的url,通过反向解析获取url
    success_url = reverse_lazy('course_list')

    # 重写form_valid使用户在成功注册之后就登录
    def form_valid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    # 设置course属性 用于保存学生选择的课程对象
    # 当表单验证通过的时候,取得当前用户设置多对多关系,然后调用父类的方法保存数据
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        # TODO
        return reverse_lazy('edu_student:student_course_list')


class StudentCourseListView(LoginRequiredMixin, ListView):
    # 这个视图是给学生展示所有的课程
    model = Course
    template_name = 'students/course_list.html'

    # 重写此方法,过滤出当前学生所选的课程
    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    '''用于向学生展示他们选的课程和章节'''
    model = Course
    template_name = 'students/course_detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()

        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
            print(context)
        else:
            context['module'] = course.modules.all()
            if context['module']:
                context['module'] = context['module'][0]
            else:
                context['module'] = None
        return context





