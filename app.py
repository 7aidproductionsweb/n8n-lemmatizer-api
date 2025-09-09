# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy

# Charger le modèle une seule fois au démarrage
nlp = spacy.load("fr_core_news_sm")

class In(BaseModel):
    text: str

app = FastAPI(title="API de Lemmatisation")

@app.post("/lemmatize")
def lemmatize(inp: In):
    if not inp.text.strip():
        raise HTTPException(status_code=400, detail="Le champ 'text' ne peut pas être vide.")
    doc = nlp(inp.text)
    lemmas = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    if not lemmas and len(doc) > 0:
        lemmas = [doc[0].lemma_]
    return {"infinitifs": lemmas}
