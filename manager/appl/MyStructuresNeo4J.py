"""
Modulo per la generalizzazione dei campi per Neo4J, contenente le strutture dati al cui interno sono
incapsulate le chiamate alle funzioni di __init__ delle super classi.
"""

from __future__ import unicode_literals

from neomodel import *


'''
Funzione di modifica degli attributi da generico a API neomodel per i campi dei tipi:
- primary_key --> unique_index
- unique --> unique_index
- default --> ok per Neomodel
- notNull --> required
- choices --> ok per Neomodel
'''
def FromGenToNeomodelType(attr):
    if 'primary_key' in attr:
        attr['unique_index'] = attr.pop('primary_key')
    # Per neomodel unique_index e default sono mutulamente escusive, se c'e' il primo tolgo il secondo
    if 'unique' in attr:
        attr['unique_index'] = attr.pop('primary_key')
    if attr[attr.keys()[0]] is None:
        attr.pop('default')
    if attr[attr.keys()[0]] is not None:
        attr.pop('notNull')
    if 'notNull' in attr:
        attr['required'] = attr.pop('notNull')
    return attr

'''
Funzione di modifica degli attributi da generico a API Django per i campi delle relationship:
- class --> cls_name
- label --> relation_type
- cardinality_source --> cardinality
- cardinality_target --> da eliminare
- direction --> ok per Neomodel
- model --> ok per Neomodel
'''
def FromGenToNeomodelRel(attr):
    if 'class' in attr:
        attr['cls_name'] = attr.pop('class')
    if 'label' in attr:
        attr['relation_type'] = attr.pop('label')
    if 'cardinalitySource' in attr:
        if attr['cardinalitySource'] == '0 - 1':
            attr['cardinality'] = 'ZeroOrOne'
        elif attr['cardinalitySource'] == '1 - 1':
            attr['cardinality'] = 'One'
        elif attr['cardinalitySource'] == '0 - N':
            attr['cardinality'] = 'ZeroOrMore'
        elif attr['cardinalitySource'] == '1 - N':
            attr['cardinality'] = 'OneOrMore'
    if 'cardinalityTarget' in attr:
        attr.pop('cardinalityTarget')
    return attr


# Classi per i Property types
class MyIDField(UniqueIdProperty):
    def __init__(self):
        super(MyIDField, self).__init__()


class MyBooleanField(BooleanProperty):
    def __init__(self, **kwargs):
        kwargs = FromGenToNeomodelType(kwargs)
        super(MyBooleanField, self).__init__(**kwargs)


class MyStringField(StringProperty):
    def __init__(self, *args, **kwargs):
        kwargs = FromGenToNeomodelType(kwargs)
        super(MyStringField, self).__init__(*args, **kwargs)


class MyDateField(DateProperty):
    def __init__(self, **kwargs):
        kwargs = FromGenToNeomodelType(kwargs)
        super(MyDateField, self).__init__(**kwargs)


class MyFloatField(FloatProperty):
    def __init__(self, **kwargs):
        kwargs = FromGenToNeomodelType(kwargs)
        super(MyFloatField, self).__init__(**kwargs)


class MyIntegerField(IntegerProperty):
    def __init__(self, **kwargs):
        kwargs = FromGenToNeomodelType(kwargs)
        super(MyIntegerField, self).__init__(**kwargs)

# Classi per le Relationship type
class MyEdge(StructuredRel):
    def __init__(self, *args, **kwargs):
        super(MyEdge, self).__init__(*args, **kwargs)

    @classmethod
    def countEdges(cls):
        """
        Metodo per contare i nodi della classe cls
        :return: Intero
        """
        res = db.cypher_query('MATCH ()-->() RETURN count(*)')
        return res[0][0][0]


class MyRelationship(object):
    def __new__(cls, *args, **kwargs):
        kwargs = FromGenToNeomodelRel(kwargs)
        if kwargs['direction'] == 'OUTGOING':
            RelationshipTo(kwargs['cls_name'], kwargs['relation_type'], kwargs['cardinality'], kwargs['model'])
        elif kwargs['direction'] == 'INCOMING':
            RelationshipFrom(kwargs['cls_name'], kwargs['relation_type'], kwargs['cardinality'], kwargs['model'])
        return RelationshipDefinition(kwargs['relation_type'], kwargs['cls_name'], kwargs['direction'], kwargs['model'])


# Classi per i Node types
class MyNode(StructuredNode):
    def __init__(self, *args, **kwargs):
        super(MyNode, self).__init__(*args, **kwargs)

    @classmethod
    def getNodes(cls):
        """
        Metodo per ottenere tutti nodi della classe cls
        :return: NodeSet
        """
        return cls.nodes

    @classmethod
    def countNodes(cls):
        """
        Metodo per contare i nodi della classe cls
        :return: Intero
        """
        return len(cls.nodes)

    @classmethod
    def orderByParam(cls, parametro):
        """
        Metodo per ordinare i nodi della classe cls
        :param parametro: criterio di ordinamento
        :return: NodeSet
        """
        return cls.nodes.order_by(parametro)

    @classmethod
    def hasRel(cls, prop):
        """
        Metodo per ottenere i nodi di cls che sono coinvolti in una relationship tramite prop
        :param prop: proprieta' di cls che definisce una relationship
        :return: NodeSet
        """
        return cls.nodes.has(prop)
