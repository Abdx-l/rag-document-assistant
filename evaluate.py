import argparse,json
from retrieval import Index
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("documents");p.add_argument("questions");a=p.parse_args()
questions=[json.loads(l) for l in Path(a.questions).read_text().splitlines() if l.strip()]
for size in (200,500,1000):
 index=Index()
 for file in Path(a.documents).glob("*.pdf"):index.add_pdf(file,size)
 hits=sum(any(s["page"]==q["page"] and Path(s["source"]).name==q["source"] for s in index.search(q["question"])) for q in questions)
 print({"chunk_size":size,"hit_rate_at_5":hits/len(questions) if questions else 0})
