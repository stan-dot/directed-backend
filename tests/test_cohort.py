from app import schemas
from .setup import client, session

def test_root(client):
    response = client.get("/")
    assert response.json() == {"message":"Hello home."}
    assert response.status_code == 200

def test_create_cohort(client):
    response = client.post(
        "/cohorts/", json={"name": "test cohort", "description": "about test cohort"}
    )
    new_cohort = schemas.Cohort(**response.json())
    assert new_cohort.name == "test cohort"
    assert response.status_code == 201
    response = client.get(
        "/cohorts/test%20cohort"
    )
    assert response.json() == {"name": "test cohort", "description": "about test cohort"}
    assert response.status_code == 200


