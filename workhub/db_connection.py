from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base
"""It's a url for db connection the take db_name,driver_name,username,password and port ,host ,db_name"""
db_url = 'postgresql+psycopg2://workhub:radheradhe@localhost:5432/workhub_db'

engine = create_engine(db_url)

"""sessionmaker => It comes from sqlalchemy.orm that help us to make connection to the db whenever we want it's like a db manager that handle db connection and disconnection it giver seprate connetion for each and every request """

Base = declarative_base()
"""Base => It's like a box whenever we make  models in project. that time we send this Base it args of the class of that models Base take a snapshot of all tables .
we can understand it's llike a box where we put over all model when we run base.create.meta it's directly make the table in database ."""
Session_local = sessionmaker(bind=engine)
def get_db() :
    with Session_local() as db : 
        yield db