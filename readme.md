# Business Application API

Welcome to the Business Application API! 

## 1. Installation

### 1.1 Creer votre environnement de développement 

```bash
python -m venv ourenv

### 1.2 Activer votre environnement de développement 

#### ON LINUX
```bash
source ourenv/bin/activate

#### ON WINDOWS
.\ourenv\Scripts\activate

### 1.3 Installer les dépendences à l'aide de la commande suivante  

```bash
pip install -r requirements.txt

## 2. Configurations

### 2.1 Créer votre base de données

### 2.2 Créer un fichier .env à la racine et respecter le modèle du fichier .env.example

### 2.3 Générer les migrations 

```bash 
alembic revision --autogenerate -m "Nom de votre migration"

### 2.4 Appliquer les migrations

```bash
alembic upgrade head

## 3 Lancer le projet 

```bash
uvicorn main:app --reload