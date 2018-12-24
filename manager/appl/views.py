# coding=utf-8
import os
import json
import subprocess
from . import MyUtils

import time

from django.http import HttpResponse
from django.shortcuts import render
from django.core.management import call_command
from django.db import connection
from django.utils import timezone
from .models import Project
from django.core import serializers


# Create your views here.

main_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # ../serverdb
current_server = None
current_project = None
project_port = Project.objects.order_by('port').last().port  # valore di porta massimo usato fino ad ora
'''if current_server is not None:
        current_server.terminate()'''
'''
    current_server = subprocess.Popen(
        ['python', 'manage.py', 'runserver', '--settings=' + current_project.name_project + '.settings',
         str(current_project.port)], cwd=current_project.folder)
    '''


def grafo(request):
    return render(request, 'graphEd/graphEd.html')


def new_project(request):
    global main_folder, current_project, project_port
    # Prendo i dati dalla request
    project_name = json.loads(request.body)['name']
    project_description = json.loads(request.body)['description']
    print("Start create project", project_name)

    # Creo la struttura delle cartelle e dei file per il nuovo progetto
    project_folder = os.path.join(main_folder, project_name)
    app_folder = os.path.join(project_folder, 'app')
    os.mkdir(project_folder)
    os.mkdir(app_folder)
    project_port = project_port + 1
    call_command('startproject', project_name, project_folder)
    call_command('startapp', 'app', app_folder)

    # Modifico il file setting del progetto appena creato a seconda del dbms scelto dall'utente
    with open(os.path.join(project_folder, project_name, "settings.py")) as old, \
            open(os.path.join(project_folder, project_name, "new.py"), "w") as new:
        for line in old:
            new.write(line)
            if 'django.contrib.staticfiles' in line:
                new.write("    'app',\n")
        new.write("STATIC_ROOT = os.path.join(BASE_DIR, 'static')\n")
    os.remove(os.path.join(project_folder, project_name, "settings.py"))
    os.rename(os.path.join(project_folder, project_name, "new.py"),
              os.path.join(project_folder, project_name, "settings.py"))

    # Modifico il file delle urls del progetto includendo il file delle urls di app
    with open(os.path.join(project_folder, project_name, "urls.py")) as old, \
            open(os.path.join(project_folder, project_name, "new.py"), "w") as new:
        for line in old:
            if "from django.conf.urls import url" in line:
                line = line.replace("from django.conf.urls import url", "from django.conf.urls import include, url")
            new.write(line)
            if "url(r'^admin/', admin.site.urls)," in line:
                new.write("    url(r'^', include('app.urls')),\n")
    os.remove(os.path.join(project_folder, project_name, "urls.py"))
    os.rename(os.path.join(project_folder, project_name, "new.py"),
              os.path.join(project_folder, project_name, "urls.py"))

    # Creo il file app.url di app
    MyUtils.copy(os.path.join(main_folder, 'manager', 'appl', 'projectTemplates', 'urlsTemplate.py'),
                 os.path.join(project_folder, 'app', 'urls.py'))
    MyUtils.copy(os.path.join(main_folder, 'manager', 'appl', 'projectTemplates', 'viewsTemplates.py'),
                 os.path.join(project_folder, 'app', 'views.py'))

    # Aggiungo il progetto al database del manager
    current_project = Project(name_project=project_name,
                              name_db=None,
                              dbms=None,
                              description=project_description,
                              port=project_port,
                              folder=project_folder,
                              created_date=timezone.now(),
                              graph=None)
    current_project.save()

    # Ritorno le meta informazioni per la gestione del progetto corrente
    meta_data = {'name_project': current_project.name_project,
                 'name_db': current_project.name_db,
                 'dbms': current_project.dbms,
                 'description': current_project.description,
                 'port': current_project.port,
                 'folder': current_project.folder,
                 'created_date': str(current_project.created_date),
                 'graph': current_project.graph}
    data = json.dumps(meta_data, ensure_ascii=False)
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def open_project(request):
    global current_project
    name_project = json.loads(request.body)

    current_project = Project.objects.get(name_project=name_project)

    meta_data = {'name_project': current_project.name_project,
                 'name_db': current_project.name_db,
                 'dbms': current_project.dbms,
                 'description': current_project.description,
                 'port': current_project.port,
                 'folder': current_project.folder,
                 'created_date': str(current_project.created_date),
                 'graph': current_project.graph}
    data1 = json.dumps(meta_data, ensure_ascii=False)
    return HttpResponse(data1, content_type='graphEd/graphEd.html')


