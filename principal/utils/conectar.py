from pymongo import MongoClient
from django.conf import settings


def conectar_db():
    cliente = MongoClient(
        settings.MONGODB_CONFIG["HOST"], settings.MONGODB_CONFIG["PORT"]
    )
    db = cliente[settings.MONGODB_CONFIG["DB_NAME"]]
    coleccion = db["trabajos"]
    return coleccion
