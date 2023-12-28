"""
File to populate db with necessary data.

1. Get the patient ids that prescriptions will be created for.
2. Get the medication ids that prescriptions will be created for.
3. Create Prescription objects to insert into the DB.
"""
from datetime import date
from sqlalchemy import insert, create_engine
from sqlalchemy.orm import Session
from app_files.main import get_db
from app_files.models import Patient, Medication, Prescription, Interaction, Issue
import json


# Table population order:
# Patient
# Medication
# Prescription
# Interaction
# Issue

# To populate Prescription Table with patient prescriptions for initial load, create with NULL provider id explicit
def populate_data(db: Session):


    # (Phase 2) Insert medications from sh_nm_drugs.json in drug_data
    # At some point use proper path, and import os if needed
    # with open('/Users/mike/projects/serve_up_recos/drug_data/sh_nm_drugs.json', 'r') as file:
    #     drug_data = json.load(file)
    #
    # for drug in drug_data:
    #     db.execute(
    #         insert(Medication).values(name=drug['name'], rxcui=drug['rxcui'])
    #     )
    #
    # db.commit()

    # Insert prescriptions
    prescriptions = [
        Prescription(medication_id=, medication_name="", dosage="", dose_type="", patient_id="", provider_id=None)
    ]
    db.add_all(prescriptions)
    db.commit()

    # Insert interactions, a reference table that links two medications.
    # For now, insert the pair twice, once in each order.
    interactions = [
        Interaction(medication1= , medication2= )
    ]
    db.add_all(interactions)
    db.commit()

    # Insert issues for the interactions.
    # For now insert it under each interaction ID for a medication pair - so once with each ID.
    # Severities:  harmless, moderate, severe, deadly
    # Probability Types: unlikely, low, even_chance, likely, certain
    issues = [
        Issue(interaction_id= , issue_severity="severe" , issue_warning=" ", probability=0.0, probability_type="unlikely")
    ]
    db.add_all(issues)
    db.commit()

if __name__ == "__main__":
    db_url = 'sqlite:///./sql_app.db'
    engine = create_engine(db_url)
    my_db = Session(bind=engine)
    populate_data(my_db)
