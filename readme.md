#Business Application API

Welcome to the Business Application API! 

## 1. Installation

###1.1 Creer votre environnement de développement 

#####This python project use python 3.11.5


```bash
python -m venv env_name
```

###1.2 Activer votre environnement de développement 

####ON LINUX

```bash
source env_name/bin/activate
```

####ON WINDOWS

```bash
.\env_name\Scripts\activate
```

###1.3 Installer les dépendences à l'aide de la commande suivante  

```bash
pip install -r requirements.txt
```

##2. Configurations

###2.1 Créer un fichier .env à la racine et respecter le modèle du fichier .env.example

###2.2 Créer votre base de données du nom mis dans votre fichier .env

###2.3 Générer les migrations 

```bash 
alembic revision --autogenerate -m "Nom de votre migration"
```

###2.4 Appliquer les migrations

```bash
alembic upgrade head
```

##3 Lancer le projet 

```bash
uvicorn main:app --reload --host 0.0.0.0  
``` 