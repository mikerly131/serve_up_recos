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
# Make sure prescriptions.json includes the patient IDs.
def populate_prescriptions(db: Session):

    with open('/Users/mike/projects/serve_up_recos/drug_data/prescriptions.json', 'r') as file:
        prescriptions = json.load(file)

    for med in prescriptions:
        db.execute(
            insert(Prescription).values(medication_id=med['medication_id'], medication_name=med['medication_name'], market_med_id=med['market_med_id'],
                                        brand_name=med['brand_name'], dose_amount=med['dose_amount'], enternal_route=med['enternal_route'],
                                        frequency=med['frequency'], patient_id=med['patient_id'], provider_id=med['provider_id'])
        )

    db.commit()


if __name__ == "__main__":
    db_url = 'sqlite:///../sql_app.db'
    engine = create_engine(db_url)
    my_db = Session(bind=engine)
    populate_prescriptions(my_db)