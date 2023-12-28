"""
File to populate db with necessary data.
DB and tables need to exist first (start then stop app if needed)
Then, run this script before restarting.  Only do this 1x unless DB is lost.

"""
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import insert, create_engine
from app_files.models import Patient, Medication, Prescription, Interaction, Issue
import json


# Table population order: Patient, Medication, Prescription, Interaction, Issue
# To populate Prescription Table with patient prescriptions for initial load, create with NULL provider id explicit
def populate_data(db: Session):

    # Insert patients
    patients = [
        Patient(given_name="Jonathan", preferred_name="Jon", family_name="Dough", dob=date(1981, 7, 21),
                height_ins=181, weight_lbs=159, bio_gender="Male", gender_identity="Male"),
        Patient(given_name="Jane", preferred_name="Jane", family_name="Dough", dob=date(1984, 1, 30),
                height_ins=175, weight_lbs=109, bio_gender="Female", gender_identity="Female"),
        Patient(given_name="Robert", preferred_name="Bob", family_name="Wehadababyitsaboy", dob=date(1991, 10, 3),
                height_ins=191, weight_lbs=229, bio_gender="Male", gender_identity="Male"),
        Patient(given_name="Anika", preferred_name="Annie", family_name="Shorsdottir", dob=date(1963, 5, 17),
                height_ins=184, weight_lbs=128, bio_gender="Female", gender_identity="Zee"),
        Patient(given_name="Deshaun", preferred_name="Deshaun", family_name="Popper", dob=date(1979, 7, 11),
                height_ins=198,weight_lbs=203, bio_gender="Male", gender_identity="Male"),
        Patient(given_name="Sanjay", preferred_name="Sanjay", family_name="Durgadin", dob=date(1975, 4, 28),
                height_ins=201, weight_lbs=188, bio_gender="Male", gender_identity="Male"),
        Patient(given_name="Avni", preferred_name="Avni", family_name="Lui", dob=date(2001, 8, 14),
                height_ins=168, weight_lbs=101, bio_gender="Male", gender_identity="Female")

    ]
    db.add_all(patients)
    db.commit()

    # Insert medications
    medications = [
        Medication(name="Tylenol", rxcui=)
    ]
    db.add_all(prescriptions)
    db.commit()

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
