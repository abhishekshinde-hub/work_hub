
from fastapi import FastAPI
from db_connection import Base, get_db,engine
from workhub.auth import models
app = FastAPI()

Base.metadata.create_all(bind=engine)

