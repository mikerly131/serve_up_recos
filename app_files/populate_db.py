"""
File to populate db with necessary data.
For now, the DB and tables need to exist first (start then stop app if needed)
Then, run this script before restarting.  Only do this 1x unless DB is lost.
"""
from datetime import date

from sqlalchemy.orm import Session
from models import Patient, Prescription, Medication, Interaction, Issue


# Table population order:
# Patient
# Medication
# Prescription
# Interaction
# Issue

# To populate Prescription Table with patient prescriptions for initial load, create with NULL provider id explicit
def populate_data(db: Session):

    # Insert patients
    patients = [
        Patient(given_name="John", family_name="Dough", dob=date(1981, 7, 21), height_ins=184, weight_lbs=159),
        Patient(given_name="Jane", family_name="Dough", dob=date(1984, 1, 30), height_ins=175, weight_lbs=109),
        Patient(given_name="Bob", family_name="Wehadababyitsaboy", dob=date(1991, 10, 3), height_ins=191, weight_lbs=190),
        Patient(given_name="Anika", family_name="Testersdottir", dob=date(1963, 5, 17), height_ins=184, weight_lbs=128)
    ]
    db.add_all(patients)
    db.commit()

    # Insert medications
    medications = [
        Medication()
    ]
    db.add_all(medications)
    db.commit()

    # Insert prescriptions
    prescriptions = [
        Prescription()
    ]
    db.add_all(prescriptions)
    db.commit()

    # Insert prescriptions
    interactions = [
        Interaction()
    ]
    db.add_all(interactions)
    db.commit()

    # Insert issues
    issues = [
        Issue()
    ]
    db.add_all(issues)
    db.commit()



if __name__ == "__main__":
    with get_db() as db:
        populate_data(db)