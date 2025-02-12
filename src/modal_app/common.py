import pathlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modal import App, Image, Secret, Volume

DB_FILENAME = "writing.db"
VOLUME_DIR = "/cache-vol"
DB_PATH = pathlib.Path(VOLUME_DIR, DB_FILENAME)
volume = Volume.from_name("sqlite-db-volume", create_if_missing=True)

image = Image.debian_slim().pip_install_from_pyproject("pyproject.toml")
secrets = Secret.from_dotenv()

app = App(name="writing_app", secrets=[secrets], image=image)

fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


