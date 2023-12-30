"""
Second file to run for setup:
1. Ensure DB has been created and patients, medications loaded.  Kill the app after, just in case.
2. Grab the patient ids and insert them into the prescriptions.
3. Run this script to load the prescriptions.
4. Restart the app.  Should be ready to rock.
"""
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import insert, create_engine, select, column
from app_files.models import Prescription
import json


# Insert prescriptions
# I'll need the patient ids in order to do this.
def populate_prescriptions(db: Session):
    prescriptions = [
        Prescription(medication_id=1, medication_name="", dosage="", dose_type="", patient_id="", provider_id=None)
    ]
    db.add_all(prescriptions)
    db.commit()


if __name__ == "__main__":
    db_url = 'sqlite:///./sql_app.db'
    engine = create_engine(db_url)
    my_db = Session(bind=engine)
    populate_prescriptions(my_db)