def show_projects(request):
    progetti = Project.objects.all().exclude(name_project="Manager")
    data = serializers.serialize('json', list(progetti))
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def delete_project(request):
    global current_project
    name_project = json.loads(request.body)
    print(name_project)
    Project.objects.get(name_project=name_project).delete()
    import shutil
    shutil.rmtree(current_project.folder)
    current_project = None
    return render(request, 'graphEd/graphEd.html')


def change_project_data(request):
    global current_project
    new_name = json.loads(request.body)['nome']
    new_nameDB = json.loads(request.body)['nomeDB']
    new_description = json.loads(request.body)['descrizione']
    project_folder = current_project.folder

    # Se il nome è stato cambiato vado a modificare i riferimenti nei file di setting (settings.py, urls.py, wsgi.py),
    # il nome delle cartelle nel progetto e il nome nel database del manager
    if new_name != current_project.name_project:
        with open(os.path.join(project_folder, current_project.name_project, "settings.py")) as old, \
                open(os.path.join(project_folder, current_project.name_project, "new.py"), "w") as new:
            for line in old:
                if current_project.name_project in line:
                    line = line.replace(current_project.name_project, new_name)
                new.write(line)
        os.remove(os.path.join(project_folder, current_project.name_project, "settings.py"))
        os.rename(os.path.join(project_folder, current_project.name_project, "new.py"),
                  os.path.join(project_folder, current_project.name_project, "settings.py"))

        with open(os.path.join(project_folder, current_project.name_project, "urls.py")) as old, \
                open(os.path.join(project_folder, current_project.name_project, "new.py"), "w") as new:
            for line in old:
                if current_project.name_project in line:
                    line = line.replace(current_project.name_project, new_name)
                new.write(line)
        os.remove(os.path.join(project_folder, current_project.name_project, "urls.py"))
        os.rename(os.path.join(project_folder, current_project.name_project, "new.py"),
                  os.path.join(project_folder, current_project.name_project, "urls.py"))

        with open(os.path.join(project_folder, current_project.name_project, "wsgi.py")) as old, \
                open(os.path.join(project_folder, current_project.name_project, "new.py"), "w") as new:
            for line in old:
                if current_project.name_project in line:
                    line = line.replace(current_project.name_project, new_name)
                new.write(line)
        os.remove(os.path.join(project_folder, current_project.name_project, "wsgi.py"))
        os.rename(os.path.join(project_folder, current_project.name_project, "new.py"),
                  os.path.join(project_folder, current_project.name_project, "wsgi.py"))

        current_project.name_project = new_name

    # Se il nomeDB è stato cambiato si rinomina il file del database e si cambia il suo nome nel file dei settings
    if new_nameDB != current_project.name_db:
        with open(os.path.join(project_folder, current_project.name_project, "settings.py")) as old, \
                open(os.path.join(project_folder, current_project.name_project, "new.py"), "w") as new:
            for line in old:
                if "'NAME': os.path.join(BASE_DIR, " in line:
                    line = line.replace(current_project.name_db, new_nameDB)
                new.write(line)
        os.remove(os.path.join(project_folder, current_project.name_project, "settings.py"))
        os.rename(os.path.join(project_folder, current_project.name_project, "new.py"),
                  os.path.join(project_folder, current_project.name_project, "settings.py"))

        print(os.path.join(project_folder, current_project.name_db + '.sqlite3'))
        print(os.path.join(project_folder, new_nameDB + '.sqlite3'))
        os.rename(os.path.join(project_folder, current_project.name_db + '.sqlite3'),
                  os.path.join(project_folder, new_nameDB + '.sqlite3'))

        current_project.name_db = new_nameDB

    os.rename(os.path.join(project_folder, current_project.name_project), os.path.join(project_folder, new_name))
    os.rename(project_folder, new_name)

    # Aggiorno le informazioni del progetto nel database del manager

    current_project.description = new_description
    current_project.folder = os.path.join(main_folder, new_name)
    current_project.save()

    meta_data = {'name_project': current_project.name_project,
                 'name_db': current_project.name_db,
                 'dbms': current_project.dbms,
                 'description': current_project.description,
                 'port': current_project.port,
                 'folder': current_project.folder,
                 'created_date': str(current_project.created_date)}
    data = json.dumps(meta_data, ensure_ascii=False)
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def save_graph(request):
    global main_folder, current_project
    current_project.graph = request.body
    current_project.save()
    return render(request, 'graphEd/graphEd.html')


