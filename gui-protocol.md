# Zappy: Protocole GUI-Serveur

## Introduction

Ceci est la spécification du protocol GUI-Serveur utilisé pour ce projet.  
Tous les messages émis seront formattés en JSON valide (excepté pour la phase d'authentification auprès du server).  
Lors des phases de description des requêtes-réponses:
```
--> [message]: Décrit un message client vers server (Requête).
<-- [message]: Décrit un message serveur vers client (Réponse).
```

## Authentification

Suite à la connection, les premiers échanges se passeront comme décrit ci-contre pour s'authentifier en tant que GUI:
```
<-- WELCOME
--> gui
<-- ok
```

Suite à ces commandes, le serveur est prêt à recevoir des requêtes JSON pour le GUI.

## Commandes

Les commandes reconnus par le serveur sont les suivantes.

### Taille de la map

Requête:
```json
{
    "command": "map-size"
}
```

Réponse:
```json
{
    "type": "response",
    "response-type": "map-size",
    "size": {
        "width": 10,
        "height": 20
    }
}
```

### Liste d'entités

Requête:
```json
{
    "command": "entities"
}
```

Réponse:
```json
{
    "type": "response",
    "response-type": "entities",
    "data": [
        {
            "type": "food",
            "data": [
                {"x": 1, "y": 2},
                {"x": 4, "y": 2},
                {"x": 5, "y": 5},
                {"x": 5, "y": 3}
            ]
        },
        {
            "type": "sibur",
            "data": [
                {"x": 10, "y": 20},
                {"x": 9, "y": 5}
            ]
        },
        {
            "type": "player",
            "data": [
                {
                    "id": 1,
                    "team": "Eo",
                    "facing": "N",
                    "level": 8,
                    "pos": {
                        "x": 1,
                        "y": 2
                    }
                }
            ]
        }
    ]
}
```

### Contenu d'une case

Requête:
```json
{
    "command": "tile",
    "pos": {
        "x": 4,
        "y": 10
    }
}
```

Réponse:
```json
{
    "type": "response",
    "response-type": "tile",
    "pos": {
        "x": 4,
        "y": 10
    },
    "data": [
        {
            "type": "food",
            "amount": 4
        },
        {
            "type": "sibur",
            "amount": 10
        },
        {
            "type": "player",
            "ids": [ 4, 5, 6 ]
        }
    ]
}
```

## Événements

Des événements peuvent surgir à n'importe quel moment et le serveur enverra les informations liés à ces événements à tous les GUIs connectés.

### Mouvement de joueur

```json
{
    "type": "event",
    "event-type": "player-move",
    "data": {
        "id": 2,
        "pos": {
            "x": 10,
            "y": 11
        }
    }
}
```

### Incantation

Début d'incantation:
```json
{
    "type": "event",
    "event-type": "incantation-start",
    "data": {
        "id": 2,
        "current-level": 4
    }
}
```

Succés de l'incantation:
```json
{
    "type": "event",
    "event-type": "incantation-success",
    "data": {
        "id": 2,
        "current-level": 5
    }
}
```

Echec de l'incantation:
```json
{
    "type": "event",
    "event-type": "incantation-fail",
    "data": {
        "id": 2,
        "current-level": 4
    }
}
```

## Erreurs

Lors d'une erreur, une réponse spéciale sera renvoyé au client par le serveur.

### Erreur de syntaxe

```json
{
    "type": "error",
    "error-type": "syntax-error"
}
```

### Erreur de commande

```json
{
    "type": "error",
    "error-type": "command-error"
}
```
