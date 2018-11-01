MyStructuresSQL
===============

Overview
--------
MyStructuresSQL contiene le classi generiche per l'interazione con le API Django_ per i database relazionali.

.. _Django: https://www.djangoproject.com

Classi dei Field Type
---------------------
Classi per la definizioni dei campi delle proprietà di nodi ed archi.

.. py:class:: MyIDField(**kwargs)

    :extend: AutoField_

    Classe per la definizione del campo ID

.. py:class:: MyBooleanField(*args, **kwargs)

    :extend: BooleanField_

    Classe per la definizione del campo boolean

.. py:class:: MyStringField(*args, **kwargs)

    :extend: CharField_

    Classe per la definizione del campo string

.. py:class:: MyDateField(*args, **kwargs)

    :extend: DateField_

    Classe per la definizione del campo date

.. py:class:: MyFloatField(*args, **kwargs)

    :extend: FloatField_

    Classe per la definizione del campo float

.. py:class:: MyIntegerField(*args, **kwargs)

    :extend: IntegerField_

    Classe per la definizione del campo integer


.. _AutoField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#autofield
.. _BooleanField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#booleanfield
.. _CharField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#charfield
.. _DateField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#datefield
.. _FloatField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#floatfield
.. _IntegerField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#integerfield

Classi dei Models Type
----------------------
Classi per la definizioni delle relazioni di nodi e archi.

.. py:class:: MyNode(*args, **kwargs)

    :extend: Model_

    Clase per la definizione dei nodi

    .. py:classmethod:: getNodes()

        :return: Insieme dei nodi di una classe istanza di MyNode
        :rtype: QuerySet_

        Metodo per ottenere tutti i nodi di una classe istanza di MyNode

    .. py:classmethod:: countNodes()

        :return: numero dei nodi di una classe istanza di MyNode
        :rtype: int

        Metodo per contare tutti i nodi di una classe istanza di MyNode

    .. py:classmethod:: orderByParam(param)

        :param str param: criterio di ordinamento
        :return: Lista dei nodi istanze di una classe istanza di MyNode ordinate secondo param
        :rtype: QuerySet_

        Metodo per ordinare i nodi di una classe istanza di MyNode secondo il valore di un'attributo

    .. py:classmethod:: getSubSetNodes(offset, limit)

        :param int offset: posizione del primo nodo considerato (inizia da 0)
        :param int limit: posizione dell'ultimo nodo considerato
        :return: Sotto insieme dei nodi di una classe istanza di MyNode da offset a limit
        :rtype: QuerySet_

        Metodo per ottenere un sotto insieme dei nodi di una classe istanza di MyNode

    .. py:classmethod:: getDistinctNodes(*args)

        :param \*args: parametri su cui eliminare i diplicati
        :type \*args: list_
        :return: Insieme distinto dei nodi istanze di cls
        :rtype: QuerySet_

        Metodo per ottenere i nodi distinti di una classe istanza di MyNode secondo gli attributi di \*args

.. py:class:: MyEdge(*args, **kwargs)

    :extend: Model_

    Classe per la definizione degli archi

    .. py:classmethod:: getEdges()

        :return: Insieme dei nodi di una classe istanza di MyEdge
        :rtype: QuerySet_

        Metodo per ottenere tutti i nodi di una classe istanza di MyEdge

    .. py:classmethod:: countEdges()

        :return: numero dei nodi di una classe istanza di MyEdge
        :rtype: int

        Metodo per contare tutti i nodi di una classe istanza di MyEdge

    .. py:classmethod:: orderByParam(param)

        :param str param: criterio di ordinamento
        :return: Lista dei nodi istanze di una classe istanza di MyEdge ordinate secondo param
        :rtype: QuerySet_

        Metodo per ordinare i nodi di una classe istanza di MyEdge secondo il valore di un'attributo

.. _Model: https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model
.. _list: https://docs.python.org/2/tutorial/datastructures.html#more-on-lists
.. _QuerySet: https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet

Classi delle Relationship Type
------------------------------

Classi per la definizione delle relationship.

.. py:class:: MyManyToManyField(cls_name, label, direction, cardinalitySource, cardinalityTarget, model=None):

    :param str cls_name: classe del'altro nodo collegato dalla relationship
    :param label: Label dell'arco
    :param str direction: Direzione dell'arco, può essere OUTGOING o INCOMING
    :param str cardinalitySource: Cardinalità massima e minima del nodo sorgente
    :param str cardinalityTarget: Cardinalità massima e minima del nodo destinazione
    :param str model: L'arco a cui si riferisce la relationship

    :extend: ManyToManyField_

    Classe per la definizione delle relationship molti a molti.

.. py:class:: MyOneToOneField(cls_name, label, direction, cardinalitySource, cardinalityTarget, model=None):

    :param str cls_name: classe del'altro nodo collegato dalla relationship
    :param label: Label dell'arco
    :param str direction: Direzione dell'arco, può essere OUTGOING o INCOMING
    :param str cardinalitySource: Cardinalità massima e minima del nodo sorgente
    :param str cardinalityTarget: Cardinalità massima e minima del nodo destinazione
    :param str model: L'arco a cui si riferisce la relationship

    :extend: OneToOneField_

    Classe per la definizione delle relationship uno a uno.

.. py:class:: MyManyToOneField(cls_name, label, direction, cardinalitySource, cardinalityTarget, model=None):

    :param str cls_name: classe del'altro nodo collegato dalla relationship
    :param label: Label dell'arco
    :param str direction: Direzione dell'arco, può essere OUTGOING o INCOMING
    :param str cardinalitySource: Cardinalità massima e minima del nodo sorgente
    :param str cardinalityTarget: Cardinalità massima e minima del nodo destinazione
    :param str model: L'arco a cui si riferisce la relationship

    :extend: ForeignKey_

    Classe per la definizione delle relationship uno a molti.

.. _ManyToManyField: https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ManyToManyField
.. _OneToOneField: https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.OneToOneField
.. _ForeignKey: https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ForeignKey

