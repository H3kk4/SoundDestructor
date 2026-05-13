#!/bin/bash
# Environnement Python
ENV=./.venv

if [ -d "$ENV" ]; then
    echo "Environnement Python déjà existant"
else
    echo "Création d'un environnement Python"
    python3 -m venv .venv
fi

source .venv/bin/activate
sudo chown -R "$USER":"$USER" .venv

pip install -r requirement.txt

# Bibliothèque tiers
sudo apt-get install libportaudio2