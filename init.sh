#!/bin/bash

read -p "Entrez votre nom d'utilisateur: " USERNAME
read -p "Entrez votre mot de passe: " PASSWORD

pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8000
