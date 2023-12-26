"""
Main script that runs my application.
"""
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="serve_up_recos/static"), name="static")
templates = Jinja2Templates(directory="serve_up_recos/templates")


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MVP Templates I will need:
#   register and login - maybe one, could be two
#   select workflow & patient - call this the encounter setup template
#   medication request -  load in the patients details, prescriptions, medications
#   medication requested - re-render prior template with ddi issues or duplicate similar template


# Path - GET: base/root page with minimal info and links to register/login
@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Path - GET: page for registering a provider
@app.get("/providers/register")
async def get_register_provider(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Path - POST: create a provider if the user_name isn't already registered, redirect to login after user registered
@app.post("/providers/register")
def register_provider(provider: schemas.ProviderCreate, db: Session = Depends(get_db)):
    a_provider = crud.get_provider(db, provider.user_name)
    if a_provider:
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        crud.register_provider(db, provider)
        return RedirectResponse(url="/providers/login", status_code=303)


# Path - GET: page for logging in a provider
@app.get("/providers/login")
async def get_register_provider(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Path - POST: login a provider, validate user_name and email.
# Need to replace return a_provider with the actual place to send customer
# Maybe use oauth or something else to generate session tokens
@app.post("/providers/login", response_model=schemas.Provider)
def login_provider(user_name: str, password: str, db: Session = Depends(get_db)):
    a_provider = crud.login_provider(db, user_name, password)
    if a_provider == 'Password':
        raise HTTPException(status_code=401, detail="Invalid password")
    elif a_provider == 'User':
        raise HTTPException(status_code=401, detail="Provider not found")
    else:
        redirect_url = f"/encounter/setup?user_name={a_provider.user_name}"
        return RedirectResponse(url=redirect_url)


# Path - GET: Show a logged in provider the workflows and patients they can choose (1 each) to start the workflow
@app.get("/encounter/setup")
def setup_encounter(request: Request, user_name: str, db: Session = Depends(get_db)):
    patients = crud.get_patients(db)
    workflows = {1: "medication_request"}
    return templates.TemplateResponse("encounter_setup.html", {
        "request": request, "provider": user_name, "patients": patients, "workflows": workflows})


# Path - GET: Start medication request workflow, show patient data,
# and show their prescriptions and list of meds that can be selected to request
@app.get("/encounter/medication_request")
def start_workflow(request: Request, user_name: str, workflow_name: str,
                   patient_id: UUID, db: Session = Depends(get_db)):
    if workflow_name == "medication_request":
        workflow_data = crud.get_workflow_data(db, patient_id)
        patient = workflow_data[0]
        medications = workflow_data[1]
        return templates.TemplateResponse("medication_request_wf.html", {
            "request": request, "provider": user_name, "patient": patient, "medications": medications})


# PATH - POST: Submit medication request, get back issues for drug-drug interactions and show them
@app.post("/encounter/medication_request")
def medication_request(request: Request, user_name: str,
                       patient_id: UUID, new_med: int, db: Session = Depends(get_db)):
    mr_id = crud.make_medication_request(db, patient_id, user_name, new_med)
    issue_list = crud.serve_ddi_issues(db, mr_id)
    workflow_data = crud.get_workflow_data(db, patient_id)
    patient = workflow_data[0]
    medications = workflow_data[1]
    # Is this a better style for returning the template as data grows?
    template_name = "medication_request_wf.html"
    template_context = {
        "request": request,
        "user_name": user_name,
        "patient": patient,
        "medications": medications,
        "new_med": new_med,
        "issue_list": issue_list,
    }
    return templates.TemplateResponse(template_name, template_context)
