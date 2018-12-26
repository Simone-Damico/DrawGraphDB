# File con le url per il reindirizzamento alle view per le query

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^popola/$', views.popola, name='popola'),

    url(r'^get_nodes/$', views.get_nodes, name='get_nodes'),
    url(r'^count_nodes/$', views.count_nodes, name='count_nodes'),
    url(r'^order_by_nodes/$', views.order_by_nodes, name='order_by_nodes'),
    url(r'^sub_set_nodes/$', views.sub_set_nodes, name='sub_set_nodes'),
    url(r'^get_distinct_nodes/$', views.get_distinct_nodes, name='get_distinct_nodes'),
    url(r'^get_max_value_nodes/$', views.get_max_value_nodes, name='get_max_value_nodes'),
    url(r'^get_min_value_nodes/$', views.get_min_value_nodes, name='get_min_value_nodes'),

    url(r'^get_edges/$', views.get_edges, name='get_edges'),
    url(r'^count_edges/$', views.count_edges, name='count_edges'),
    url(r'^order_by_edges/$', views.order_by_edges, name='order_by_edges'),
    url(r'^sub_set_edges/$', views.sub_set_edges, name='sub_set_edges'),
    url(r'^get_max_value_edges/$', views.get_max_value_edges, name='get_max_value_edges'),
    url(r'^get_min_value_edges/$', views.get_min_value_edges, name='get_min_value_edges'),
]