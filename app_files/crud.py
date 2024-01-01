"""
Create, Read, Update, Delete actions defined to interact with the database
For this project's MVP, might only need Create and Read
"""
from uuid import UUID

from sqlalchemy.orm import Session, joinedload
from . import models, schemas


# Function to register providers (users) of the application
def register_provider(db: Session, provider: schemas.ProviderCreate):
    fake_hashed_password = provider.password + "notreallyhashed"
    db_provider = models.Provider(given_name=provider.given_name, hashed_password=fake_hashed_password,
                                  family_name=provider.family_name, org=provider.org, user_name=provider.user_name)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


# Helper function to check if a user_name for a provider is already taken
def get_provider(db: Session, user_name: str):
    a_provider = db.query(models.Provider).filter(models.Provider.user_name == user_name).first()
    return a_provider


# Helper function to get the provider id from the supplied provider user_name
def get_provider_id(db: Session, user_name: str):
    a_provider = db.query(models.Provider).filter(models.Provider.user_name == user_name).first()
    provider_id = a_provider.id
    return provider_id


# Function to login providers (users) of the application, raises exceptions for bad user and invalid password
def login_provider(db: Session, user_name: str, password: str):
    fake_hashed_password = password + "notreallyhashed"
    provider = db.query(models.Provider).filter(models.Provider.user_name == user_name).first()
    if provider:
        if provider.hashed_password == fake_hashed_password:
            return provider
        else:
            return "Password"
    else:
        return "User"


# Function to provide a list of patients for the provider to select for an encounter
def get_patients(db: Session):
    patients = db.query(models.Patient).all()
    return patients


# Function to get all the data to populate an encounter workflow form
def get_workflow_data(db: Session, patient_id: str):
    patient_details = get_patient_details(db, patient_id)
    medications = get_medications(db)
    workflow_data = [patient_details, medications]
    return workflow_data


# Helper function to get patient details to display in the encounter workflow form
def get_patient_details(db: Session, patient_id: str):
    patient_details = db.query(models.Patient).options(joinedload(models.Patient.prescriptions)).filter(models.Patient.id == patient_id).first()
    return patient_details


# Helper function to get selectable medications for a medication request workflow
def get_medications(db: Session):
    medications = db.query(models.Medication).all()
    return medications

# UNNECESSARY - patient_details returns prescriptions objects
# def get_prescriptions(db: Session, prescriptions):
#     prescription_details = []
#     for prescription in prescriptions:
#         prescription_info = db.query(models.Prescription).filter(models.Prescription.id == prescription.id).first()
#         prescription_details.append(prescription_info)
#     return prescription_details


# Function to make a medication request on form submission
def make_medication_request(db: Session, patient_id: str, user_name: str, new_medication, med_name, new_market_med,
                            brand_name, dose_amount, enternal_route, frequency, duration):
    provider_id = get_provider_id(db, user_name)

    # Create a new MedicationRequest
    medication_request = models.MedicationRequest(
        patient_id=patient_id,
        provider_id=provider_id,
        new_medication=new_medication,
        med_name=med_name,
        new_market_med=new_market_med,
        brand_name=brand_name,
        dose_amount=dose_amount,
        enternal_route=enternal_route,
        frequency=frequency,
        duration=duration
    )

    db.add(medication_request)
    medication_request.set_current_medication_ids(db)
    db.commit()
    db.refresh(medication_request)
    return medication_request.id


# Function to get the drug-drug interaction issues for a medication request
def serve_ddi_issues(db: Session, mr_id: int):
    # get the medication reqeust
    mr = db.query(models.MedicationRequest).filter(models.MedicationRequest.id == mr_id).first()
    # loop through each current medications
    current_meds = list(map(int, mr.current_medication_ids.split(",")))
    issue_list = []
    for med in current_meds:
        # get issues for med and new_med
        issues = get_ddi_issue(db, mr.new_medication, med)
        # if there are issues, get the issues and put them in the issue list
        if issues:
            for issue in issues:
                issue_list.append(issue)
    return issue_list


# Helper function for the serve_ddi_issues to return top 3 issues by severity
def get_ddi_issue(db: Session, med1: int, med2: int):
    interaction = db.query(models.Interaction).filter(models.Interaction.medication_1 == med1,
                                                      models.Interaction.medication_2 == med2).first()
    if interaction:
        ddi_issue = interaction.issue_description
        return ddi_issue


# Helper function for medication request to return predictions of drug-drug interactions (ddi)
# def make_ddi_predictions(db: Session, mr_id: int):
#     pass


# Function to place a medication order for the medication request workflow
# def make_medication_order():
#     pass
