# VTU_Chatbot
A simple, student-friendly AI assistant for VTU (2022 Scheme)

This project is a lightweight chatbot built to help VTU students quickly find the information they need — syllabus details, module explanations, exam patterns, important questions, and more. Instead of scrolling through PDFs or asking classmates, you can just type your doubt and get a clear answer instantly.

The current version focuses on **CSE 5th Semester – Artificial Intelligence (BCS515B)**, but the structure is flexible enough to expand to any VTU subject or semester later.

---

## 🌟 What This Chatbot Can Do

- **Module-wise syllabus lookup**  
  Ask things like “What’s in module 3?” or “Explain module 1 topics”.

- **Important question suggestions**  
  Type “important questions of module 5” and you’ll get a clean list ready for exam prep.

- **Smart question matching**  
  Even if your grammar isn’t perfect — “imporatant ques of ai mod 3” — it still understands you.

- **Exam pattern & CIE/SEE info**  
  Tell the bot “exam pattern for AI” and it gives you the precise breakdown.

- **Course outcomes (COs)**  
  Handy when preparing assignments or understanding what the course expects from you.

---

## 🧠 How It Works (In Simple Words)

This is not a heavy LLM model.  
It uses simple and efficient techniques:

- **TF-IDF** to understand and match questions  
- **Rule-based intent detection** (syllabus? exam pattern? important questions?)  
- **Clean, structured JSON/CSV data** as its knowledge base  
- **Streamlit** to create a fast and clean UI  
- **Python** to keep everything small and easy to modify

This makes the chatbot fast, predictable, and perfect for a college mini-project.

---

## 📂 Project Structure

vtu-chatbot/
│── app/
│ ├── ai_app.py # Streamlit UI
│ ├── ai_bot_core.py # Chatbot logic
│ └── nlp_core.py # NLP + similarity matching
│
│── data/
│ └── syllabus/
│ ├── bcs515b_syllabus.json
│ └── important_questions_ai.csv
│
│── notebooks/ # For testing or experiments (optional)
│── requirements.txt
│── README.md

yaml
Copy code

---

## 🚀 Running the Project

Make sure you have Python installed (and a virtual environment helps).

1. Clone/download this project  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
Run the app:

bash
Copy code
streamlit run app/ai_app.py
Open the link Streamlit shows (usually http://localhost:8501)

That’s it. Start chatting with your VTU AI assistant.

📝 Data Sources
VTU 2022 Scheme syllabus (Artificial Intelligence – BCS515B)

Manually curated important questions

Official CIE/SEE guidelines and module descriptions

🎯 Future Improvements
Support for more VTU subjects

Cleaner UI with animations or dark mode themes

Adding diagrams or unit summaries

Student login + saving notes

Embedding-based vector search for deeper Q&A

