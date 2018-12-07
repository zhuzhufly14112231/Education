#!/usr/bin/env python
# encoding: utf-8
'''
@file: fields.py
@time: 2018/11/20 16:08
'''

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    def __init__(self,for_fields=None,*args,**kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args,**kwargs)

    # 这个方法是在save到数据库之前执行的
    def pre_save(self, model_instance, add):
        if getattr(model_instance,self.attname) is None:
            # 如果没有值,查询自己所在表的全部内容,找到最后一条,设置临时value=最后的序号+1
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # 如果存在for_fields参数,通过这个参数取对应的数据行
                    query = {field:getattr(model_instance,field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # 取最后一个数据对象的编号
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname,value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance,add)





