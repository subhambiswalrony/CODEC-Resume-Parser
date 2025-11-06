# app.py
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from parser import parse_resume

DB_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@localhost:5432/resumes")

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_conn():
    return psycopg2.connect(DB_URL)

@app.route("/upload", methods=["POST"])
def upload_resume():
    f = request.files.get("file")
    if not f:
        return jsonify({"error":"no file"}), 400
    filename = f.filename
    bytes_ = f.read()
    parsed = parse_resume(bytes_, filename)
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO candidates (full_name, email, phone, location, summary) VALUES (%s,%s,%s,%s,%s) RETURNING id",
            (parsed.get("full_name"), ",".join(parsed.get("emails",[])) or None, ",".join(parsed.get("phones",[])) or None, None, parsed.get("summary"))
        )
        candidate_id = cur.fetchone()[0]
        for skill in parsed.get("skills",[]):
            cur.execute("INSERT INTO skills (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = skills.name RETURNING id", (skill,))
            sid = cur.fetchone()[0]
            cur.execute("INSERT INTO candidate_skills (candidate_id, skill_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", (candidate_id, sid))
        for ed in parsed.get("education",[]):
            cur.execute("INSERT INTO education (candidate_id, degree, institution, raw) VALUES (%s,%s,%s,%s)", (candidate_id, ed.get("degree"), ed.get("institution"), ed.get("raw")))
        for ex in parsed.get("experience",[]):
            cur.execute("INSERT INTO experience (candidate_id, title, company, raw) VALUES (%s,%s,%s,%s)", (candidate_id, ex.get("title"), ex.get("company"), ex.get("raw")))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB error:", e)
    return jsonify({"candidate_id": None, "parsed": parsed})

@app.route('/search')
def search():
    q = request.args.get('q')
    skill = request.args.get('skill')
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if skill:
            cur.execute("""
                SELECT c.* FROM candidates c
                JOIN candidate_skills cs ON cs.candidate_id = c.id
                JOIN skills s ON s.id = cs.skill_id
                WHERE lower(s.name) = lower(%s)
                LIMIT 100
            """, (skill,))
        elif q:
            cur.execute("SELECT * FROM candidates WHERE lower(full_name) LIKE %s OR lower(summary) LIKE %s LIMIT 100", (f"%{q.lower()}%", f"%{q.lower()}%"))
        else:
            cur.execute("SELECT * FROM candidates ORDER BY created_at DESC LIMIT 50")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        print("Search DB error:", e)
        return jsonify([])

# Serve frontend
@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('../frontend', path)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
