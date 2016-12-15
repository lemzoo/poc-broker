# This file contains some basics command to laucnh the rabbit-mq and Celery

1. Create virtualenv
$ virtualenv -p /your/python/directory name_of_your_venv

2. Install dependencies by using pip
$ pip install celery

3. Launch Rabbit-mq server

4. Launch celery server
celery -A tasks worker --loglevel=info
tasks est le nom de la tache associé à l'instance de Celery

5. Launch your worker
nom_du_worker.deley(arg1, arg2, arg3)
