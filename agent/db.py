import aiosqlite, os, sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS hosts(
  id INTEGER PRIMARY KEY, program TEXT, host TEXT, tech TEXT, alive INTEGER, last_seen TEXT
);
CREATE TABLE IF NOT EXISTS findings(
  id INTEGER PRIMARY KEY, program TEXT, host TEXT, url TEXT,
  template TEXT, severity TEXT, evidence TEXT, status TEXT, created_at TEXT
);
"""

def init_db(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    con.commit()
    con.close()

async def insert_hosts(db_path, program, rows):
    async with aiosqlite.connect(db_path) as con:
        for r in rows:
            await con.execute(
              "INSERT INTO hosts(program,host,tech,alive,last_seen) VALUES(?,?,?,1,datetime('now'))",
              (program, r["url"], ",".join(r.get("tech",[])))
            )
        await con.commit()

async def insert_findings(db_path, program, rows):
    async with aiosqlite.connect(db_path) as con:
        for f in rows:
            url = f.get("matched","") or ""
            await con.execute(
              "INSERT INTO findings(program,host,url,template,severity,evidence,status,created_at) VALUES(?,?,?,?,?,?,?,datetime('now'))",
              (program, url, url, f.get("template",""), f.get("severity",""), f.get("evidence",""), "new")
            )
        await con.commit()
