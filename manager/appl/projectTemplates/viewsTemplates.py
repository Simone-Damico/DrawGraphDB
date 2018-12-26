import json

from django.core import serializers
from django.http import HttpResponse


# Views per il popolamento - DA CAMBIARE SICURAMENTE -
def popola(request):
    pop = json.load(request.body)
    print 'Populating Database...'
    print '----------------------'
    for deserialized_object in serializers.deserialize('json', pop):
        deserialized_object.save()
        print 'Saved: ', deserialized_object
    return HttpResponse()

############################################################


# Views per tutti i nodi
def get_nodes(request):
    cls = json.load(request.body)['cls']
    data = cls.getEdges()
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def count_nodes(request):
    cls = json.load(request.body)['cls']
    data = cls.countNodes()
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def order_by_nodes(request):
    cls = json.load(request.body)['cls']
    param = json.loads(request.body)['param']
    data = cls.orderByParam(param)
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def sub_set_nodes(request):
    cls = json.load(request.body)['cls']
    offset = json.loads(request.body)['param']
    limit = json.loads(request.body)['param']
    data = cls.orderByParam(offset, limit)
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def get_distinct_nodes(request):
    cls = json.load(request.body)['cls']
    params = json.loads(request.body)['params']
    data = cls.orderByParam(params)
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def get_max_value_nodes(request):
    cls = json.load(request.body)['cls']
    params = json.loads(request.body)['params']
    data = cls.orderByParam(params).first()
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def get_min_value_nodes(request):
    cls = json.load(request.body)['cls']
    params = json.loads(request.body)['params']
    data = cls.orderByParam(params).last()
    return HttpResponse(data, content_type='graphEd/graphEd.html')


# Views per tutti gli archi
def get_edges(request):
    cls = json.load(request.body)['cls']
    data = cls.getEdges()
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def count_edges(request):
    cls = json.load(request.body)['cls']
    data = cls.countEdges()
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def order_by_edges(request):
    cls = json.load(request.body)['cls']
    param = json.loads(request.body)['param']
    data = cls.orderByParam(param)
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def sub_set_edges(request):
    cls = json.load(request.body)['cls']
    offset = json.loads(request.body)['param']
    limit = json.loads(request.body)['param']
    data = cls.orderByParam(offset, limit)
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def get_max_value_edges(request):
    cls = json.load(request.body)['cls']
    params = json.loads(request.body)['params']
    data = cls.orderByParam(params).first()
    return HttpResponse(data, content_type='graphEd/graphEd.html')


def get_min_value_edges(request):
    cls = json.load(request.body)['cls']
    params = json.loads(request.body)['params']
    data = cls.orderByParam(params).last()
    return HttpResponse(data, content_type='graphEd/graphEd.html')

########################################################################

