"""
Pydantic model (schemas) for reading data from API and creating data.
"""
from pydantic import BaseModel, UUID4, Field
from datetime import date, datetime
from enum import Enum


# Enum for drug-drug interaction severity
class IssueSeverity(str, Enum):
    HARMLESS = 'harmless'
    MODERATE = 'moderate'
    SEVERE = 'severe'
    DEADLY = 'deadly'


# Enum for drug-drug interaction chance of happening, probability ranges.
class ProbabilityType(str, Enum):
    UNLIKELY = 'unlikely'  # 0.0-0.15
    LOW = 'low'  # 0.16-0.40
    EVEN_CHANCE = 'even_chance'  # .41-.60
    LIKELY = 'likely'   # .61-.90
    CERTAIN = 'certain'  # .91-1.0


class Prescription(BaseModel):
    dosage: str
    dose_type: str
    patient_id: UUID4
    provider_id: UUID4
    medication_id: int
    id: int

    class Config:
        orm_mode = True


class Patient(BaseModel):
    given_name: str
    family_name: str
    dob: date
    height_ins: int
    weight_lbs: int
    id: UUID4
    prescriptions: list[Prescription] = []

    class Config:
        orm_mode = True


class ProviderBase(BaseModel):
    given_name: str
    family_name: str
    org: str
    user_name: str


class ProviderCreate(ProviderBase):
    password: str


class Provider(ProviderBase):
    id: UUID4
    prescriptions: list[Prescription] = []

    class Config:
        orm_mode = True


class Medication(BaseModel):
    name: str
    common_name: str
    manufacturer: str
    id: int

    class Config:
        orm_mode = True


class Issue(BaseModel):
    issue_severity: IssueSeverity
    issue_warning: str
    probability_type: ProbabilityType
    probability: float
    id: int
    interaction_id: int

    class Config:
        orm_mode = True


class Interaction(BaseModel):
    medication1: int
    medication2: int
    id = int
    issues: list[Issue] = []

    class Config:
        orm_mode = True


class MedicationRequestBase(BaseModel):
    patient_id: UUID4
    provider_id: UUID4
    request_dt: Field(default_factory=datetime.utcnow)
    new_medication: int


class MedicationRequestCreate(MedicationRequestBase):
    pass


class MedicationRequest(MedicationRequestBase):
    id: int
    current_medication_ids: str

    class Config:
        orm_mode = True


class PredictionBase(BaseModel):
    interaction_issues_list: str
    medication_request_id: int
    request_dt: Field(default_factory=datetime.utcnow)


class PredictionCreate(PredictionBase):
    pass


class Prediction(PredictionBase):
    id: int

    class Config:
        orm_mode = True
