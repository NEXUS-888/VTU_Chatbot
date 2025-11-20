# app/ai_bot_core.py

import re
from nlp_core import (
    SYLLABUS,
    IMP_Q,
    classify_intent,
    match_module,
    match_imp_questions,
)

def _get_module(num: int):
    for m in SYLLABUS["modules"]:
        if m["number"] == num:
            return m
    return None

# ---------- Handlers ----------

def handle_syllabus(q: str) -> str:
    m = re.search(r"(module|unit)\s+(\d+)", q.lower())
    if m:
        num = int(m.group(2))
    else:
        num = match_module(q)

    mod = _get_module(num)
    if not mod:
        return "I don't have details for that module."

    lines = [
        f"**Module {mod['number']}: {mod['title']}**",
        "",
        mod["description"],
    ]
    if "chapters" in mod and mod["chapters"]:
        lines.append("")
        lines.append(f"Textbook coverage: {mod['chapters']}")
    return "\n".join(lines)

def handle_exam_pattern() -> str:
    ep = SYLLABUS["exam_pattern"]
    return (
        f"**Exam pattern for {SYLLABUS['subject_name']} ({SYLLABUS['subject_code']}):**\n"
        f"- CIE: {ep['cie_marks']} marks\n"
        f"- SEE: {ep['see_marks']} marks\n"
        f"- Duration: {ep['duration_hours']} hours\n"
        "CIE usually includes two tests and assignments as per department rules."
    )

def handle_course_outcomes() -> str:
    cos = SYLLABUS.get("course_outcomes", [])
    if not cos:
        return "Course outcomes are not added yet."
    lines = [
        f"**Course Outcomes for {SYLLABUS['subject_name']} ({SYLLABUS['subject_code']}):**"
    ]
    for i, co in enumerate(cos, start=1):
        lines.append(f"{i}. {co}")
    return "\n".join(lines)

def handle_imp_questions(q: str) -> str:
    ql = q.lower()
    m = re.search(r"(module|unit)\s+(\d+)", ql)

    # If module explicitly mentioned -> list ALL questions of that module
    if m:
        num = int(m.group(2))
        df = IMP_Q[IMP_Q["module"] == num] if not IMP_Q.empty else IMP_Q
        if df is None or df.empty:
            # fallback to similarity if no exact module data
            df = match_imp_questions(q, top=5)

        if df is None or df.empty:
            return "I don't have important questions stored for that module yet."

        lines = [f"**Important questions for Module {num}:**"]
        for _, row in df.iterrows():
            lines.append(f"- {row['question']}")
        return "\n".join(lines)

    # Otherwise use TF-IDF to get top questions
    df = match_imp_questions(q, top=5)
    if df is None or df.empty:
        return "I don't have important questions stored yet."

    lines = ["**Here are some relevant important questions:**"]
    for _, row in df.iterrows():
        lines.append(f"- (Module {row['module']}) {row['question']}")
    return "\n".join(lines)

# ---------- Main entry ----------

def answer_question(q: str) -> str:
    intent = classify_intent(q)

    if intent == "syllabus":
        return handle_syllabus(q)
    if intent == "exam_pattern":
        return handle_exam_pattern()
    if intent == "course_outcomes":
        return handle_course_outcomes()
    if intent == "important_questions":
        return handle_imp_questions(q)

    return (
        "I can help with:\n"
        "- Module-wise syllabus\n"
        "- Exam pattern (CIE / SEE)\n"
        "- Course outcomes\n"
        "- Important questions (e.g. 'important questions of module 3')"
    )
