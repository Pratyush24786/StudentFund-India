"""Launchpad local web server and SQLite API."""
import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

BASE = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("LAUNCHPAD_DB", BASE / "launchpad.db"))
ADMIN_PASSWORD = os.environ.get("LAUNCHPAD_ADMIN_PASSWORD", "change-me-now")
app = Flask(__name__, static_folder=str(BASE), static_url_path="")

FIELDS = ("title", "category", "label", "icon", "iconTone", "description", "amount", "deadline", "level", "location", "tag", "eligibility", "details", "provider", "url")
SAMPLES = [
    ("Campus Idea Lab Microgrant","funding","FUNDING & GRANTS","✳","green","Small starter grants for students testing a campus or community idea.","Up to ₹25,000","Rolling applications","undergraduate","india","Prototype friendly","Enrolled undergraduate students with an early-stage idea and a faculty or campus mentor.","A sample microgrant listing for student-led experiments. Confirm current funding limits, documents and dates with the official provider.","Campus innovation office",""),
    ("Student Startup Sprint","startup","BUILD A STARTUP","↗","peach","A guided six-week program to validate a problem and shape a first pitch.","Mentorship + workspace","Next cohort: check provider","any","india","Beginner friendly","Open to college students working individually or in teams; no registered company required.","A sample early-stage startup program. Confirm the next intake with the host incubator.","University incubator",""),
    ("National Innovation Challenge","innovation","INNOVATION PROGRAM","⚡","blue","Turn a real-world problem into a working solution with expert feedback.","Awards + incubation","Seasonal","undergraduate","india","Team applications","Student teams from recognized colleges. Challenge themes and team size depend on the annual call.","A sample innovation challenge entry. Look for the current edition on the organizer’s official site.","Innovation program",""),
    ("Need-Based Student Support","student","STUDENT SCHEME","✦","lilac","Financial support to help eligible students meet education expenses.","Varies by scheme","Check official portal","undergraduate","india","Education support","Eligibility may depend on household income, course, academic progress and state or institution rules.","A sample directory entry. Verify conditions and the application portal with an official source.","Government / institution",""),
    ("Build It Prototype Fund","funding","FUNDING & GRANTS","⚙","blue","Funding and lab access for students turning a concept into a first prototype.","Up to ₹1,00,000","Two calls per year","any","india","Hardware & software","Student founders at participating colleges. A short proposal and mentor endorsement may be required.","A sample prototype support opportunity. Check the current official announcement.","Partner incubator",""),
    ("Emerging Builders Fellowship","innovation","INNOVATION PROGRAM","◎","lilac","A remote peer community for students building solutions with social impact.","Mentoring + network","Applications open seasonally","any","global","Remote friendly","Students worldwide interested in responsible innovation and community-led projects.","A sample global fellowship listing. Check the organizer for country eligibility and dates.","Global fellowship",""),
    ("Research to Market Track","startup","BUILD A STARTUP","⌘","green","Explore commercialization support for research and university inventions.","Incubation + expert support","Contact your institute","postgraduate","india","Research-led ideas","Postgraduate students and researchers with an institute-linked project or patentable idea.","A sample university commercialization pathway. Availability depends on your institution.","University TTO / incubator",""),
    ("Student Conference Travel Aid","student","STUDENT SCHEME","✈","peach","Find support for attending academic, innovation and entrepreneurship events.","Partial travel support","Before event registration","any","global","Travel & participation","Current students presenting, competing or participating in eligible events; institution rules apply.","A sample student benefit listing. Contact your student affairs office for its travel grant rules.","College student affairs",""),
]

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("CREATE TABLE IF NOT EXISTS opportunities (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, category TEXT NOT NULL, label TEXT NOT NULL, icon TEXT NOT NULL, iconTone TEXT NOT NULL, description TEXT NOT NULL, amount TEXT NOT NULL, deadline TEXT NOT NULL, level TEXT NOT NULL, location TEXT NOT NULL, tag TEXT NOT NULL, eligibility TEXT NOT NULL, details TEXT NOT NULL, provider TEXT NOT NULL, url TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        if con.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0] == 0:
            marks = ",".join("?" for _ in FIELDS)
            con.executemany(f"INSERT INTO opportunities ({','.join(FIELDS)}) VALUES ({marks})", SAMPLES)

@app.get("/")
def home():
    return send_from_directory(BASE, "index.html")

@app.get("/admin")
def admin():
    return send_from_directory(BASE, "admin.html")

@app.get("/api/opportunities")
def list_opportunities():
    with connect() as con:
        rows = con.execute(f"SELECT id, {','.join(FIELDS)} FROM opportunities ORDER BY id DESC").fetchall()
    return jsonify([dict(row) for row in rows])

@app.post("/api/opportunities")
def add_opportunity():
    if request.headers.get("X-Admin-Password", "") != ADMIN_PASSWORD:
        return jsonify(error="Incorrect admin password."), 401
    data = request.get_json(silent=True) or {}
    clean = {field: str(data.get(field, "")).strip() for field in FIELDS}
    required = ("title", "category", "description", "amount", "deadline", "eligibility", "details", "provider")
    if any(not clean[field] for field in required):
        return jsonify(error="Please fill in all required fields."), 400
    if clean["category"] not in {"funding", "startup", "innovation", "student"}:
        return jsonify(error="Choose a valid opportunity category."), 400
    if clean["level"] not in {"undergraduate", "postgraduate", "any"} or clean["location"] not in {"india", "global"}:
        return jsonify(error="Choose a valid study level and location."), 400
    if clean["url"] and not clean["url"].startswith(("https://", "http://")):
        return jsonify(error="Official link must start with http:// or https://."), 400
    clean["label"] = {"funding":"FUNDING & GRANTS", "startup":"BUILD A STARTUP", "innovation":"INNOVATION PROGRAM", "student":"STUDENT SCHEME"}[clean["category"]]
    clean["icon"] = clean["icon"] or {"funding":"♢", "startup":"↗", "innovation":"✳", "student":"✦"}[clean["category"]]
    clean["iconTone"] = clean["iconTone"] or {"funding":"green", "startup":"peach", "innovation":"blue", "student":"lilac"}[clean["category"]]
    with connect() as con:
        cur = con.execute(f"INSERT INTO opportunities ({','.join(FIELDS)}) VALUES ({','.join('?' for _ in FIELDS)})", [clean[f] for f in FIELDS])
        row = con.execute(f"SELECT id, {','.join(FIELDS)} FROM opportunities WHERE id=?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "8000")), debug=False)
