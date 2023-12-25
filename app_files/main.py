"""
Main script that runs my application.
"""
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="serve_up_recos/templates")


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Templates I will need:
#   register and login - maybe one, could be two
#   select workflow & patient - call this the encounter setup template
#   medication request -  load in the patients details, prescriptions, medications
#   medication requested - include predictions to the above template or duplicate similar template
#   medication order - end template, from here provider can pick another patient or workflow.


# Path - GET: base/root page with minimal info and links to regist/login
@app.get("/")
async def get_root():
    return templates.TemplateResponse("index.html", {})


# Path - GET: page for registering a provider
@app.get("/providers/register")
async def get_register_provider():
    return templates.TemplateResponse("register.html", {})


# Path - POST: create a provider if the user_name isn't already registered
# Maybe this should return login template.
@app.post("/providers/register", response_model=schemas.Provider)
def register_provider(provider: schemas.ProviderCreate, db: Session = Depends(get_db)):
    a_provider = crud.get_provider(db, provider.user_name)
    if a_provider:
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        return crud.register_provider(db, provider)


# Path - GET: page for logging in a provider
@app.get("/providers/login")
async def get_register_provider():
    return templates.TemplateResponse("login.html", {})


# Path - POST: login a provider, validate user_name and email.
@app.post("/providers/login", response_model=schemas.Provider)
def login_provider(user_name: str, password: str, db: Session = Depends(get_db)):
    a_provider = crud.login_provider(db, user_name, password)
    if a_provider == 'Password':
        raise HTTPException(status_code=401, detail="Invalid password")
    elif a_provider == 'User':
        raise HTTPException(status_code=401, detail="Provider not found")
    else:
        return a_provider



# Example of how to make medication request
# Assuming you have a session object already created
# medication_request = MedicationRequest(patient_id=some_patient_id, provider_id=some_provider_id)
# medication_request.set_medication_ids(session)  # Retrieve and set medication IDs
# session.add(medication_request)
# session.commit()

# Retrieve medication IDs from the MedicationRequest instance
# medication_ids = medication_request.get_medication_ids()
# print("Medication IDs:", medication_ids)
