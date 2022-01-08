# FileManagementSystem

* to run a django web server - `python manage.py runserver`

* to make a new web application - `python manage.py startapp 'appName' `

* whenever you create a new applicatio, add it to the settings.py --> INSTALLED_APPS >> `appname.apps.AppnameConfig`

* create virtual environment venv - `pip install virtualenv`  `virtualenv [directory]` 
* use for this project (I do always)
* and pip install django and mysqlclient (requirements.txt) in the venv
* to load all static files do `python manage.py runserver --insecure` with `debug=False` in settings.py