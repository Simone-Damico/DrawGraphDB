from django.urls import path

from . import views

urlpatterns = [
    path('', views.grafo, name='grafo'),
    path('create_schema_SQL/', views.create_schema_SQL, name='create_schema_SQL'),
    path('create_schema_NEO4J/', views.create_schema_NEO4J, name='create_schema_NEO4J'),
    path('new_project/', views.new_project, name='new_project'),
    path('change_project_data/', views.change_project_data, name='change_project_data'),
    path('show_projects/', views.show_projects, name='show_projects'),
    path('openProject/', views.open_project, name='open_project'),
    path('delete_project/', views.delete_project, name='delete_project'),
    path('save_graph/', views.save_graph, name='save_graph'),
]
