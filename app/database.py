import psycopg2
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .configure import settings


SQLALCHEMY_DATABASE_URI =f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

#while True:
#    try:
#        conn = psycopg2.connect(host ='localhost', dbname='fastapi1', user='postgres', password='Starforge46321SWAN#', cursor_factory=RealDictCursor)
#        cur = conn.cursor()
#        print("Database connection was successfull")
#        break
#    except Exception as error:
#        print("Connection with database failed")
#        print("Error:", error)
#        time.sleep(2)
#        count+=1
#        if (count >=1000):
#            print("Complete failure you are")
#            break


#def find_posts(id):
#    for p in my_posts:
#        if p["id"] == id:
#            return p
#    
#def find_ind_post(id):
#    for i, p in enumerate(my_posts):
#        if p["id"] == id:
#            return i
