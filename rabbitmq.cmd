# http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html

# Starting/Stopping the RabbitMQ server

# To start the server:
$ sudo rabbitmq-server

# You can also run it in the background by adding the
# -detached option (note: only one dash):
$ sudo rabbitmq-server -detached

# Never use kill (kill(1)) to stop the RabbitMQ server,
# but rather use the rabbitmqctl command:
$ sudo rabbitmqctl stop

###############################################################
################### Setting up RabbitMQ #######################
###############################################################
# To use Celery we need to create a RabbitMQ user,
# a virtual host and allow that user access to that virtual host:

$ sudo rabbitmqctl add_user myuser mypassword
$ sudo rabbitmqctl add_vhost myvhost
$ sudo rabbitmqctl set_user_tags myuser mytag
$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

# Details about RabbitMQ
current node details:
- node name: 'rabbitmq-cli-86@lamine'
- home dir: /var/lib/rabbitmq
- cookie hash: t95PIM9vnvqAuUzA4/pYgg==

Useful link : http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html#broker-instructions

