import sqlite3
from modal import asgi_app
from .common import DB_PATH, VOLUME_DIR, app, fastapi_app, volume

@app.function(volumes={VOLUME_DIR: volume})

def init_db():
    volume.reload()
    conn = sqlite3.connect(str(DB_PATH))

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS writing (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)")

    conn.commit()
    conn.close()
    volume.commit()

@app.function(volumes={VOLUME_DIR: volume})

@asgi_app()
def fastapi_entrypoint():
  init_db.remote()
  return fastapi_app

@fastapi_app.post("/writing/{writing_id}")

def main():
    conn = sqlite3.connect("writing.db")

