Manager
=======

Overview
--------
Il manager gestisce i vari progetti creati dagli utenti ed è un classico project Django ed è quindi
formato dai moduli tipici del framework.


Views
-----
Le vievs ricevono dati dall'interfaccia, li elaborano e li usano per gestire i vari progetti.

.. py:function:: new_project(request)

    Crea un nuovo progetto

    :param request: Richiesta http con i dati per la creazione di un nuovo progetto
    :type request: HttpRequest_
    :return: Risposta con i dati del nuovo progetto ed il template a cui mandarla
    :rtype: HttpResponse_

.. py:function:: open_project(request)

    Apre il progetto scelto dall'utente

    :param HttpRequest request: Richiesta http con i dati del progetto da aprire
    :type request: HttpRequest_
    :return: Risposta con i dati del progetto ed il template a cui mandarla
    :rtype: HttpResponse_

.. py:function:: showProjects(request)

    Mostra tutti i progetti presenti

    :param request: Richiesta http di mostrare i progetti
    :type request: HttpRequest_
    :return: Risposta con i progetti ed il template a cui mandarla
    :rtype: HttpResponse_

.. py:function:: delete_project(request)

    Elimina il progetto corrente

    :param request: Richiesta http di eliminare il progetto corrente
    :type request: HttpRequest_
    :return: Risposta della corretta eliminazione ed il template a cui mandarla
    :rtype: HttpResponse_

.. py:function:: change_project_data(request)

    Modifica i dati del progetto corrente

    :param request: Richiesta http con i dati da modificare
    :type request: HttpRequest_
    :return: Risposta della corretta modifica ed il template a cui mandarla
    :rtype: HttpResponse_

.. py:function:: create_schema_SQL(request)

    Crea lo schema SQL dal grafo del progetto corrente

    :param request: Richiesta http con i dati del grafo
    :type request: HttpRequest_
    :return: Risposta della corretta creazione ed il template a cui mandarla
    :rtype: HttpResponse_

.. py:function:: create_schema_NEO4J(request)

    Crea lo schema neo4j dal grafo del progetto corrente

    :param request: Richiesta http con i dati del grafo
    :type request: HttpRequest_
    :return: Risposta della corretta creazione ed il template a cui mandarla
    :rtype: HttpResponse_

Function
--------

.. py:function:: crea_proprieta(proprieta, domini, list_unique, pk=None)

    Crea le proprietà del nodo o dell'arco esaminato

    :param proprieta: Dizionario delle proprietà del nodo o dell'arco
    :type proprieta: dict_
    :param domini: Dizionario dei domini
    :type domini: dict_
    :param list_unique: Lista delle proprietà unique
    :type list_unique: list_
    :param str pk: Chiave primaria
    :return: La stringa delle proprietà da scrivere nel file dei models del progetto corrente
    :rtype: str

.. py:function:: crea_vincoli(vincoli, nome)

    Crea le proprietà del nodo o dell'arco esaminato

    :param vincoli: Dizionario dei vincoli del nodo o dell'arco
    :type vincoli: dict_
    :param str nome: nome del nodo o dell'arco
    :return: La stringa della classe clean da scrivere nel file dei models del progetto corrente
    :rtype: str

    .. _HttpRequest: https://docs.djangoproject.com/en/2.0/ref/request-response/#httprequest-objects
    .. _HttpResponse: https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
    .. _dict: https://docs.python.org/2/tutorial/datastructures.html#dictionaries
    .. _list: https://docs.python.org/2/tutorial/datastructures.html#more-on-lists


Models
------
.. py:class:: Project()

    Model per i progetti

    :extend: Model_

    .. py:attribute:: id

        Identificativo di un progetto

        :istance: AutoField_
        :type: int

    .. py:attribute:: name_project

        Nome del progetto

        :istance: CharField_
        :type: str

    .. py:attribute:: name_db

        Nome del database

        :istance: CharField_
        :type: str

    .. py:attribute:: dbms

        DBMS del progetto

        :istance: CharField_
        :type: str

    .. py:attribute:: description

        Descrizione del progetto

        :istance: TextField_
        :type: str

    .. py:attribute:: port

        Porta http del progetto

        :istance: IntegerField_
        :type: int

    .. py:attribute:: folder

        Path del progetto

        :istance: IntegerField_
        :type: int

    .. py:attribute:: created_date

        Data di creazione del progetto

        :istance: DateField_
        :type: date

    .. py:attribute:: graph

        Grafo del progetto

        :istance: JSONField_
        :type: int

        .. _Model: https://docs.djangoproject.com/en/2.0/ref/models/instances/#django.db.models.Model
        .. _AutoField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#autofield
        .. _CharField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#charfield
        .. _TextField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#textfield
        .. _IntegerField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#integerfield
        .. _FilePathField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#filepathfield
        .. _DateField: https://docs.djangoproject.com/en/2.0/ref/models/fields/#datefield
        .. _JSONField: https://pypi.org/project/django-jsonfield/

