import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from .database import engine
from . import models
import time
import json
import os
from .routers import cohort, milestone, school, student
from sqlalchemy import event

from .database import Base
import uvicorn

models.Base.metadata.create_all(bind=engine)

file_path = os.path.join(
                    os.path.dirname(__file__), 
                    'tags_metadata.json'
                    )
metadata_file = open(file_path, 'r')
metadata = json.load(metadata_file)
metadata_file.close()


app = FastAPI(docs_url="/documentation", openapi_tags=metadata)

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='directed', 
            user='postgres', 
            password='',
            cursor_factory=RealDictCursor
            )
        cursor = conn.cursor()
        print('Database connection successful!')
        break

    except Exception as error:
        print('Connecting to database failed')
        print('Error', error)
        time.sleep(2)

@app.on_event("startup")
def configure():
    Base.metadata.create_all(bind=engine)

app.include_router(school.router)
app.include_router(cohort.router)
app.include_router(student.router)
app.include_router(milestone.router)


