import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel,Field
from retrieval import Index
index=None
@asynccontextmanager
async def lifespan(app):
 global index
 index=Index()
 for p in Path(os.getenv("DOCUMENT_DIR","documents")).glob("*.pdf"):index.add_pdf(p)
 yield
app=FastAPI(lifespan=lifespan)
class Question(BaseModel):question:str=Field(min_length=1,max_length=4000)
@app.post("/ask")
def ask(q:Question):
 sources=index.search(q.question)
 return {"answer":"\n".join(f'{s["text"]} [{s["id"]}]' for s in sources) if sources else "Not found in the documents.","sources":sources,"mode":"cited-excerpts"}
@app.get("/health")
def health():return {"indexed_chunks":len(index.chunks) if index else 0}
