# Guide d'installation Rabbit MQ

## Installation Rabbit MQ (Debian, Ubuntu)
```
1. echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list

2. wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

3. sudo apt-get update

4. sudo apt-get install rabbitmq-server
```
Source : https://www.rabbitmq.com/install-debian.html

## Configuration Rabbit MQ
```
cd /etc/rabbitmq/
sudo wget https://raw.githubusercontent.com/rabbitmq/rabbitmq-server/master/docs/rabbitmq.config.example
sudo mv rabbitmq.config.example rabbitmq.config
```

Retirer le commentaire à la ligne 58 et ajouter guest à la ligne des users
```
sudo vi rabbitmq.config
```
 {loopback_users, ["guest"]},
```

Retirer le commentaire de la ligne 95 et ajouter 'PLAIN', 'AMQPLAIN' (Attention à la virgule à retirer)
```
  {auth_mechanisms, ['PLAIN', 'AMQPLAIN', 'EXTERNAL']}
```

Firewall peut empecher la communication entre les noeuds et les outils CLI. Verifier que les ports suivant soient ouverts:

- 4369 (epmd)
- 5672, 5671 (AMQP 0-9-1 and 1.0 without and with TLS)
- 25672. Ce port utilisé par la distribution Erlang pour la communication entre les nœuds et les outils CLI est alloué à partir d'une plage dynamique (limitée à un seul port par défaut, calculé en tant que port AMQP + 20000). Voir le guide de mise en réseau pour plus de détails.
- 15672 (Si mangement-plugin est activé voir plus bas)
- 61613, 61614 (si STOMP est activé)
- 1883, 8883 (if MQTT est activé)
Il est possible de configurer RabbitMQ sur différents ports et interfaces réseau spécifiques.

## Installation Rabbit MQ Management

1. sudo rabbitmq-plugins enable rabbitmq_management

2. http://localhost:15672/

3. Connecter vous avec le login et password par defaut guest/guest


## Gestion du Rabbit MQ

Affiche le statut du broker
```
sudo rabbitmqctl status
```

Stoppe le noeud Erlang sur lequel RabbitMQ s'execute
```
sudo rabbitmqctl stop
```

Demarre l'application RabbitMQ
```
sudo rabbitmqctl start_app
```

Stoppe l'application RabbitMQ
```
sudo rabbitmqctl stop_app
```

Pour plus d'information sur les commande voir le manuel:

https://www.rabbitmq.com/man/rabbitmqctl.1.man.html


# POC Broker Rabbit-MQ

1. Verifier le fonctionnement FIFO de Rabbit-mq : Par défaut, rabbit-mq utilise le fonctionnement FIFO

2. Création des fils dynamiques : Le client utilisé peut créer la file (queue)

3. La distrubitivité de rabbit-mq : Le fait de repartir la charge sur N noeuds

4. L'interface d'administration : Déportation de l'administrateur

5. Sauvegarde/Edition de message dans la base Mongo.


## Fonctionnalités du Broker existant


## FIFO

Oui, mais attention : si on a plusieurs files, les tâches qui doivent être FIFO doivent être envoyées dans la même file (tuto 4, Routing).

Donc on doit bien définir l'ordre partiel sur l'ensemble des tâches, et implementer un routeur avec les rêgles correspondantes

Solution : Faire une queue dossier

## Creation de file dynamique

Oui, rabbit-mq est capable de créer de queues dynamiquement tant que y'a de la mémoire dans la machine.

Autre point à démontrer : que fait-on en cas d'erreur dans une file ?

- Comment on peut arrêter / suspendre le traitement de la file.
- Comment pouvoir retraiter le message après une correction de connecteur et ou du message par exemple ?
- Un genre de fonction handleError ?

## Distributivité / disponnibilité

Pas besoin de répartir la charge pour les workers. Comment éviter un SPOF sur le RabbitMQ pour s'assurer que les événements envoyés par le back ne disparaissent pas.

Normallement RabbitMQ est fait pour, pas de risque de ce côté mais à bien confirmer (trouver une référence qui le montre). Si un noeud tombe, est-ce qu'on perd des événements ?

Write Concern ?


## Déporter l'interface d'administration

- Il existe une API HTTP, qui permet d'avoir accès à la plupart des ressources rabbitmq (exchanges, channels, users, vhosts, permissions).

On pourrait lister plus précisément des cas d'utilisation qu'on avoir pour pouvoir valider que l'API HTTP perment des les implémenter?


## Sauvegarde / Edition de messages dans la base Mongo

Pour pouvoir modifier un message en erreur par exemple, voir plus haut.

## Fonctionnalités existantes

- Générer des messages
- Les distribuer à des acteurs
- Avoir une queue de messages FIFO par acteur
- Quand un message traité est en erreur, toute la queue est bloquée automatiquement jusqu'à ce qu'une correction soit validée.
- Une interface d'administration qui perment de mettre en pause et de relancer les queues, de visualiser / modifier les messages (écriture de JSON à la main), les annuler, les relancer.

Un événement : ce que déclenche le backend (`event.py`). L'événement n'est pas persisté.
Le backend définit des abonnements à ces évennements (`event_handler.py`), et génère un message presisté pour chaque abonné.


## Références

Les tutos RabbitMQ :
- <https://www.rabbitmq.com/getstarted.html>
