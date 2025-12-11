import os
import json
from datetime import datetime

# Dossier logs situé un niveau au-dessus de src/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "events.log")

# Créer le dossier logs s'il n'existe pas
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(data: dict) -> None:
    """
    Enregistre un événement dans logs/events.log au format JSON.
    Ajoute automatiquement un timestamp UTC.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        **data
    }

    with open(LOG_FILE, "a", encoding="utf-8") as logfile:
        logfile.write(json.dumps(entry) + "\n")