def create_schema_SQL(request):
    global main_folder, current_project
    data = MyUtils.json_loads_byteified(request.body)
    name_db = data['nomeDB']
    dbms = data['dbms']
    graph = data['graph']
    current_project.name_db = name_db
    current_project.dbms = dbms
    current_project.graph = graph
    current_project.save()
    project_folder = current_project.folder
    print("Creazione schema SQL")

    # Modifico il file setting del progetto appena creato a seconda del dbms scelto dall'utente
    with open(os.path.join(project_folder, current_project.name_project, "settings.py")) as old, \
            open(os.path.join(project_folder, current_project.name_project, "new.py"), "w") as new:
        for line in old:
            if dbms == 'MySQL':
                if 'django.db.backends.sqlite3' in line:
                    line = line.replace('sqlite3', 'mysql')
                if 'db.sqlite3' in line:
                    line = line.replace("os.path.join(BASE_DIR, 'db.sqlite3')", "'" + name_db + "'")
            if dbms == 'SQLite':
                if 'db.sqlite3' in line:
                    line = line.replace("'db.sqlite3'", "'" + name_db + ".sqlite3'")
            if dbms == 'Neo4j':
                if 'import os' in line:
                    new.write('from neomodel import config\n')
                    new.write("config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'  # default\n")
            new.write(line)
    os.remove(os.path.join(project_folder, current_project.name_project, "settings.py"))
    os.rename(os.path.join(project_folder, current_project.name_project, "new.py"),
              os.path.join(project_folder, current_project.name_project, "settings.py"))

    # Creo i file delle strutture dati giusto in base al tipo di database
    if dbms == 'Neo4j':
        MyUtils.copy(os.path.join(main_folder, 'manager', 'appl', 'MyStructuresNeo4J.py'),
                     os.path.join(project_folder, 'app', 'MyStructuresNeo4J.py'))
    else:
        MyUtils.copy(os.path.join(main_folder, 'manager', 'appl', 'MyStructuresSQL.py'),
                     os.path.join(project_folder, 'app', 'MyStructuresSQL.py'))

    nodi = graph['nodes']
    archi = graph['links']
    domini = graph['domini']
    archi_gia_esaminati = []

    with open(os.path.join(project_folder, 'app', 'new.py'), 'w') as new:
        new.write('from __future__ import unicode_literals\n')
        new.write('# Create your models here.\n')
        new.write('from MyStructuresSQL import *\n\n')
        new.write('from django.core.exceptions import ValidationError\n\n')
        for nodo in nodi:
            nome = nodo['nome']
            new.write('class ' + nome.replace(" ", "_").capitalize() + '(MyNode):\n')

            # Prendo tutte le chiavi composte da un sola proprietà del nodo, userò questa lista per mettere o meno
            # "unique" nella definizione dell'attributo
            list_simple_unique_node = []
            for sk in nodo['secondarykey']:
                if len(sk) == 1:
                    list_simple_unique_node.append(sk[0])

            # Defisisco una lista che conterrà la chiavi secondarie composte da più proprietà degli archi esaminati
            list_composite_unique_edge = []

            # Definisco il dizionario che conterra' i vincoli del nodo, la chiave è il nome della proprietà e il valore
            # sono i vincoli, li userò per sovrascrivere la funzione clear per la validazione dei campi
            vincoli = {}

            if not nodo['primaryKey']:
                new.write(' ' * 4 + "id_" + nome.replace(" ", "_") + " = MyIDField(auto_created=True, primary_key=True, serialize=False, "
                                                   "verbose_name='ID')\n")

            # new.write(' ' * 4 + "mynode_ptr = MyOneToOneField(auto_created=True, "
            #                 "on_delete=models.CASCADE, parent_link=True, to='app.MyNode', null = True)\n")

            # Definisco i campi in base alle proprietà del nodo che sto esaminando
            new.write(crea_proprieta(nodo['proprieta'], domini, list_simple_unique_node, nodo['primaryKey']))

            # Inserico gli intervalli della proprietà esaminata nei vincoli
            for prop in nodo['proprieta']:
                if len(prop['intervalli']) > 0:
                    vincoli[prop['nomeProp']] = prop['intervalli']
                for dom in domini:
                    if dom['nome'] == prop['dominio'] and dom['generico'] != 'enum':
                        for intervallo in dom['valori']:
                            vincoli[prop['nomeProp']].append(intervallo)

            # Esamino gli archi che hanno come estremo il nodo che sto definendo
            for arco in archi:
                if arco['nome'] not in archi_gia_esaminati:

                    # Esamino le relationship uno - uno, accorpo quindi la relationship nel nodo che sto
                    # definendo e aggiungo le proprietà dell'arco che sto esaminando
                    if (arco['molteplicita']['source'] == "0 - 1" or arco['molteplicita']['source'] == "1 - 1") and \
                            (arco['molteplicita']['target'] == "0 - 1" or arco['molteplicita']['target'] == "1 - 1"):

                        if arco['source']['nome'] == nome:
                            new.write(' ' * 4 + "edge_" + arco['target']['nome'].replace(" ", "_") + ' = ' +
                                      "MyRelationship('" + arco['target']['nome'].replace(" ", "_").capitalize() +
                                      "', model='" + arco['nome'].replace(" ", "_") + "', label='" + arco[
                                          'nome'].replace(" ", "_").upper() +
                                      "', cardinalitySource='" + arco['molteplicita']['source'] +
                                      "', cardinalityTarget='" + arco['molteplicita']['target'] +
                                      "', direction='OUTGOING')\n")
                        elif arco['target']['nome'] == nome:
                            new.write(' ' * 4 + "edge_" + arco['source']['nome'].replace(" ", "_") + ' = ' +
                                      "MyRelationship('" + arco['source']['nome'].replace(" ", "_").capitalize() +
                                      "', model='" + arco['nome'].replace(" ", "_") + "', label='" + arco[
                                          'nome'].replace(" ", "_").upper() +
                                      "', cardinalitySource='" + arco['molteplicita']['source'] +
                                      "', cardinalityTarget='" + arco['molteplicita']['target'] +
                                      "', direction='INCOMING')\n")

                        # Prendo tutte le chiavi composte da un sola proprietà dell'arco, userò questa lista per
                        # mettere o meno "unique" nella definizione dell'attributo
                        list_simple_unique_edge = []
                        for sk in arco['secondarykey']:
                            if len(sk) == 1:
                                list_simple_unique_edge.append(sk[0])

                        # Inserisco nella lista le chiavi secondarie composte da più attributi
                        for sk in arco['secondarykey']:
                            if len(sk) > 1:
                                list_composite_unique_edge.append(sk)

                        # Definisco la lista con i vincoli dei valori
                        for prop in arco['proprieta']:
                            if len(prop['intervalli']) > 0:
                                vincoli[prop['nomeProp']] = prop['intervalli']

                        # Definisco le proprietà per gli archi con molteplicità uno - uno accorpati nel nodo che sto
                        # esaminando
                        new.write(crea_proprieta(arco['proprieta'], domini, list_simple_unique_edge))

                        archi_gia_esaminati.append(arco['nome'])

                    # Esamino le relationship uno - molti ( e molti - uno), definisco la foreign key nel nodo che ha
                    # vincolo di molteplicita massima uno e aggiungo le proprietà dell'arco che sto esaminando
                    elif ((arco['molteplicita']['source'] == "0 - 1" or arco['molteplicita']['source'] == "1 - 1") and
                          (arco['molteplicita']['target'] == "0 - N" or arco['molteplicita']['target'] == "1 - N")) or \
                            ((arco['molteplicita']['target'] == "0 - 1" or arco['molteplicita'][
                                'target'] == "1 - 1") and
                             (arco['molteplicita']['source'] == "0 - N" or arco['molteplicita']['source'] == "1 - N")):

                        if arco['source']['nome'] == nome and (arco['molteplicita']['source'] == "0 - 1" or
                                                               arco['molteplicita']['source'] == "1 - 1"):

                            new.write(' ' * 4 + "edge_" + arco['target']['nome'].replace(" ", "_") + ' = ' +
                                      "MyRelationship('" + arco['target']['nome'].replace(" ", "_").capitalize() +
                                      "', model='" + arco['nome'].replace(" ", "_") + "', label='" + arco[
                                          'nome'].replace(" ", "_").upper() +
                                      "', cardinalitySource='" + arco['molteplicita']['source'] +
                                      "', cardinalityTarget='" + arco['molteplicita']['target'] +
                                      "', direction='OUTGOING')\n")

                        elif arco['target']['nome'] == nome and (arco['molteplicita']['target'] == "0 - 1" or
                                                                 arco['molteplicita']['target'] == "1 - 1"):

                            new.write(' ' * 4 + "edge_" + arco['source']['nome'].replace(" ", "_") + ' = ' +
                                      "MyRelationship('" + arco['source']['nome'].replace(" ", "_").capitalize() +
                                      "', model='" + arco['nome'].replace(" ", "_") + "', label='" + arco[
                                          'nome'].replace(" ", "_").upper() +
                                      "', cardinalitySource='" + arco['molteplicita']['source'] +
                                      "', cardinalityTarget='" + arco['molteplicita']['target'] +
                                      "', direction='INCOMING')\n")

                        # Prendo tutte le chiavi composte da un sola proprietà dell'arco, userò questa lista per
                        # mettere o meno "unique" nella definizione dell'attributo
                        list_simple_unique_edge = []
                        for sk in arco['secondarykey']:
                            if len(sk) == 1:
                                list_simple_unique_edge.append(sk[0])

                        # Inserisco nella lista le chiavi secondarie composte da più attributi
                        for sk in arco['secondarykey']:
                            if len(sk) > 1:
                                list_composite_unique_edge.append(sk)

                        # Definisco la lista con i vincoli dei valori
                        for prop in arco['proprieta']:
                            if len(prop['intervalli']) > 0:
                                vincoli[prop['nomeProp']] = prop['intervalli']

                        # Definisco le proprietà per gli archi con molteplicità uno - molti o molti - uno accorpati nel
                        # nodo che sto esaminando
                        new.write(crea_proprieta(arco['proprieta'], domini, list_simple_unique_edge))

                        archi_gia_esaminati.append(arco['nome'])

                    # Esamino le relationship molti - molti, definisco il campo ManyToManyField nel nodo che sto
                    # definendo passando a "through" il nome della relazione che sarà derivata dall'arco esaminato
                    elif ((arco['molteplicita']['source'] == "0 - N" or arco['molteplicita']['source'] == "1 - N") and
                          (arco['molteplicita']['target'] == "0 - N" or arco['molteplicita']['target'] == "1 - N")):

                        if arco['source']['nome'] == nome:
                            new.write(' ' * 4 + "edge_" + arco['nome'].replace(" ", "_") + ' = ' +
                                      "MyRelationship('" + arco['target']['nome'].replace(" ", "_").capitalize() +
                                      "', model='" + arco['nome'].replace(" ", "_").capitalize() + "', label='" + arco[
                                          'nome'].replace(" ", "_").upper() +
                                      "', cardinalitySource='" + arco['molteplicita']['source'] +
                                      "', cardinalityTarget='" + arco['molteplicita']['target'] +
                                      "', direction='OUTGOING')\n")

                        elif arco['target']['nome'] == nome:
                            new.write(' ' * 4 + "edge_" + arco['nome'].replace(" ", "_") + ' = ' +
                                      "MyRelationship('" + arco['source']['nome'].replace(" ", "_").capitalize() +
                                      "', model='" + arco['nome'].replace(" ", "_").capitalize() + "', label='" + arco[
                                          'nome'].replace(" ", "_").upper() +
                                      "', cardinalitySource='" + arco['molteplicita']['source'] +
                                      "', cardinalityTarget='" + arco['molteplicita']['target'] +
                                      "', direction='INCOMING')\n")

                        archi_gia_esaminati.append(arco['nome'])

            # Creo vincoli
            if bool(vincoli):
                new.write(crea_vincoli(vincoli, nodo['nome']))

            # Prendo tutte le chiavi secondarie composte da più attributi del nodo
            list_composite_unique_node = []
            for sk in nodo['secondarykey']:
                if len(sk) > 1:
                    list_composite_unique_node.append(sk)

            # Definisco la lista di tutte le chiavi secondarie composte che passerò a unique_together
            list_composite_unique = list_composite_unique_node + list_composite_unique_edge

            new.write("\n" + ' ' * 4 + "class Meta:\n")
            new.write(' ' * 8 + "unique_together" + ' = ' +
                      str(tuple(MyUtils.unique_to_tuple(list_composite_unique))) + "\n\n\n")

        for arco in archi:
            # Esamino gli archi con molteplicità molti - molti e genero una nuova relazione
            if ((arco['molteplicita']['source'] == "0 - N" or arco['molteplicita']['source'] == "1 - N") and
                    (arco['molteplicita']['target'] == "0 - N" or arco['molteplicita']['target'] == "1 - N")):

                vincoli = {}

                # Inserico gli intervalli della proprietà esaminata nei vincoli
                for prop in arco['proprieta']:
                    if len(prop['intervalli']) > 0:
                        vincoli[prop['nomeProp']] = prop['intervalli']
                    for dom in domini:
                        if dom['nome'] == prop['dominio'] and dom['generico'] != 'enum':
                            for intervallo in dom['valori']:
                                vincoli[prop['nomeProp']].append(intervallo)

                # Definisco una lista delle chiavi secondarie composta da un singolo attributo che userò per mettere o
                # meno unique
                list_simple_unique_edge = []
                for sk in arco['secondarykey']:
                    if len(sk) == 1:
                        list_simple_unique_edge.append(sk[0])

                nome = arco['nome'].replace(" ", "_")
                new.write('class ' + nome.capitalize() + '(MyEdge):\n')

                new.write(' ' * 4 + "id_" + nome.replace(" ", "_") + " = MyIDField(auto_created=True, "
                                                   "primary_key=True, serialize=False, verbose_name='ID')\n")
                # new.write(' ' * 4 + "myedge_ptr = MyOneToOneField(auto_created=True, null=True, "
                # "on_delete=models.CASCADE, parent_link=True, serialize=False, to='app.MyEdge')\n")

                new.write(' ' * 4 + arco['source']['nome'].replace(" ", "_") + ' = ' +
                          "MyRelationship('" + arco['source']['nome'].replace(" ", "_").capitalize() +
                          "', model='" + arco['nome'].replace(" ", "_") + "', label='" + arco['nome'].replace(" ",
                                                                                                              "_").upper() +
                          "', cardinalitySource='" + arco['molteplicita']['source'] +
                          "', cardinalityTarget='0 - 1', direction='OUTGOING')\n")

                new.write(' ' * 4 + arco['target']['nome'].replace(" ", "_") + ' = ' +
                          "MyRelationship('" + arco['target']['nome'].replace(" ", "_").capitalize() +
                          "', model='" + arco['nome'].replace(" ", "_") + "', label='" + arco['nome'].replace(" ",
                                                                                                              "_").upper() +
                          "', cardinalitySource='" + arco['molteplicita']['source'] +
                          "', cardinalityTarget='0 - 1', direction='INCOMING')\n")

                # Definisco i campi in base alle proprietà dell'arco che sto esaminando
                new.write(crea_proprieta(arco['proprieta'], domini, list_simple_unique_edge, arco['primaryKey']))

                if bool(vincoli):
                    new.write(crea_vincoli(vincoli, arco['nome']))

                list_composite_unique_edge = []
                for sk in arco['secondarykey']:
                    if len(sk) > 1:
                        list_composite_unique_edge.append(sk)

                new.write("\n" + ' ' * 4 + "class Meta:\n")
                new.write(' ' * 8 + "unique_together" + ' = ' +
                          str(tuple(MyUtils.unique_to_tuple(list_composite_unique_edge))) + "\n\n\n")

                new.write('\n')
                new.write('\n')

    os.remove(os.path.join(project_folder, 'app', 'models.py'))
    os.rename(os.path.join(project_folder, 'app', 'new.py'), os.path.join(project_folder, 'app', 'models.py'))

    subprocess.Popen(
        ['python', 'manage.py', 'makemigrations', '--settings=' + current_project.name_project + '.settings'],
        cwd=current_project.folder)
    print("Creazione models")
    time.sleep(5)
    print("Migrazione models")
    subprocess.Popen(['python', 'manage.py', 'migrate', '--settings=' + current_project.name_project + '.settings'],
                     cwd=current_project.folder)

    return render(request, 'graphEd/graphEd.html')


