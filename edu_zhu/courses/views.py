from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.core.cache import cache
from django.apps import apps
from django.forms.models import modelform_factory
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from courses.models import Course,Subject,Module,Content
from courses.forms import ModuleFormSet
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin,View
# TemplateResponseMixin 这个mixin提供的功能是渲染模板并且返回http响应,需要一个template_name属性,用于指定模板的位置
# 还提供render_to_response方法给模板传递上下文,并且渲染模板
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# PermissionRequiredMixin  允许具有特定权限的用户访问这个视图,超级用户具有所有权限
# Create your views here.
from students.forms import CourseEnrollForm

class OwnerMixin:
    def get_queryset(self):
        qs = super(OwnerMixin,self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin):
    model = Course
    fields = ['subject','title','slug','overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin,OwnerEditMixin):
    fields = ['subject','title','slug','overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'manage/course/forms.html'


class ManageCourseListView(OwnerCourseMixin,ListView):
    template_name = 'manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin,CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,OwnerCourseEditMixin,UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,OwnerCourseMixin,DeleteView):
    permission_required = 'courses.delete_course'
    template_name = 'manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')


class CourseModuleView(TemplateResponseMixin, View):
    template_name = 'manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk, *args, **kwargs):
        '''
        这个方法是View视图的方法,是一个分发器,http请求进来之后,最先执行的是dispatch
        这个方法把小写的http请求的种类分发给同名的方法
        比如:GET请求会被返送到get()方法
        :param request:
        :param pk: primary key
        :return:
        '''
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({"courses":self.course,'formset':formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'courses':self.course,'formset':formset})

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text','video','image','file']:
            return apps.get_model(app_label='courses',model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        # get_form 获取需要修改的四种内容之一生成的表单
        # 如果没有id,self.obj = None
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # 新内容
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form':form, 'object':self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        # 获得content对象
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        # 删除相关的text,video,image,file对象
        content.item.delete()
        # 删除content对象
        content.delete()
        # 重定向到module_content_list
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})

class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/list.html'

    def get(self, request, subject=None):
        # 获取所有的主题,使用annotate分组,count聚合方法生成一个包含课程数量的字段
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects)
        # 获取所有的课程,增加一个按照章节分组计数的字段
        all_courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = 'subject_{}_courses'.format(subject.id)
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key,courses)
        else:
            # 缓存智能是用于存储最终可供页面直接使用的查询结果,不能在中间步骤缓存
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'subjects':subjects,'subject':subject,'courses':courses})

class CourseDetailView(DetailView):
    '''
    显示一个具体的课程视图
    '''
    model = Course
    template_name = 'courses/detail.html'

    # 重写此方法,把这个表单添加到模板变量中,并且将表单隐藏的字段内容初始化成当前的课程对象
    # 然后就可以直接通过按钮提交表单,不需要用户填写隐藏字段
    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context



