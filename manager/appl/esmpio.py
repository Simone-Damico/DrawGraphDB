from django.db import models
from abc import ABCMeta, abstractmethod


def FromGenToDjango(attr):
    if 'notNull' in attr:
        attr['null'] = not attr.pop('notNull')
    return attr


class GenericBool:

    __metaclass__ = ABCMeta

    @abstractmethod
    def __new__(cls, *args, **kwargs):
        pass


class MyBooleanField(GenericBool):
    def __new__(cls, *args, **kwargs):
        kwargs = FromGenToDjango(kwargs)
        return models.BooleanField(*args, **kwargs)


class GenericInt:

    __metaclass__ = ABCMeta

    @abstractmethod
    def __new__(cls, *args, **kwargs):
        pass


class MyIntegerField(GenericInt):
    def __new__(cls, *args, **kwargs):
        kwargs = FromGenToDjango(kwargs)
        return models.IntegerField(*args, **kwargs)


class GenericSting:

    __metaclass__ = ABCMeta

    @abstractmethod
    def __new__(cls, *args, **kwargs):
        pass


class MyStringField(GenericSting):
    def __new__(cls, *args, **kwargs):
        kwargs = FromGenToDjango(kwargs)
        return models.CharField(*args, **kwargs)








class genericRel:

    __metaclass__ = ABCMeta

    @abstractmethod
    def __new__(cls, *args, **kwargs):
        pass




#sql
class MyRelFieldSQL(genericRel):
    def __new__(cls, *args, **kwargs):
        if kwargs['mol'] == 'uno-molti':
            return models.ForeignKey(*args, **kwargs)
        elif kwargs['mol'] == 'uno-uno':
            return models.OneToOneField(*args, **kwargs)
        elif kwargs['mol'] == 'molti-molti':
            return models.ManyToManyField(*args, **kwargs)