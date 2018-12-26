# DrawGraphDB

This is a work in progress project. 

With DrawGraphDB you can create and manage a graph to model your scenario of interest. 
DrawGraphDB will then transform the graph into a database automatically, which you can then query.  
It's possible to create relational databases (SQLite or MySQL) or graph databases (Neo4j). More to come!

### Frontend
The frontend is made with JavaScriptm using:

* AngularJS 1.6 (to migrate to 1.7);
* Angular Material 1.1.4 (to migrate to 1.1.11).

### Backend
The backend is made in Python 3.7 with Django.

Use the requirements.txt file to install the needed libraries, otherwise install with pip:

* Django==2.1.4
* django-jsonfield==1.0.1
* neomodel==3.3.0


