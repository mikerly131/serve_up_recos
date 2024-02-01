# serve_up_recos
Mocked EHR workflow for a medication request by a provider during an encounter with a patient.   Built using Python with the FastAPI framework.
Demonstrates drug-drug interaction warnings when a new medication is requested for the patient.
This is an MVP that relies on known drug interactions sourced from the now deprecated NIH drugInteraction API.

# App Setup - Local
### <span style="color: red;"> APP WON'T WORK: DATA FILES NOT IN THE REPO YET</span>
1. Clone the repo in a directory. Now you have a project directory
2. Setup a virtual environment in the project directory
3. Install the requirements.txt file
4. From project directory in terminal run: uvicorn app_files.main:app --reload
5. Press ctrl-c to kill the app now that the DB is created.
6. Run the setup_step1.py file in the populated_db sub-directory
7. Run the setup_step2.py file in the populated_db sub-directory

Setup is now complete. This is only needed once. Run the app locally from terminal with:
<code>uvicorn app_files.main:app --reload</code>



# Open Source Used (MIT/Apache Licensed)
Check out NOTICE.md for information on code I utilized that is provided free of charge and its licensing.

# Works Cited
Check out NOTICE.md for citations on sources of data for this project.



