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

# To delete all the message on the queue
$ sudo rabbitmqctl purge_queue queue_name

# To list all the queue and see process
$ sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged

# List the bindings
$ sudo rabbitmqctl list_bindings

# Activate rabbitmq plugins
$ sudo rabbitmq-plugins enable rabbitmq_management

# Acces to the interface
http://localhost:15672/
username 1 : guest
password 1 : guest

username 2 : admin
password 2 : root

username 3 : manager
password 3 : root

# interface admin ref
https://www.rabbitmq.com/management.html


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

https://www.rabbitmq.com/tutorials/tutorial-five-python.html
