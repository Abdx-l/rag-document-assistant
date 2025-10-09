# RAG Document Assistant

PDF ingestion with overlapping chunks, MiniLM embeddings, FAISS cosine retrieval, source/page citations, refusal below threshold, FastAPI endpoints, and retrieval evaluation. Answers currently return cited source excerpts so claims stay traceable.

## Run

Install requirements.txt, place PDFs in documents/, run `uvicorn app:app`. POST /ask with {"question":"..."}. Run `pytest`; evaluation reads JSONL question/source/page labels.
