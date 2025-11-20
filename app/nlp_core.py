# app/nlp_core.py

import re
import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Paths & data loading ----------

BASE = Path(__file__).resolve().parent.parent / "data" / "syllabus"

syllabus_path = BASE / "bcs515b_syllabus.json"
questions_path = BASE / "important_questions_ai.csv"

with open(syllabus_path, "r", encoding="utf-8") as f:
    SYLLABUS = json.load(f)

if questions_path.exists():
    IMP_Q = pd.read_csv(questions_path)
else:
    print("WARNING: important_questions_ai.csv not found, using empty frame")
    IMP_Q = pd.DataFrame(columns=["module", "question"])

# ---------- Helpers ----------

def clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def classify_intent(q: str) -> str:
    ql = q.lower()

    # be forgiving about spelling ("imporatant", "imp", etc.)
    if "important" in ql or "imporatant" in ql or "imp q" in ql or "imp question" in ql:
        return "important_questions"

    if any(k in ql for k in ["mark", "cie", "see", "exam pattern", "internal", "ia"]):
        return "exam_pattern"

    if any(k in ql for k in ["course outcome", "course outcomes", "co", "skill set"]):
        return "course_outcomes"

    if any(k in ql for k in ["syllabus", "module", "unit", "topic", "chapter"]):
        return "syllabus"

    if "question" in ql:
        return "important_questions"

    return "syllabus"

# ---------- TF-IDF for modules ----------

module_texts = []
module_ids = []

for m in SYLLABUS["modules"]:
    txt = f"module {m['number']} {m['title']} {m['description']} {m.get('chapters','')}"
    module_texts.append(clean(txt))
    module_ids.append(m["number"])

mod_vec = TfidfVectorizer()
mod_matrix = mod_vec.fit_transform(module_texts)

def match_module(query: str) -> int:
    vec = mod_vec.transform([clean(query)])
    sims = cosine_similarity(vec, mod_matrix)[0]
    idx = sims.argmax()
    return module_ids[idx]

# ---------- TF-IDF for important questions ----------

if not IMP_Q.empty:
    q_vec = TfidfVectorizer()
    q_matrix = q_vec.fit_transform([clean(q) for q in IMP_Q["question"]])

    def match_imp_questions(q: str, top: int = 5) -> pd.DataFrame:
        vec = q_vec.transform([clean(q)])
        sims = cosine_similarity(vec, q_matrix)[0]
        idxs = sims.argsort()[::-1][:top]
        return IMP_Q.iloc[idxs]
else:
    def match_imp_questions(q: str, top: int = 5) -> pd.DataFrame:
        return IMP_Q
