"""
Models for the application.
Classes: Patients, Providers, Prescriptions, Medications, Medication Requests, Interactions, Issues, Predictions
Each class is commented below with details about its data and relationships.
"""
import uuid
from sqlalchemy import (Column, ForeignKey, Integer, String,
                        Date, Float, CheckConstraint, DateTime, Text)
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date, datetime


# Patient have 0 to many prescriptions, allergies and conditions (MVP: prescriptions)
class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    given_name = Column(String(length=40))
    preferred_name = Column(String(length=40))
    family_name = Column(String(length=60))
    dob = Column(Date, default=date(1900, 1, 1))
    height_ins = Column(Integer)
    weight_lbs = Column(Integer)
    bio_gender = Column(String(length=20))
    gender_identity = Column(String(length=20))

    # Will I even have time to make use of these relationships?
    # allergies = relationship("Allergy", back_populates="patient")
    # conditions = relationship("Condition", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")


# Provider are the users, they prescribe 0 to many medications for a patient.
# These are also the "users" of the application.  Adding username and password for now, might make users table.
class Provider(Base):
    __tablename__ = "providers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    given_name = Column(String(length=40))
    family_name = Column(String(length=60))
    org = Column(String(length=50))


# Prescription has a patient, provider, medication, dosage, dose type
class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"))
    medication_name = Column(String(length=100))
    dose_amount = Column(String)
    dose_type = Column(String)
    frequency = Column(String)
    duration = Column(String)
    patient_id = Column(String, ForeignKey("patients.id"))
    provider_id = Column(String, ForeignKey("providers.id"))

    patient = relationship("Patient", back_populates="prescriptions")


# Medications have a name, manufacturer, and used in 0 to many prescriptions
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100))
    rxcui = Column(Integer, unique=True)
    app_type = Column(String(length=20))
    amount = Column(String)


# Interactions limited to 2 meds, one or more issues, and each issue has a risk level and severity (READ).
# This is essentially my "mocked" AI/ML model predictions and/or its training data at some point.
# This design might force me to enter 2 interactions where med 1 and med 2 are swapped...yikes
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    medication1 = Column(Integer, ForeignKey('medications.rxcui'))
    medication2 = Column(Integer, ForeignKey('medications.rxcui'))

    issues = relationship('Issue', back_populates='interaction')


# Issue belongs to an interaction (READ)
class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey('interactions.id'))
    issue_severity = Column(String, nullable=False)
    issue_warning = Column(String)
    probability = Column(Float)
    probability_type = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint('probability >= 0.0 AND probability <= 1.0', name='check_risk_probability_range'),
    )

    interaction = relationship('Interaction', back_populates='issues')


# Medication Request is for one patient, by one provider, at a specific time, and considers all existing prescriptions
class MedicationRequest(Base):
    __tablename__ = "medication_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    provider_id = Column(String, ForeignKey("providers.id"))
    request_dt = Column(DateTime, default=datetime.utcnow)
    current_medication_ids = Column(String)
    new_medication = Column(Integer, ForeignKey('medications.id'))

    # Get the medication IDs from prescriptions for patients at the time of the request
    def set_current_medication_ids(self, session):
        # Query prescriptions for the patient
        prescriptions = (
            session.query(Prescription.medication_id)
            .filter(Prescription.patient_id == self.patient_id)
            .all()
        )

        # Save the medication IDs as a comma-separated string
        medication_ids = [prescription.medication_id for prescription in prescriptions]
        self.current_medication_ids = ",".join(medication_ids)

    # Get the medication IDs for a medication request as a list of ints - ids type in medication table
    def get_current_medication_ids(self):
        if self.current_medication_ids:
            return [int(medication_id) for medication_id in self.current_medication_ids.split(",")]
        else:
            return []


# A prediction is for one medication reqeust and has 0 to many interactions it returns
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    medication_request_id = Column(Integer, ForeignKey('medication_requests.id'))
    interaction_issues_list = Column(Text)
    request_dt = Column(DateTime, default=datetime.utcnow)
