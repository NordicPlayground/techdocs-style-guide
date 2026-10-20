# Nordic TechDocs Style Guide

The Nordic TechDocs Style Guide is the authoritative reference for technical writing at Nordic Semiconductor. It provides guidelines on grammar, style, content structure, procedures, and formatting for all externally published documentation.

## Sources and hierarchy

This guide consolidates rules from multiple sources. When sources conflict, follow this precedence:

1. **This style guide** (takes precedence)
2. [Merriam-Webster dictionary](https://www.merriam-webster.com/) (spelling and usage)

The guide was originally forked from the [Microsoft Style Guide](https://github.com/MicrosoftDocs/microsoft-style-guide/tree/main/styleguide) and has since been substantially expanded with Nordic-specific guidelines and industry best practices.

## Style guide repository

[Nordic TechDocs Style Guide](https://github.com/NordicPlayground/techdocs-style-guide) is the official repository for the guide.

## What is covered

* **Grammar and style** — Sentence structure, verbs, clauses, nouns, pronouns, modifiers, person
* **Content structure** — Headings, lists, tables, links, cross-references, error messages, notes and admonitions, modular writing, organization schemes, illustrations
* **Procedures and instructions** — Step-by-step instructions, task hierarchy, task organization, UI interactions, procedure review
* **Writing tips** — Accessibility, bias-free communication, internationalization, scannable writing, online writing, reader-focused writing, jargon, anthropomorphisms, redundancies
* **Punctuation** — Commas, dashes and hyphens, parentheses, apostrophes, colons, semicolons, and more
* **Planning** — Content planning, design planning, document types, editorial process, legal guidelines, release notes (including nRF Connect SDK conventions)
* **Reference** — Acronyms, glossary, capitalization, numbers, units of measurement, typographic conventions, trademarks, product names, URLs

## MkDocs framework

We use the [MkDocs framework](https://www.mkdocs.org) with the [Material](https://squidfunk.github.io/mkdocs-material) theme to build the static documentation site.

## How to view the style guide

### Step 1: Create a virtual environment

Create a folder and set up a Python virtual environment:

```bash
python -m venv venv
```

### Step 2: Activate the virtual environment

=== "Linux / macOS"

    ```bash
    source venv/bin/activate
    ```

=== "Windows"

    ```bash
    venv\Scripts\activate
    ```

### Step 3: Install dependencies

```bash
pip install mkdocs mkdocs-material mkdocs-macros-plugin
```

Optionally, install the MCP server dependencies:

```bash
pip install mcp fastmcp
```

### Step 4: Clone the repository

```bash
git clone https://https://github.com/NordicPlayground/techdocs-style-guide
```

### Step 5: Preview the documentation

Navigate to the `techdocs-style-guide` directory and run:

```bash
mkdocs serve
```

The site is available at `http://127.0.0.1:8000`. Press **Ctrl+C** to stop the server.

### Step 6: Build the static site

To build the documentation for deployment:

```bash
mkdocs build
```

The output is written to the `site/` directory. Use `--strict` to catch broken links and other issues:

```bash
mkdocs build --strict
```

### Step 7: Deactivate the virtual environment

```bash
deactivate
```

## MCP server

This repository includes an MCP server, `tools/tiny_docs_mcp.py`, that serves the style guide documentation to AI tools via full-text search.

The server uses an SQLite FTS5 index (`docs_index.db`) and exposes four capabilities:

* **`reindex`** -- rebuild the search index from all `.md` files in the docs directory
* **`search`** -- full-text search returning matching documents with snippets
* **`read_doc`** -- tool that returns the full content of a search result by its `id`
* **`doc://by-id/{id}`** -- resource to fetch the full content of a search result

### Initial setup

Before using the MCP server for the first time, you must build the search index. Call the `reindex` tool with the docs directory as the root, or run it manually:

```bash
cd techdocs-style-guide
python tools/tiny_docs_mcp.py
```

Then call the `reindex` tool from your AI client. Reindex again after adding or modifying documentation files.

### Use with Cursor

Add the following to your `mcp.json`:

```json
{
  "mcpServers": {
    "nordic-style-guide": {
      "command": "path/to/venv/python",
      "args": [
        "/path/to/techdocs-style-guide/tools/tiny_docs_mcp.py"
      ],
      "cwd": "/path/to/techdocs-style-guide"
    }
  }
}
```

Use this as the basis for either your workspace or system-wide MCP configuration. You can also add this through **File > Preferences > Cursor Settings > Tools and MCP**.

Restart Cursor after adding the configuration.

### Use with VS Code

Add the following to your `.vscode/mcp.json` in the workspace root:

```json
{
  "servers": {
    "nordic-style-guide": {
      "command": "path/to/venv/python",
      "args": [
        "/path/to/techdocs-style-guide/tools/tiny_docs_mcp.py"
      ],
      "cwd": "/path/to/techdocs-style-guide"
    }
  }
}
```

Alternatively, add it to your user settings (`settings.json`):

```json
{
  "mcp": {
    "servers": {
      "nordic-style-guide": {
        "command": "path/to/venv/python",
        "args": [
          "/path/to/techdocs-style-guide/tools/tiny_docs_mcp.py"
        ],
        "cwd": "/path/to/techdocs-style-guide"
      }
    }
  }
}
```

Reload the window after adding the configuration.
