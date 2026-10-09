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

INSERT INTO opportunities (title, category, label, icon, iconTone, description, amount, deadline, level, location, tag, eligibility, details, provider, url) VALUES
('Campus Idea Lab Microgrant','funding','FUNDING & GRANTS','✳','green','Small starter grants for students testing a campus or community idea.','Up to ₹25,000','Rolling applications','undergraduate','india','Prototype friendly','Enrolled undergraduate students with an early-stage idea and a faculty or campus mentor.','Sample listing. Confirm current amounts, documents and dates with the official provider.','Campus innovation office',''),
('Student Startup Sprint','startup','BUILD A STARTUP','↗','peach','A guided six-week program to validate a problem and shape a first pitch.','Mentorship + workspace','Next cohort: check provider','any','india','Beginner friendly','Open to college students working individually or in teams; no registered company required.','Sample listing. Confirm the next intake with the host incubator.','University incubator',''),
('National Innovation Challenge','innovation','INNOVATION PROGRAM','⚡','blue','Turn a real-world problem into a working solution with expert feedback.','Awards + incubation','Seasonal','undergraduate','india','Team applications','Student teams from recognized colleges; annual themes and team size may vary.','Sample listing. Look for the current edition on the organizer’s official site.','Innovation program',''),
('Need-Based Student Support','student','STUDENT SCHEME','✦','lilac','Financial support to help eligible students meet education expenses.','Varies by scheme','Check official portal','undergraduate','india','Education support','Eligibility may depend on household income, course and institution rules.','Sample listing. Verify conditions and application portal with an official source.','Government / institution',''),
('Build It Prototype Fund','funding','FUNDING & GRANTS','⚙','blue','Funding and lab access for students turning a concept into a first prototype.','Up to ₹1,00,000','Two calls per year','any','india','Hardware & software','Student founders at participating colleges; a proposal or mentor endorsement may be required.','Sample listing. Check the current official announcement.','Partner incubator',''),
('Emerging Builders Fellowship','innovation','INNOVATION PROGRAM','◎','lilac','A remote peer community for students building solutions with social impact.','Mentoring + network','Applications open seasonally','any','global','Remote friendly','Students worldwide interested in responsible innovation and community-led projects.','Sample listing. Check the organizer for country eligibility and dates.','Global fellowship',''),
('Research to Market Track','startup','BUILD A STARTUP','⌘','green','Explore commercialization support for research and university inventions.','Incubation + expert support','Contact your institute','postgraduate','india','Research-led ideas','Postgraduate students and researchers with an institute-linked project.','Sample listing. Availability depends on your institution.','University TTO / incubator',''),
('Student Conference Travel Aid','student','STUDENT SCHEME','✈','peach','Find support for attending academic, innovation and entrepreneurship events.','Partial travel support','Before event registration','any','global','Travel & participation','Current students attending eligible events; institution rules apply.','Sample listing. Contact your student affairs office for its grant rules.','College student affairs','');
