# backend/main.py
from fastapi import FastAPI, HTTPException
from backend.models import TranscriptionRequest, SummaryRequest, SaveRequest
from backend.utils import transcribe_audio, generate_summary_pegasus, generate_solutions
from backend.database import init_db, save_user_data, get_user_data

app = FastAPI()

# Initialize the database
init_db()

@app.post("/transcribe")
def transcribe(request: TranscriptionRequest):
    try:
        # The request contains a base64-encoded audio file
        transcription = transcribe_audio(request.audio_file)
        return {"transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
def summarize(request: SummaryRequest):
    try:
        # Use the Pegasus-based summarization
        summary = generate_summary_pegasus(request.transcription_text, request.summary_type)
        solutions = generate_solutions(summary, request.solution_types)
        return {"summary": summary, "solutions": solutions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save")
def save_data(request: SaveRequest):
    try:
        save_user_data(
            email=request.email,
            full_text=request.full_text,
            summary=request.summary,
            template=request.template
        )
        return {"message": "Data saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/retrieve")
def retrieve_data(email: str):
    data = get_user_data(email)
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail="User data not found.")
