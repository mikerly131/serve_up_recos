"""
Pydantic model (schemas) for reading data from API and creating data.
The classes (tables) for the db are given schemas so the app knows how to handle them in API request/response.
Notice:  Only providers, medication requests and predictions can be created by API.
            and predictions is only included incase I find an AI/ML as API to hit and get predictions from.
"""
from pydantic import BaseModel, UUID4, Field
from datetime import date, datetime
from enum import Enum


# Enum for drug-drug interaction severity
# class IssueSeverity(str, Enum):
#     HARMLESS = 'harmless'
#     MODERATE = 'moderate'
#     SEVERE = 'severe'
#     DEADLY = 'deadly'


# Enum for drug-drug interaction chance of happening, probability ranges.
# class ProbabilityType(str, Enum):
#     UNLIKELY = 'unlikely'  # 0.0-0.15
#     LOW = 'low'  # 0.16-0.40
#     EVEN_CHANCE = 'even_chance'  # .41-.60
#     LIKELY = 'likely'   # .61-.90
#     CERTAIN = 'certain'  # .91-1.0


class Prescription(BaseModel):
    id: int
    medication_id: int
    medication_name: str
    market_med_id: int
    brand_name: str
    dose_amount: str
    enternal_route: str
    frequency: str
    duration: str
    patient_id: str
    provider_id: str

    class Config:
        orm_mode = True


class Patient(BaseModel):
    id: str
    given_name: str
    preferred_name: str
    family_name: str
    dob: date
    height_ins: int
    weight_lbs: int
    bio_gender: str
    gender_identity: str
    prescriptions: list[Prescription] = []

    class Config:
        orm_mode = True


class Provider(BaseModel):
    given_name: str
    family_name: str
    org: str
    user_name: str


class ProviderCreate(Provider):
    password: str


class ProviderRead(Provider):
    id: str

    class Config:
        orm_mode = True


class MarketMedication(BaseModel):
    id: int
    medication_id: int
    brand_name: str

    class Config:
        orm_mode = True


class Medication(BaseModel):
    rxcui: int
    generic_name: str
    market_instances: list[MarketMedication] = []

    class Config:
        orm_mode = True


# MVP:  Ditching idea, no sourcing for issue data
# class Issue(BaseModel):
#     issue_severity: IssueSeverity
#     issue_warning: str
#     probability_type: ProbabilityType
#     probability: float
#     id: int
#     interaction_id: int
#
#     class Config:
#         orm_mode = True


class Interaction(BaseModel):
    id: int
    medication1: int
    medication2: int
    # issues: list[Issue] = []

    class Config:
        orm_mode = True


class MedicationRequest(BaseModel):
    id: int
    patient_id: str
    provider_id: str
    request_dt: datetime = Field(default_factory=datetime.utcnow)
    current_medication_ids: str
    new_medication: int
    med_name: str
    new_market_med: int
    brand_name: str
    dose_amount: str
    enternal_route: str
    frequency: str
    duration: str

    class Config:
        orm_mode = True


# MVP: No AI integrations, ditching for MVP
# class PredictionBase(BaseModel):
#     interaction_issues_list: str
#     medication_request_id: int
#     request_dt: datetime = Field(default_factory=datetime.utcnow)
#
#
# class PredictionCreate(PredictionBase):
#     pass
#
#
# class Prediction(PredictionBase):
#     id: int
#
#     class Config:
#         orm_mode = True
