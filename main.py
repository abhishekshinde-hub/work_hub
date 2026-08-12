
from fastapi import FastAPI
from db_connection import Base, get_db,engine
from workhub.auth import models
from workhub.auth.router import user_auth
app = FastAPI()
Base.metadata.create_all(bind=engine)
"Include => When we make router then we have to run router files b'coz over main logic and code into the router thats why we include router in here so that when we run main over other file will be run"
app.include_router(user_auth.router)


