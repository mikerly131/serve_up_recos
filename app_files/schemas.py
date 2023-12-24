"""
Pydantic model (schemas) for reading data from API and creating data.
"""
from pydantic import BaseModel, UUID4
from datetime import date
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


class PrescriptionBase(BaseModel):
    dosage: str
    dose_type: str


class PrescriptionCreate(PrescriptionBase):
    patient_id: UUID4
    provider_id: UUID4
    medication_id: int


class Prescription(PrescriptionBase):
    id: int

    class Config:
        orm_mode = True


class PatientBase(BaseModel):
    given_name: str
    family_name: str
    dob: date
    height_ins: int
    weight_lbs: int


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: UUID4
    prescriptions: list[Prescription] = []

    class Config:
        orm_mode = True


class ProviderBase(BaseModel):
    given_name: str
    family_name: str
    org: str


class ProviderCreate(ProviderBase):
    password: str


class Provider(ProviderBase):
    id: UUID4
    user_name: str
    prescriptions: list[Prescription] = []

    class Config:
        orm_mode = True


class MedicationBase(BaseModel):
    name: str
    common_name: str
    manufacturer: str


class MedicationCreate(MedicationBase):
    pass


class Medication(MedicationBase):
    id: int

    class Config:
        orm_mode = True


class IssueBase(BaseModel):
    issue_severity: IssueSeverity
    issue_warning: str
    probability_type: ProbabilityType
    probability: float


class Issue(IssueBase):
    id: int
    interaction_id: int


class InteractionBase(BaseModel):
    medication1: int
    medication2: int


class Interaction(InteractionBase):
    id = int
    issues: list[Issue] = []

    class Config:
        orm_mode = True


class MedicationRequestBase(BaseModel):
    pass


class MedicationRequest(MedicationRequestBase):
    pass


class PredictionBase(BaseModel):
    pass


class PredictionCreate(PredictionBase):
    pass


class Prediction(PredictionBase):
    pass


