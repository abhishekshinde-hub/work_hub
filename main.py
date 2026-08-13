
from fastapi import FastAPI
from workhub.admin.routers import admin_power
from workhub.db_connection import Base,engine
from workhub.auth import models
from workhub.auth.router import user_auth
from workhub.user_profile import user_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
"Include => When we make router then we have to run router files b'coz over main logic and code into the router thats why we include router in here so that when we run main over other file will be run"
app.include_router(user_auth.router)
app.include_router(admin_power.router)
app.include_router(user_router.router)


