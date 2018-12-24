"""
Modulo per la generalizzazione dei campi per SQLite e MySQL, contenente le strutture dati al cui interno sono
incapsulate le chiamate alle funzioni di __init__ delle super classi.
"""

from __future__ import unicode_literals

from django.db import models

'''
Funzione di modifica degli attributi da generico a API Django per i campi dei tipi:
- primary_key --> ok per Djnago
- unique --> ok per Djnago
- default --> ok per Djnago
- notNull --> null con valore inverso
- choices --> ok per Djnago
'''
def FromGenToDjangoType(attr):
    if 'notNull' in attr:
        attr['null'] = not attr.pop('notNull')
    return attr


'''
Funzione di modifica degli attributi da generico a API Django per i campi delle relationship:
- class --> to
- label --> da eliminare
- cardinality_source --> da eliminare
- cardinality_target --> da eliminare
- direction --> da eliminare
'''
def FromGenToDjangoRel(attr):
    if 'class' in attr:
        attr['to'] = attr.pop('class')
    if 'label' in attr:
        attr.pop('label')
    if 'cardinalitySource' in attr:
        attr.pop('cardinalitySource')
    if 'cardinalityTarget' in attr:
        attr.pop('cardinalityTarget')
    if 'direction' in attr:
        attr.pop('direction')
    return attr


# Classi per i Field types
class MyIDField(models.AutoField):
    def __init__(self, *args, **kwargs):
        kwargs = FromGenToDjangoType(kwargs)
        super(MyIDField, self).__init__(*args, **kwargs)


class MyBooleanField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs = FromGenToDjangoType(kwargs)
        super(MyBooleanField, self).__init__(*args, **kwargs)


class MyStringField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs = FromGenToDjangoType(kwargs)
        kwargs['max_length'] = 255
        super(MyStringField, self).__init__(*args, **kwargs)


class MyDateField(models.DateField):
    def __init__(self, **kwargs):
        kwargs = FromGenToDjangoType(kwargs)
        super(MyDateField, self).__init__(**kwargs)


class MyFloatField(models.FloatField):
    def __init__(self, **kwargs):
        kwargs = FromGenToDjangoType(kwargs)
        super(MyFloatField, self).__init__(**kwargs)


class MyIntegerField(models.IntegerField):
    def __init__(self, **kwargs):
        kwargs = FromGenToDjangoType(kwargs)
        super(MyIntegerField, self).__init__(**kwargs)


# classe per le relationship
class MyRelationship(object):
    def __new__(cls, to, *args, **kwargs):
        # relationship molti a molti
        if ((kwargs['cardinalitySource'] == '1 - N' or kwargs['cardinalitySource'] == '0 - N') and
                (kwargs['cardinalityTarget'] == '1 - N' or kwargs['cardinalityTarget'] == '0 - N')):
            kwargs = FromGenToDjangoRel(kwargs)
            if 'model' in kwargs:
                kwargs['through'] = kwargs.pop('model')
            return MyManyToManyField(to, **kwargs)
        # relationship uno a molti
        if ((kwargs['cardinalitySource'] == '1 - N' or kwargs['cardinalitySource'] == '0 - N') and
                (kwargs['cardinalityTarget'] == '1 - 1' or kwargs['cardinalityTarget'] == '0 - 1')) or\
                ((kwargs['cardinalityTarget'] == '1 - N' or kwargs['cardinalityTarget'] == '0 - N') and
                 (kwargs['cardinalitySource'] == '1 - 1' or kwargs['cardinalitySource'] == '0 - 1')):
            kwargs = FromGenToDjangoRel(kwargs)
            if 'model' in kwargs:  # viene tolto il model perche' non serve nel campo foreign key
                kwargs.pop('model')
            return MyOneToManyField(to, on_delete=models.CASCADE, **kwargs)
        # relationship uno a uno
        if ((kwargs['cardinalitySource'] == '1 - 1' or kwargs['cardinalitySource'] == '0 - 1') and
                (kwargs['cardinalityTarget'] == '1 - 1' or kwargs['cardinalityTarget'] == '0 - 1')):
            kwargs = FromGenToDjangoRel(kwargs)
            if 'model' in kwargs:  # viene tolto il model perche' non serve nel campo foreign key
                kwargs.pop('model')
            return MyOneToOneField(to, on_delete=models.CASCADE, **kwargs)


class MyManyToManyField(models.ManyToManyField):
    def __init__(self, to, **kwargs):
        super(MyManyToManyField, self).__init__(to, **kwargs)


class MyOneToManyField(models.OneToOneField):
    def __init__(self, to, **kwargs):
        super(MyOneToManyField, self).__init__(to, **kwargs)


class MyOneToOneField(models.OneToOneField):
    def __init__(self, to, **kwargs):
        super(MyOneToOneField, self).__init__(to, **kwargs)


# Classe per i nodi
class MyNode(models.Model):
    def __init__(self, *args, **kwargs):
        super(MyNode, self).__init__(*args, **kwargs)

    @classmethod
    def getNodes(cls):
        """
        Metodo per ottenere tutti i nodi di cls
        :return: QuerySet
        """
        return cls.objects.all()

    @classmethod
    def countNodes(cls):
        """
        Metodo per contare tutti i nodi di cls
        :return: Integer
        """
        return cls.objects.count()

    @classmethod
    def orderByParam(cls, param):
        """
        Metodo per ordinare i nodi della classe cls
        :param param: criterio di ordinamento
        :return: QuerySet
        """
        return cls.objects.order_by(param)

    @classmethod
    def getSubSetNodes(cls, offset, limit):
        """
        Metodo per ottenere un sotto insieme dei nodi della classe cls
        :param offset: posizione del primo nodo considerato (inizia da 0)
        :param limit: posizione dell'ultimo nodo considerato
        :return: QuerySet
        """
        return cls.getNodes()[offset:limit]

    @classmethod
    def getDistinctNodes(cls, *args):
        """
        Metodo per ottenere i nodi distinti della classe cls
        :param args: parametri su cui eliminare i diplicati
        :return: QuerySet
        """
        return cls.getNodes().distinct(*args)


# Classe per gli archi
class MyEdge(models.Model):
    def __init__(self, *args, **kwargs):
        super(MyEdge, self).__init__(*args, **kwargs)

    @classmethod
    def getEdges(cls):
        """
        Metodo per ottenere tutti gli archi di cls
        :return: QuerySet
        """
        return cls.objects.all()

    @classmethod
    def countEdges(cls):
        """
        Metodo per contare tutti gli archi di cls
        :return: Integer
        """
        return cls.objects.count()

    @classmethod
    def orderByParam(cls, param):
        """
        Metodo per ordinare gli archi della classe cls
        :param param: criterio di ordinamento
        :return: QuerySet
        """
        return cls.objects.order_by(param)
