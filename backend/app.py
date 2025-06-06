from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from backend import model, vector_store, jsonlookup, config
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Personal Chatbot API",
    description="An API to interact with Venkata Ramana Reddy's resume and project portfolio.",
    version="1.0.0"
)

# Add this block to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectordb = vector_store.load_vector_store()
project_metadata = jsonlookup.load_project_metadata(os.path.join(config.ROOT_DIR, "data/project_metadata.json"))

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    project = jsonlookup.search_project_info(query.question, project_metadata)
    if project:
        return {"response": project}
    else:
        answer = model.answer_query(query.question, vectordb)
        return {"response": answer}

@app.post("/voice-query")
def voice_query(file: UploadFile = File(...)):
    from backend.voice_module import speech_to_text, text_to_speech
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    text = speech_to_text(temp_path)
    answer = model.answer_query(text, vectordb)
    text_to_speech(answer)
    return {"response": answer}