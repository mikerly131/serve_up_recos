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

    # allergies = relationship("Allergy", back_populates="patient")
    # conditions = relationship("Condition", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")


# Provider are the users, they prescribe 0 to many medications for a patient.
# MVP: Adding username and password for now, might make users table separate at some point.
class Provider(Base):
    __tablename__ = "providers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    given_name = Column(String(length=40))
    family_name = Column(String(length=60))
    org = Column(String(length=50))


# Prescription has a patient, provider, medication, medication instance, dosage, dose type, frequence, duration
# MVP: Just using the medication, not market instance?
# Future: Want to use market available instances of medication (dose amount, type already set not user entered)
class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.rxcui"))
    medication_name = Column(String(length=100))
    market_med_id = Column(Integer, ForeignKey('market_medications.id'))
    brand_name = Column(String)
    dose_amount = Column(String)
    enternal_route = Column(String)
    frequency = Column(String)
    duration = Column(String)
    patient_id = Column(String, ForeignKey("patients.id"))
    provider_id = Column(String, ForeignKey("providers.id"))


# Medications are used in 0 to many prescriptions (maybe just reference, see MVP note)
# MVP: My idea is this table is for the generic medication concept, not manufactured instances of it.
#      The interaction data I can source is for the concept, doesn't take dose / enternal type into account.
class Medication(Base):
    __tablename__ = "medications"

    rxcui = Column(Integer, primary_key=True, index=True)
    generic_name = Column(String(length=100))

    market_instances = relationship("MarketMedication", back_populates="medications")


# Without having to serialize or use NoSQL, can store 0 to many manufactured instances of a medication.
# This provides the details of the prescribable market instances of a medication.
# MVP: Issues sourcing this data, may not use for MVP -> prescription to medication only.
class MarketMedication(Base):
    __tablename__ = "market_medications"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey('medications.rxcui'))
    brand_name = Column(String)


# Interactions limited to 2 medications, not market instances (Data sourcing issues)
# Interaction has 1 to Many issues, and each issue has a risk level and severity.
# This is essentially my "mocked" AI/ML model predictions and/or its training data at some point.
# I think I need a 2 tuples for each interaction of 2 meds -> order of med1 and med2 can change in request (fixable?)
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    medication1 = Column(Integer, ForeignKey('medications.rxcui'))
    medication2 = Column(Integer, ForeignKey('medications.rxcui'))
    issue_description = Column(String)

#    issues = relationship('Issue', back_populates='interactions')


# MVP: Ditching this idea since can't source severity or probability data
# Issue belongs to an interaction, 1 to many issues per an interactions.
# Interactions with 0 issues don't have records.
# Can't find severity data (need to go across sources, don't have similar ids for meds, names not searchable)
# Can't find probability data (not finding sources, academic papers maybe)
# class Issue(Base):
#     __tablename__ = "issues"
#
#     id = Column(Integer, primary_key=True, index=True)
#     interaction_id = Column(Integer, ForeignKey('interactions.id'))
#     issue_severity = Column(String, nullable=True)
#     issue_warning = Column(String)
#     probability = Column(Float)
#     probability_type = Column(String, nullable=True)
#
#     __table_args__ = (
#         CheckConstraint('probability >= 0.0 AND probability <= 1.0', name='check_risk_probability_range'),
#     )


# Medication Request is for one patient, by one provider, at a specific time, and considers all existing prescriptions
# It prescribes one new medication and market instance of it.
# MVP: Might only use the generic medications, don't have time to source and clean market instances.
class MedicationRequest(Base):
    __tablename__ = "medication_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    provider_id = Column(String, ForeignKey("providers.id"))
    request_dt = Column(DateTime, default=datetime.utcnow)
    current_medication_ids = Column(String)
    new_medication = Column(Integer, ForeignKey('medications.id'))
    med_name = Column(String)
    new_market_med = Column(Integer, ForeignKey('market_medications.id'))
    brand_name = Column(String)
    dose_amount = Column(String)
    enternal_route = Column(String)
    frequency = Column(String)
    duration = Column(String)

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
# MVP: Not going to use this for MVP.
# class Prediction(Base):
#     __tablename__ = "predictions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     medication_request_id = Column(Integer, ForeignKey('medication_requests.id'))
#     interaction_issues_list = Column(Text)
#     request_dt = Column(DateTime, default=datetime.utcnow)
