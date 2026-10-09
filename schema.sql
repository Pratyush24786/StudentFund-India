CREATE TABLE IF NOT EXISTS opportunities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  category TEXT NOT NULL CHECK (category IN ('funding', 'startup', 'innovation', 'student')),
  label TEXT NOT NULL,
  icon TEXT NOT NULL,
  iconTone TEXT NOT NULL,
  description TEXT NOT NULL,
  amount TEXT NOT NULL,
  deadline TEXT NOT NULL,
  level TEXT NOT NULL CHECK (level IN ('undergraduate', 'postgraduate', 'any')),
  location TEXT NOT NULL CHECK (location IN ('india', 'global')),
  tag TEXT NOT NULL DEFAULT '',
  eligibility TEXT NOT NULL,
  details TEXT NOT NULL,
  provider TEXT NOT NULL,
  url TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
