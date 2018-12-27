from django.db import models
from django.utils import timezone
from jsonfield import JSONField


# Create your models here.


class Project(models.Model):

    DBMS = (('MySQL', 'MySQL'), ('SQLite', 'SQLite'), ('Neo4j', 'Neo4j'))

    name_project = models.CharField(unique=True, max_length=200)
    name_db = models.CharField(max_length=200, null=True)
    dbms = models.CharField(max_length=6, choices=DBMS, null=True)
    description = models.TextField(blank=True, null=True)
    port = models.IntegerField()
    folder = models.FilePathField()
    created_date = models.DateField(default=timezone.now, auto_now=False)
    graph = JSONField(null=True)

    #p = Project(name_project='Manager', name_db='ManagerDB', dbms='SQLite', description='Database del manager del sistema', port=8000, folder='C:\\Users\\Utente\\Desktop\\django\\serverdb\\manager', graph=None)


    def __str__(self):
        return self.name_project
