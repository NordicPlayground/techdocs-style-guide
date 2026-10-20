# tiny_docs_mcp.py
import sqlite3, pathlib, json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TechDocsStyleGuideMCP")

# Use absolute path for DB based on the script location
SCRIPT_DIR = pathlib.Path(__file__).parent.parent
DB = str(SCRIPT_DIR / "docs_index.db")

# skip typical noise dirs
EXCLUDE_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "dist", "build", "out", ".tox",
                ".mypy_cache", ".pytest_cache", "__pycache__"}

def _conn():
    c = sqlite3.connect(DB)
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA synchronous=NORMAL;")
    return c

def _reset_schema(cur):
    cur.execute("DROP TABLE IF EXISTS docs;")
    cur.execute("""
      CREATE VIRTUAL TABLE docs USING fts5(
        path UNINDEXED, title, content, tokenize='porter'
      );
    """)

@mcp.tool()
def reindex(root: str = ".") -> str:
    """
    Rebuild the index from scratch for all .md/.rst under 'root'.
    Excludes the *root* README.md and common build/VC dirs.
    """
    rootp = pathlib.Path(root).resolve()
    c = _conn(); cur = c.cursor()
    _reset_schema(cur)
    rows = []
    for p in rootp.rglob("*"):
        # relative to root, so folders above root don't count as excluded dirs
        rel = p.relative_to(rootp)
        if (not p.is_file() or p.suffix.lower() not in {".md", ".rst"}
                or any(part in EXCLUDE_DIRS for part in rel.parts) or rel.as_posix() == "README.md"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rows.append((rel.as_posix(), p.stem, text))
    if rows:
        cur.executemany("INSERT INTO docs(path,title,content) VALUES(?,?,?)", rows)
    c.commit(); c.close()
    return f"Indexed {len(rows)} files from {rootp}"

@mcp.tool()
def search(query: str, k: int = 8) -> str:
    """
    Full-text search. Returns JSON: [{id,title,path,snippet,resource_uri}]. Use read_doc with a hit's id for the full page.
    """
    c = _conn(); c.row_factory = sqlite3.Row
    cur = c.cursor()
    cur.execute("""
      SELECT rowid, path, title,
             snippet(docs, 2, '[', ']', ' … ', 12) AS snippet
      FROM docs
      WHERE docs MATCH ?
      ORDER BY rank
      LIMIT ?
    """, (query, k))
    out = []
    for r in cur.fetchall():
        rid = r["rowid"]
        out.append({
            "id": rid,
            "title": r["title"],
            "path": r["path"],              # repo-relative path (e.g. docs/…)
            "snippet": r["snippet"],
            "resource_uri": f"doc://by-id/{rid}"
        })
    c.close()
    return json.dumps(out, ensure_ascii=False, indent=2)

@mcp.resource("doc://by-id/{rowid}")
def get_doc_by_id(rowid: int) -> str:
    """
    Fetch the full plain content for a search hit by numeric id.
    """
    c = _conn(); c.row_factory = sqlite3.Row
    cur = c.cursor()
    row = cur.execute("SELECT content FROM docs WHERE rowid=?", (rowid,)).fetchone()
    c.close()
    if not row:
        raise FileNotFoundError(f"No doc with id={rowid}")
    return row["content"]

@mcp.tool()
def read_doc(id: int) -> str:
    """
    Return the full plain content of a search hit by its numeric id. Same text as doc://by-id/{id}.
    """
    return get_doc_by_id(id)

if __name__ == "__main__":
    mcp.run(transport="stdio")
