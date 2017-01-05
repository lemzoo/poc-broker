
# https://www.rabbitmq.com/tutorials/tutorial-two-python.htmlhttps://www.rabbitmq.com/tutorials/tutorial-two-python.html

`Durable = True`  permet de persister la queue pour que les messages ne soient
pas supprimer lorsque rabbitmq crache



`delivery_mode = 2` make message persistent



`prefetch = 1` : Permet de repartir la charge des worker de maniere equitable.