def create_schema_NEO4J(request):
    global main_folder, project_folder
    print("Creazione schema Neo4J")
    data = MyUtils.json_loads_byteified(request.body)
    nome = data['nomeProgetto']
    nodi = data['nodes']
    archi = data['links']
    domini = data['domini']
    project_folder = os.path.join(main_folder, nome)
    with open(os.path.join(project_folder, 'app', 'new.py'), 'w') as new:
        new.write('from __future__ import unicode_literals\n\n')
        new.write('# Create your models here.\n\n')
        new.write('from MyStructuresNeo4J import *\n\n\n')

        # Esamino gli archi e vi aggiungo le rispettive proprietà
        for arco in archi:
            nome = arco['nome']
            new.write('class ' + nome.capitalize() + '(MyEdge):\n')

            if len(arco['proprieta']) != 0:
                new.write(crea_proprieta(arco['proprieta'], domini, []))
            else:
                new.write(' ' * 4 + "pass\n")

            new.write("\n\n")

        for nodo in nodi:
            nome = nodo['nome']
            new.write('class ' + nome.capitalize() + '(MyNode):\n')

            if nodo['primaryKey'] == []:
                new.write(' ' * 4 + "id_" + nome + " = MyIDField()\n")

            # Defisisco una lista che conterrà la chiavi secondarie composte da più proprietà degli archi esaminati
            list_composite_unique_edge = []

            # Definisco le proprietà degli attributi del nodo
            new.write(crea_proprieta(nodo['proprieta'], domini, [], nodo['primaryKey']))

            # Per ogni arco che ha il nodo esaminato come estremo aggiungo la proprietà relationship
            for arco in archi:

                if arco['source']['nome'] == nome:
                    new.write(' ' * 4 + arco['nome'] + ' = ' +
                              "MyRelationship('" + arco['target']['nome'].capitalize() + "', " +
                              "model=" + arco['nome'].capitalize() + ", label='" + arco['nome'].upper() +
                              "', cardinalitySource='" + arco['molteplicita']['source'] +
                              "', cardinalityTarget='" + arco['molteplicita']['target'] +
                              "', direction='OUTGOING')\n")

                elif arco['target']['nome'] == nome:
                    new.write(' ' * 4 + arco['nome'] + ' = ' +
                              "MyRelationship('" + arco['target']['nome'].capitalize() + "', "
                                                                                         "model=" + arco[
                                  'nome'].capitalize() + ", label='" + arco['nome'].upper() +
                              "', cardinalitySource='" + arco['molteplicita']['source'] +
                              "', cardinalityTarget='" + arco['molteplicita']['target'] +
                              "', direction='INCOMING')\n")

            new.write("\n\n")

    os.remove(os.path.join(project_folder, 'app', 'models.py'))
    os.rename(os.path.join(project_folder, 'app', 'new.py'), os.path.join(project_folder, 'app', 'models.py'))

    # subprocess.Popen(['python', 'manage.py', 'makemigrations', '--settings=' + current_project.name_project + '.settings'], cwd=current_project.folder)
    # subprocess.Popen(['python', 'manage.py', 'migrate', '--settings=' + current_project.name_project + '.settings'], cwd=current_project.folder)

    return render(request, 'graphEd/graphEd.html')


