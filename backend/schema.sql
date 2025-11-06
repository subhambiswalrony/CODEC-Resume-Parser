-- create DB and tables (Postgres)
CREATE TABLE IF NOT EXISTS candidates (
  id SERIAL PRIMARY KEY,
  full_name TEXT,
  email TEXT,
  phone TEXT,
  location TEXT,
  summary TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS skills (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS candidate_skills (
  candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
  skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
  PRIMARY KEY (candidate_id, skill_id)
);

CREATE TABLE IF NOT EXISTS education (
  id SERIAL PRIMARY KEY,
  candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
  degree TEXT,
  institution TEXT,
  start_date TEXT,
  end_date TEXT,
  raw TEXT
);

CREATE TABLE IF NOT EXISTS experience (
  id SERIAL PRIMARY KEY,
  candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
  title TEXT,
  company TEXT,
  start_date TEXT,
  end_date TEXT,
  description TEXT,
  raw TEXT
);

CREATE INDEX IF NOT EXISTS idx_skills_name ON skills(lower(name));
