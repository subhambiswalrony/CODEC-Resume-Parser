# Resume Parser — Ready to Run (Fullstack)

## What you got
- Flask backend that accepts resume uploads (PDF/DOCX), parses them using spaCy + pdfplumber, and stores parsed results to PostgreSQL.
- Frontend with glassmorphism UI, light/dark toggle, resume text preview, and search UI.
- SQL schema to create the necessary tables.

## Prereqs
- Python 3.10+
- PostgreSQL
- (Optional) virtualenv

## Setup
1. Create a Postgres DB and run `backend/schema.sql` to create tables.
2. From the `backend/` folder, install Python deps:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
3. Set `DATABASE_URL` env var:
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost:5432/resumes"
   ```
4. Start the Flask app from the `backend` folder:
   ```bash
   python app.py
   ```
5. Open the frontend at `http://localhost:5000/` in your browser and test uploading resumes.

## Notes
- The spaCy model (`en_core_web_sm`) must be downloaded separately.
- For production, use connection pooling and a proper WSGI server (gunicorn/uvicorn).
- Legacy `.doc` files are not supported by python-docx; convert to `.docx` first.
