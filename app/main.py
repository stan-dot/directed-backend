from fastapi import FastAPI
from .database import engine
from . import models
import json
import os
from .routers import cohort, milestone, school, student
from .database import Base


#create all tables according to models
#models.Base.metadata.create_all(bind=engine)

file_path = os.path.join(
                    os.path.dirname(__file__), 
                    'tags_metadata.json'
                    )
metadata_file = open(file_path, 'r')
metadata = json.load(metadata_file)
metadata_file.close()

app = FastAPI(docs_url="/documentation", openapi_tags=metadata)

@app.get('/')
def root():
    return {'message': "DirectEd Database"}


app.include_router(school.router)
app.include_router(cohort.router)
app.include_router(student.router)
app.include_router(milestone.router)


