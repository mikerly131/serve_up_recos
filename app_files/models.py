"""
Models for the application.
Classes: Patients, Providers, Prescriptions, Medications, Medication Requests, Interactions, Issues, Predictions
Each class is commented below with details about its data and relationships.
"""
import uuid
from sqlalchemy import (Column, ForeignKey, Integer, String,
                        UUID, Date, Float, CheckConstraint, DateTime, Text)
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date, datetime


# Patient has an id, given name, family name and 0 to many prescriptions
# Patients also have some arbitrary data for filling out the screen - dob, height(inches), weight(pounds)
class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    given_name = Column(String(length=40))
    family_name = Column(String(length=60))
    dob = Column(Date, default=date(1970, 1, 1))
    height_ins = Column(Integer)
    weight_lbs = Column(Integer)
    prescriptions = relationship("Prescription", back_populates="patient")


# Provider has an id, given name, family name, organization, and 0 to many prescriptions ordered
# These are also the "users" of the application.  Adding username and password for now, might make users table.
class Provider(Base):
    __tablename__ = "providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    given_name = Column(String(length=40))
    family_name = Column(String(length=60))
    org = Column(String(length=50))

    prescriptions = relationship("Prescription", back_populates="provider")


# Prescription has a patient, provider, medication, dosage, dose type
class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"))
    dosage = Column(String)
    dose_type = Column(String)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"))

    patient = relationship("Patient", back_populates="prescriptions")
    provider = relationship("Provider", back_populates="prescriptions")


# Medications have a name, manufacturer, and used in 0 to many prescriptions
# TODO - Do I reference the name or common name in the Prescriptions table to make reading simpler?
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100))
    common_name = Column(String(length=40))
    manufacturer = Column(String(length=50))


# Interactions have two or more medications, one or more issues, and each issue has a risk level and severity.
# This is essentially my "mocked" AI/ML model predictions and/or its training data at some point.
# This design might force me to enter 2 interactions where med 1 and med 2 are swapped...yikes
# TODO - Would a back reference to medications make accessing the data easier?
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    medication1 = Column(Integer, ForeignKey('medications.id'))
    medication2 = Column(Integer, ForeignKey('medications.id'))

    issues = relationship('Issue', back_populates='interaction')


# Issue belongs to an interaction
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
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"))
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
