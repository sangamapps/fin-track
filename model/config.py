from os import environ

MONGO_DB_URL = "mongodb+srv://prod-king:itsprodking@cluster0.gaeyh.mongodb.net"
MONGO_DB_NAME = "fin-track" if int(environ.get("DEBUG", 0)) == 0 else "fin-track-beta"
