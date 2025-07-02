from fastapi import FastAPI, HTTPException
from models import QuestionnaireInput
from db import save_response

app = FastAPI()

@app.get("/")
def root():
    return {"message": "GrowPal backend is running"}

@app.post("/submit-questionnaire")
def submit_questionnaire(data: QuestionnaireInput):
    try:
        save_response(data)
        return {"status": "success", "message": "Preferences saved!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
