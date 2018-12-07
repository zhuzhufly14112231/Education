from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from courses.fields import OrderField
from django.template.loader import render_to_string
# Create your models here.

class Subject(models.Model):
    # 不同主题
    title = models.CharField(max_length=200,verbose_name='主题')
    slug = models.SlugField(max_length=200,unique=True,verbose_name='标识')
    class Meta:
        db_table = 'subject'

    def __str__(self):
        return self.title


class Course(models.Model):
    # 课程的拥有者
    owner = models.ForeignKey(User,related_name='course_created',on_delete=models.CASCADE)
    # 课程所属的主题
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    # 课程的标题
    title = models.CharField(max_length=200,verbose_name='标题')
    # 用来生成url
    slug = models.SlugField(max_length=200,unique=True)
    # 课程的简介
    overview = models.TextField()
    # 课程创建的时间
    created = models.DateTimeField(auto_now_add=True)
    # 课程与学生之间添加一个多对多的关系
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        # db_table='courses'
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Module(models.Model):
    # 章节
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    # 章节的标题
    title = models.CharField(max_length=200,verbose_name='标题')
    # 章节的详细介绍
    description = models.TextField(blank=True)
    order = OrderField(for_fields=['course'],blank=True)

    def __str__(self):
        return '{}.{}'.format(self.order,self.title)

    class Meta:
        db_table = 'module'
        ordering = ('order',)

class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)
    # limit_choices_to  限定contenttype对象是这四个模型
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={'model__in':('text','file','image','video')})
    object_id = models.PositiveIntegerField()
    # 通用的关联关系字段,通过合并content_type和object_id进行关联的
    item = GenericForeignKey('content_type','object_id')
    order = OrderField(for_fields=['module'],blank=True)

    class Meta:
        db_table = 'content'
        ordering = ('order',)

class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    # 使用内置的render_to_string,传入一个模板名称和上下文
    # 然后渲染成为一个html字符串
    # 每种不同的类型的内容采用不同名称的模板
    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name),{'item':self})

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()








