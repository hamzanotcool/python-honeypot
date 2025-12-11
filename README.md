Python Honeypot — HTTP & Fake SSH (Low Interaction)
===================================================

Ce projet est un honeypot pédagogique développé en Python.
Il permet d’observer, enregistrer et analyser des tentatives d’accès
malveillantes en simulant deux services :

1. Un honeypot HTTP amélioré (fausse page de login)
2. Un faux SSH interactif (FakeShell) inspiré de Cowrie

Ce projet ne simule aucun protocole réel et n’exécute aucune commande système.
Il s’agit d’un honeypot low-interaction 100% sécurisé.

---------------------------------------------------
1. Fonctionnalités
---------------------------------------------------

Honeypot HTTP :
- Page login factice
- Logs JSON (IP, username, password, User-Agent)
- Plusieurs endpoints : / /login /admin /api
- Port configurable via config.json

Faux SSH (FakeShell) :
- Port 2222
- Simulation login/password
- Fausse console interactive
- Commandes simulées : ls, cat, exit
- Faux système de fichiers virtuel
- Logs JSON des commandes et connexions
- Multi-clients via threads

---------------------------------------------------
2. Architecture du projet
---------------------------------------------------

my-honeypot/

│

├── src/

│   ├── honeypot_http.py

│   ├── fake_ssh.py

│   └── logger.py

│

├── logs/

│   └── events.log

│

├── config.json

├── README.txt

└── requirements.txt


---------------------------------------------------
3. Installation et exécution
---------------------------------------------------

Lancer le honeypot HTTP :
    cd src
    python3 honeypot_http.py

Lancer le faux SSH :
    cd src
    python3 fake_ssh.py

Connexion SSH simulée :
    nc localhost 2222

---------------------------------------------------
4. Auteur
---------------------------------------------------

Projet développé par EL MOUSSAOUI Hamza.
Étudiant en cybersécurité, en recherche d’alternance.
