"""
Create, Read, Update, Delete actions defined to interact with the database
For this project, might only need Create and Read
"""
from fastapi import HTTPException

from sqlalchemy.orm import Session
from . import models, schemas


# Functions that I think I'll need for my program (MVP)
#  I want providers to be able to register (create) and login (create for session?, update?)
#  I want a provider who is signed in to pick a workflow (1 to start) and a patient (read, handful to start)
#  I want to display patient information in the workflow (read)
#       I want to include current prescriptions and medications (helper functions, read)
#       I want to display a list of medications to prescribe (handful to start, read)
#  I want to allow a medication prescription to be requested (create,  create a prediction as well)
#  I want to display the predicted interactions (create predictions returns for the create medication request)
#       I want to include the 3 most severe issues, ordered by severity (read)
#  I want to allow a medication order to be placed after predictions are served (2nd screen, mock/dummy no DB for now)
#  Note:  orders being saved to DB and updating patient prescriptions will be in phase 2.


# Function to register providers (users) of the application
def register_provider(db: Session, provider: schemas.ProviderCreate):
    fake_hashed_password = provider.password + "notreallyhashed"
    db_provider = models.Provider(given_name=provider.given_name, hashed_password=fake_hashed_password,
                                  family_name=provider.family_name, org=provider.org, user_name=provider.user_name)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


# Function to login providers (users) of the application, raises exceptions for bad user and invalid password
def login_provider(db: Session, user_name: str, password: str):
    fake_hashed_password = password + "notreallyhashed"
    provider = db.query(models.Provider).filter(models.Provider.user_name == user_name).first()
    if provider:
        if provider.hashed_password == fake_hashed_password:
            return provider
        else:
            raise HTTPException(status_code=401, detail="Invalid password")
    else:
        raise HTTPException(status_code=401, detail="Provider not found")


# Function to provide a list of patients for the provider to select for an encounter
def get_patients():
    pass


# Function to select a single user for one of the mocked encounter workflows
def set_workflow_patient():
    pass


# Function to get all the data to populate an encounter workflow form
def get_workflow_data():
    get_patient_details()
    get_prescriptions()
    get_medications()
    pass


# Helper function to get patient details to display in the encounter workflow form
def get_patient_details():
    pass


# Helper function to
def get_prescriptions():
    pass


# Helper function to get selectable medications for a medication request workflow
def get_medications():
    pass


# Function to make a medication request on form submission
def make_medication_request():
    pass


# Helper function for medication request to return predictions of drug-drug interactions (ddi)
def make_ddi_predictions():
    pass


# Helper function for the make_ddi_predictions (ddi) to return top 3 issues by severity
def get_ddi_issues():
    pass


# Function to place a medication order for the medication request workflow
def make_medication_order():
    pass

