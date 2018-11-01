from django.conf.urls import url
from django.views.generic import ListView

from models import Project
from . import views

urlpatterns = [
    url(r'^$', views.grafo, name='grafo'),
    url(r'^create_schema_SQL/$', views.create_schema_SQL, name='create_schema_SQL'),
    url(r'^create_schema_NEO4J/$', views.create_schema_NEO4J, name='create_schema_NEO4J'),
    url(r'^new_project/$', views.new_project, name='new_project'),
    url(r'^change_project_data/$', views.change_project_data, name='change_project_data'),
    url(r'^show_projects/$', views.show_projects, name='show_projects'),
    url(r'^openProject/$', views.open_project, name='open_project'),
    url(r'^delete_project/$', views.delete_project, name='delete_project'),
    url(r'^save_graph/$', views.save_graph, name='save_graph'),
]
