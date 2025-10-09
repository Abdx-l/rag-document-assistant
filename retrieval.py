from dataclasses import dataclass,asdict
from pathlib import Path
import json,numpy as np
@dataclass
class Chunk:
 id:str
 source:str
 page:int
 text:str
def chunks(text,size=500,overlap=50):
 if size<=overlap or overlap<0:raise ValueError("overlap must be smaller than size")
 words=text.split()
 for start in range(0,len(words),size-overlap):
  yield " ".join(words[start:start+size])
  if start+size>=len(words):break
class Index:
 def __init__(self,encoder=None):
  if encoder is None:
   from sentence_transformers import SentenceTransformer
   encoder=SentenceTransformer("all-MiniLM-L6-v2")
  self.encoder=encoder;self.chunks=[];self.vectors=None
 def add_pdf(self,file,size=500):
  from pypdf import PdfReader
  new=[]
  for page,content in enumerate(PdfReader(file).pages,1):
   for part,text in enumerate(chunks(content.extract_text() or "",size)):
    new.append(Chunk(f"{Path(file).name}:{page}:{part}",str(file),page,text))
  self.chunks.extend(new)
  if self.chunks:self.vectors=np.asarray(self.encoder.encode([c.text for c in self.chunks],normalize_embeddings=True),dtype="float32")
 def search(self,question,k=5,threshold=.25):
  if not self.chunks:return []
  import faiss
  index=faiss.IndexFlatIP(self.vectors.shape[1]);index.add(self.vectors)
  scores,indices=index.search(np.asarray(self.encoder.encode([question],normalize_embeddings=True),dtype="float32"),min(k,len(self.chunks)))
  return [{**asdict(self.chunks[i]),"score":float(s)} for s,i in zip(scores[0],indices[0]) if s>=threshold]
