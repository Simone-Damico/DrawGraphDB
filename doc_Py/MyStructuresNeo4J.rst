MyStructuresNeo4J
=================

Overview
--------
MyStructuresSQL contiene le classi generiche per l'interazione con le API neomodel_ per i database a grafi.

.. _neomodel: https://neomodel.readthedocs.io/en/latest/index.html

Classi dei Field Type
---------------------
Classi per la definizioni dei campi delle proprietà di nodi ed archi.

.. py:class:: MyIDField(**kwargs)

    :extend: UniqueIdProperty_

    Classe per la definizione del campo ID.

.. py:class:: MyBooleanField(**kwargs)

    :extend: BooleanProperty_

    Classe per la definizione del campo boolean.

.. py:class:: MyStringField(*args, **kwargs)

    :extend: StringProperty_

    Classe per la definizione del campo string.

.. py:class:: MyDateField(**kwargs)

    :extend: DateProperty_

    Classe per la definizione del campo date.

.. py:class:: MyFloatField(**kwargs)

    :extend: FloatProperty_

    Classe per la definizione del campo float.

.. py:class:: MyIntegerField(**kwargs)

    :extend: IntegerProperty_

    Classe per la definizione del campo integer.


.. _UniqueIdProperty: https://neomodel.readthedocs.io/en/latest/module_documentation.html#neomodel.properties.UniqueIdProperty
.. _BooleanProperty: https://neomodel.readthedocs.io/en/latest/module_documentation.html#neomodel.properties.BooleanProperty
.. _StringProperty: https://neomodel.readthedocs.io/en/latest/module_documentation.html#neomodel.properties.StringProperty
.. _DateProperty: https://neomodel.readthedocs.io/en/latest/module_documentation.html#neomodel.properties.DateProperty
.. _FloatProperty: https://neomodel.readthedocs.io/en/latest/module_documentation.html#neomodel.properties.FloatProperty
.. _IntegerProperty: https://neomodel.readthedocs.io/en/latest/module_documentation.html#neomodel.properties.IntegerProperty


Classi dei Models Type
----------------------
Classi per la definizioni dei nodi e degli archi.

.. py:class:: MyNode(*args, **kwargs)

    :extend: StructuredNode_

    Clase per la definizione dei nodi.

    .. py:classmethod:: getNodes()

        :return: Insieme dei nodi di una classe istanza di MyNode.
        :rtype: NodeSet_

        Metodo per ottenere tutti i nodi di una classe istanza di MyNode.

    .. py:classmethod:: countNodes()

        :return: numero dei nodi di una classe istanza di MyNode.
        :rtype: int

        Metodo per contare tutti i nodi di una classe istanza di MyNode.

    .. py:classmethod:: orderByParam(param)

        :param str param: criterio di ordinamento
        :return: Lista dei nodi istanze di una classe istanza di MyNode ordinate secondo param.
        :rtype: NodeSet_

        Metodo per ordinare i nodi di una classe istanza di MyNode secondo il valore di un'attributo.

.. py:class:: MyEdge(*args, **kwargs)

    :extend: StructuredRel_

    Classe per la definizione degli archi.

    .. py:classmethod:: countEdges()

        :return: numero dei nodi di una classe istanza di MyEdge
        :rtype: int

        Metodo per contare tutti i nodi di una classe istanza di MyEdge.

.. _StructuredNode: https://neomodel.readthedocs.io/en/latest/module_documentation.html#neomodel.core.StructuredNode
.. _StructuredRel: https://neomodel.readthedocs.io/en/latest/module_documentation.html#module-neomodel.relationship
.. _NodeSet: https://neomodel.readthedocs.io/en/latest/module_documentation.html#neomodel.match.NodeSet

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

    :extend: RelationshipDefinition

    Classe per la definizione delle relationship molti a molti.

.. py:class:: MyOneToOneField(cls_name, label, direction, cardinalitySource, cardinalityTarget, model=None):

    :param str cls_name: classe del'altro nodo collegato dalla relationship
    :param label: Label dell'arco
    :param str direction: Direzione dell'arco, può essere OUTGOING o INCOMING
    :param str cardinalitySource: Cardinalità massima e minima del nodo sorgente
    :param str cardinalityTarget: Cardinalità massima e minima del nodo destinazione
    :param str model: L'arco a cui si riferisce la relationship

    :extend: RelationshipDefinition

    Classe per la definizione delle relationship uno a uno.

.. py:class:: MyManyToOneField(cls_name, label, direction, cardinalitySource, cardinalityTarget, model=None):

    :param str cls_name: classe del'altro nodo collegato dalla relationship
    :param label: Label dell'arco
    :param str direction: Direzione dell'arco, può essere OUTGOING o INCOMING
    :param str cardinalitySource: Cardinalità massima e minima del nodo sorgente
    :param str cardinalityTarget: Cardinalità massima e minima del nodo destinazione
    :param str model: L'arco a cui si riferisce la relationship

    :extend: RelationshipDefinition

    Classe per la definizione delle relationship uno a molti.