def crea_proprieta(proprieta, domini, list_unique, pk=None):
    res = ''
    for prop in proprieta:
        for dom in domini:
            if prop['dominio'] == dom['nome']:
                if dom['generico'] == 'int':
                    if prop['default'] is None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyIntegerField(primary_key=True, default=" + \
                                  dom['default'] + ")\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyIntegerField(unique=True, default=" + \
                                  dom[
                                      'default'] + ", notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyIntegerField(default=" + str(
                                dom['default']) + ", notNull=" + str(prop['notNull']) + ")\n"
                    else:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyIntegerField(primary_key=True, default=" + \
                                  prop['default'] + ")\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyIntegerField(unique=True, default=" + \
                                  prop[
                                      'default'] + ", notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyIntegerField(default=" + \
                                  prop[
                                      'default'] + ", notNull=" + str(prop['notNull']) + ")\n"

                elif dom['generico'] == 'float':
                    if prop['default'] is None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyFloatField(primary_key=True, default=" + \
                                  dom[
                                      'default'] + ")\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyFloatField(unique=True, default=" + \
                                  dom[
                                      'default'] + ", notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyFloatField(default=" + dom[
                                'default'] + ", notNull=" + str(prop['notNull']) + ")\n"
                    else:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyFloatField(primary_key=True, default=" + \
                                  prop['default'] + ")\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyFloatField(unique=True, default=" + \
                                  prop[
                                      'default'] + ", notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyFloatField(default=" + \
                                  prop[
                                      'default'] + ", notNull=" + str(prop['notNull']) + ")\n"

                elif dom['generico'] == 'string':
                    if prop['default'] != None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyStringField(primary_key=True, default='" + \
                                  prop['default'] + "')\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ",
                                                                           "_") + " = MyStringField(unique=True, default='" + \
                                  prop[
                                      'default'] + "', notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyStringField(default='" + \
                                  prop[
                                      'default'] + "', notNull=" + str(prop['notNull']) + ")\n"
                    elif prop['default'] is None and dom['default'] is not None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyStringField(primary_key=True, default='" + \
                                  dom['default'] + "')\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyStringField(unique=True, default='" + dom[
                                'default'] + "', notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyStringField(default='" + dom[
                                'default'] + "', notNull=" + str(prop['notNull']) + ")\n"
                    else:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyStringField(primary_key=True')\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyStringField(unique=True, notNull=" + str(
                                prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyStringField(notNull=" + str(
                                prop['notNull']) + ")\n"

                elif dom['generico'] == 'bool':
                    if prop['default'] is None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyBooleanField(primary_key=True, default=" + \
                                  dom['default'] + ")\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyBooleanField(unique=True, default=" + dom[
                                'default'] + ", notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyBooleanField(default=" + dom[
                                'default'] + ", notNull=" + str(prop['notNull']) + ")\n"
                    else:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyBooleanField(primary_key=True, default=" + \
                                  prop['default'] + ")\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyBooleanField(unique=True, default=" + prop[
                                'default'] + ", notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyBooleanField(default=" + prop[
                                'default'] + ", notNull=" + str(prop['notNull']) + ")\n"

                elif dom['generico'] == 'date':
                    if prop['default'] is not None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(primary_key=True, default='" + \
                                  prop['default'] + "')\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(unique=True, default='" + prop[
                                'default'] + "', notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(default='" + prop[
                                'default'] + "', notNull=" + str(prop['notNull']) + ")\n"
                    elif prop['default'] is None and dom['default'] is not None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(primary_key=True, default='" + dom[
                                'default'] + "')\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(unique=True, default='" + dom[
                                'default'] + "', notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(default='" + dom[
                                'default'] + "', notNull=" + str(prop['notNull']) + ")\n"
                    else:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(primary_key=True)\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(unique=True, notNull=" + str(
                                prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop['nomeProp'].replace(" ", "_") + " = MyDateField(notNull=" + str(
                                prop['notNull']) + ")\n"

                elif dom['generico'] == 'enum':
                    if prop['default'] is not None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(primary_key=True, choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ", default='" + prop['default'] + "')\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(unique=True, choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ", default='" + prop['default'] + "', notNull=" + str(
                                prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ", default='" + prop['default'] + "', notNull=" + str(
                                prop['notNull']) + ")\n"
                    elif prop['default'] is None and dom['default'] is not None:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(primary_key=True, choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ", default='" + dom['default'] + "')\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(unique=True, choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ", default='" + dom['default'] + "', notNull=" + str(
                                prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ", default='" + dom['default'] + "', notNull=" + str(
                                prop['notNull']) + ")\n"
                    else:
                        if pk == prop['nomeProp']:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(primary_key=True, choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ")\n"
                        elif prop['nomeProp'] in list_unique:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(unique=True, choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ", notNull=" + str(prop['notNull']) + ")\n"
                        else:
                            res = res + ' ' * 4 + prop[
                                'nomeProp'].replace(" ", "_") + " = MyStringField(choices=" + MyUtils.choise_to_string(
                                dom['valori']) + ", notNull=" + str(prop['notNull']) + ")\n"
    return res


def crea_vincoli(vincoli, nome):
    res = '\n' + ' ' * 4 + 'def clean(self):\n'
    for prop in vincoli.keys():
        for int in vincoli[prop]:
            res = res + ' ' * 8 + "if not(" + int.replace("value", "self." + prop) + "):\n"
            res = res + " " * 12 + "raise ValidationError('Violazione vincolo: " + int.replace("value", prop) + "')\n"
    res = res + "\n" + ' ' * 4 + "def save(self, *args, **kwargs):\n"
    res = res + ' ' * 8 + "self.clean()\n"
    res = res + ' ' * 8 + "return super(" + nome.capitalize() + ", self).save(**kwargs)\n"
    return res
