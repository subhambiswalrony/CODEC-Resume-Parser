# 🧾 Resume Parser — Ready to Run (Fullstack)

## What you got 🚀
- Flask backend that accepts resume uploads (PDF/DOCX), parses them using spaCy + pdfplumber, and stores parsed results to PostgreSQL.
- Frontend with glassmorphism UI, light/dark toggle, resume text preview, and search UI.
- SQL schema to create the necessary tables.

## Prereqs ✅
- Python 3.10+
- PostgreSQL
- (Optional) virtualenv

## 📁 Project Structure
```
RESUME-PARSER/
│
├── backend/
│   ├── __pycache__/                  # Auto-generated Python cache files
│   │
│   ├── uploads/                      # Folder to store uploaded resume files temporarily
│   │
│   ├── app.py                        # Main Flask backend application (API endpoints)
│   ├── db.py                         # Handles PostgreSQL database connection and queries
│   ├── parser.py                     # Core logic for parsing resumes (text extraction & processing)
│   ├── requirements.txt              # List of Python dependencies for backend
│   └── schema.sql                    # SQL schema for creating required database tables
│
├── frontend/
│   ├── index.html                    # Main UI for uploading resumes
│   ├── script.js                     # Handles frontend logic and API requests
│   └── style.css                     # Styling for the frontend interface
│
└── README.md                         # Documentation and setup guide
```


## Setup ⚙️
1️⃣ Create a Postgres DB and run `backend/schema.sql` to create tables.

2️⃣ From the `backend/` folder, install Python deps:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3️⃣ Set `DATABASE_URL` env var (or use a `.env` file at project root):
   ```powershell
   # Windows PowerShell
   $env:DATABASE_URL = "postgresql://user:pass@localhost:5432/resumes"
   ```
   or
   ```bash
   # Unix / macOS
   export DATABASE_URL="postgresql://user:pass@localhost:5432/resumes"
   ```

4️⃣ Start the Flask app from the `backend` folder:
   ```powershell
   C:\path\to\venv\Scripts\python.exe app.py
   ```

5️⃣ Open the frontend at `http://localhost:5000/` in your browser and test uploading resumes.

## Notes ⚠️
- The spaCy model (`en_core_web_sm`) must be downloaded separately.
- For production, use connection pooling and a proper WSGI server (gunicorn/uvicorn).
- Legacy `.doc` files are not supported by python-docx; convert to `.docx` first.

## 📄 License

This project is created for educational purposes as part of Codec Technologies' training program.

## 🙏 Credits 🙌

Developed as part of the AI project at Codec Technologies.
Developed by Subham Biswal ❤️