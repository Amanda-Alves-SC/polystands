import os

config = {
    "host": os.getenv("MYSQLHOST"),
    "user": os.getenv("MYSQLUSER"),
    "password": os.getenv("MYSQLPASSWORD"),
    "database": os.getenv("MYSQLDATABASE"),
    "port": int(os.getenv("MYSQLPORT"))
}

print("HOST:", os.getenv("MYSQLHOST"))
print("USER:", os.getenv("MYSQLUSER"))
print("DB:", os.getenv("MYSQLDATABASE"))
print("PORT:", os.getenv("MYSQLPORT"))

key = os.getenv("GOOGLE_MAPS_API_KEY")