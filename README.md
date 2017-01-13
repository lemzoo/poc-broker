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
