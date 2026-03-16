# tiny_docs_mcp_easy.py
# A beginner-friendly MCP server for searching documentation

import sqlite3
import pathlib
import json
from mcp.server.fastmcp import FastMCP

# =============================================================================
# STEP 1: Setup and Configuration
# =============================================================================

# Create the MCP server with a name
server = FastMCP("StyleGuideMCP")

# Find where this script is located
script_location = pathlib.Path(__file__).parent.parent

# Database file will be stored next to the script
database_file = str(script_location / "docs_index.db")

# Folders to skip when indexing (build artifacts, version control, etc.)
SKIP_FOLDERS = {
    ".git", ".venv", "venv", "node_modules",
    "dist", "build", "__pycache__"
}


# =============================================================================
# STEP 2: Database Helper Functions
# =============================================================================

def connect_to_database():
    """Open a connection to the SQLite database"""
    connection = sqlite3.connect(database_file)
    # These settings make the database faster and more reliable
    connection.execute("PRAGMA journal_mode=WAL;")
    connection.execute("PRAGMA synchronous=NORMAL;")
    return connection


def create_search_table(cursor):
    """Create a fresh search table (deletes old one if exists)"""
    # Delete old table
    cursor.execute("DROP TABLE IF EXISTS docs;")

    # Create new search table using FTS5 (Full-Text Search)
    cursor.execute("""
        CREATE VIRTUAL TABLE docs USING fts5(
            path UNINDEXED,
            title,
            content,
            tokenize='porter'
        );
    """)


# =============================================================================
# STEP 3: File Finding Functions
# =============================================================================

def should_skip_file(file_path):
    """Check if we should skip this file"""
    # Skip if it's in a folder we want to ignore
    for part in file_path.parts:
        if part in SKIP_FOLDERS:
            return True

    # Only process .md and .rst files
    if file_path.suffix.lower() not in [".md", ".rst"]:
        return True

    # Skip the root README.md (but keep READMEs in subfolders)
    if file_path.name == "README.md":
        # Check if it's directly in the root (not in a subfolder)
        if len(file_path.parts) <= 2:  # Simple check
            return True

    return False


def find_all_docs(root_folder):
    """Find all markdown and RST files in the folder"""
    root = pathlib.Path(root_folder).resolve()
    doc_files = []

    # Look through all files in the folder and subfolders
    for file_path in root.rglob("*"):
        # Skip if not a file
        if not file_path.is_file():
            continue

        # Skip if we should ignore this file
        if should_skip_file(file_path):
            continue

        doc_files.append(file_path)

    return doc_files


def get_relative_path(root_folder, file_path):
    """Get the path relative to the root (e.g. 'docs/intro.md')"""
    root = pathlib.Path(root_folder).resolve()
    full_path = file_path.resolve()
    relative = full_path.relative_to(root)
    return relative.as_posix()  # Convert to 'docs/intro.md' format


# =============================================================================
# STEP 4: MCP Tools (What agents can call)
# =============================================================================

@server.tool(
    name="reindex",
    description="Scan all .md and .rst files and add them to the search database"
)
def reindex(root: str = ".") -> str:
    """
    Rebuild the search index from all documentation files.

    This will:
    1. Find all .md and .rst files
    2. Read their content
    3. Add them to the search database

    Args:
        root: Folder to search (default is current folder)

    Returns:
        A message saying how many files were indexed
    """
    print(f"Starting to index files in: {root}")

    # Connect to database
    connection = connect_to_database()
    cursor = connection.cursor()

    # Create fresh search table
    create_search_table(cursor)

    # Find all documentation files
    root_folder = pathlib.Path(root).resolve()
    doc_files = find_all_docs(root_folder)

    print(f"Found {len(doc_files)} files to index")

    # Read each file and prepare for database
    rows_to_insert = []
    for file_path in doc_files:
        try:
            # Read the file content
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            # Prepare data for database
            relative_path = get_relative_path(root_folder, file_path)
            title = file_path.stem  # Filename without extension

            rows_to_insert.append((relative_path, title, content))

            print(f"  OK - Indexed: {relative_path}")

        except Exception as error:
            print(f"  X - Skipped {file_path.name}: {error}")
            continue

    # Insert all files into database
    if rows_to_insert:
        cursor.executemany(
            "INSERT INTO docs(path, title, content) VALUES(?, ?, ?)",
            rows_to_insert
        )

    # Save changes and close database
    connection.commit()
    connection.close()

    # Return summary
    result = f"Successfully indexed {len(rows_to_insert)} files from {root_folder}"
    print(result)
    return result


@server.tool(
    name="search",
    description="Search the documentation. Returns JSON with matching documents."
)
def search(query: str, k: int = 8) -> str:
    """
    Search for documentation matching your query.

    Args:
        query: What to search for (e.g., "capitalize headings")
        k: Maximum number of results to return (default: 8)

    Returns:
        JSON array with search results including:
        - id: Document ID
        - title: Document title
        - path: File path
        - snippet: Preview with matching terms highlighted in [brackets]
        - resource_uri: Link to get full document
    """
    print(f"Searching for: {query}")

    # Connect to database
    connection = connect_to_database()
    connection.row_factory = sqlite3.Row  # Makes results easier to work with
    cursor = connection.cursor()

    # Search the database
    cursor.execute("""
        SELECT
            rowid,
            path,
            title,
            snippet(docs, 2, '[', ']', ' … ', 12) AS snippet
        FROM docs
        WHERE docs MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, k))

    # Collect results
    results = []
    for row in cursor.fetchall():
        doc_id = int(row["rowid"])
        results.append({
            "id": doc_id,
            "title": row["title"],
            "path": row["path"],
            "snippet": row["snippet"],
            "resource_uri": f"doc://by-id/{doc_id}"
        })

    # Close database
    connection.close()

    print(f"Found {len(results)} results")

    # Return as pretty JSON
    return json.dumps(results, indent=2, ensure_ascii=False)


@server.resource("doc://by-id/{rowid}")
def get_full_document(rowid: int) -> str:
    """
    Get the full content of a document by its ID.

    This is called when an agent wants to see the complete document,
    not just the snippet from search results.

    Args:
        rowid: The document ID from search results

    Returns:
        Full document content as text
    """
    print(f"Fetching full document: {rowid}")

    # Connect to database
    connection = connect_to_database()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Get the document
    row = cursor.execute(
        "SELECT content FROM docs WHERE rowid=?",
        (rowid,)
    ).fetchone()

    # Close database
    connection.close()

    # Return content or error
    if not row:
        raise FileNotFoundError(f"Document with ID {rowid} not found")

    return row["content"]


# =============================================================================
# STEP 5: Start the Server
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Style Guide MCP Server")
    print("=" * 60)
    print(f"Database location: {database_file}")
    print()
    print("Available tools:")
    print("  1. reindex - Build the search index")
    print("  2. search - Search the documentation")
    print()
    print("Available resources:")
    print("  - doc://by-id/{id} - Get full document content")
    print("=" * 60)

    # Start the MCP server
    server.run(transport="stdio")

