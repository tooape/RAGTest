---
version: 1
pageType: claudeMemory
created: 2025-08-05
aliases:
  - Obsidian MCP Commands
tags:
  - claude
---

# MCP Tools Reference
---

Comprehensive reference for MCP tools available through the Obsidian MCP Tools plugin.

## Server Information

### `mcp__obsidian-mcp-tools__get_server_info`
Returns basic details about the Obsidian Local REST API and authentication status. This is the only API request that does not require authentication.

## Active File Operations

### `mcp__obsidian-mcp-tools__get_active_file`
Returns the content of the currently active file in Obsidian. Can return either markdown content or a JSON representation including parsed tags and frontmatter.

**Parameters:**
- `format`: "json" or "markdown" (optional)

### `mcp__obsidian-mcp-tools__update_active_file`
Update the content of the active file open in Obsidian.

**Parameters:**
- `content`: The new content (required)

### `mcp__obsidian-mcp-tools__append_to_active_file`
Append content to the end of the currently-open note.

**Parameters:**
- `content`: Content to append (required)

### `mcp__obsidian-mcp-tools__patch_active_file`
Insert or modify content in the currently-open note relative to a heading, block reference, or frontmatter field.

**Parameters:**
- `content`: The actual content to insert, append, or use as replacement (required)
- `operation`: "append", "prepend", or "replace" (required)
- `target`: The identifier - heading path, block reference ID, or frontmatter field name (required)
- `targetType`: "heading", "block", or "frontmatter" (required)
- `contentType`: "application/json" or "text/markdown" (optional)
- `targetDelimiter`: Separator for heading paths, default "::" (optional)
- `trimTargetWhitespace`: Remove whitespace from target identifier, default false (optional)

### `mcp__obsidian-mcp-tools__delete_active_file`
Delete the currently-active file in Obsidian.

## Vault File Operations

### `mcp__obsidian-mcp-tools__show_file_in_obsidian`
Open a document in the Obsidian UI. Creates a new document if it doesn't exist. Returns a confirmation if the file was opened successfully.

**Parameters:**
- `filename`: The file to open (required)
- `newLeaf`: Open in new leaf/tab (optional)

### `mcp__obsidian-mcp-tools__list_vault_files`
List files in the root directory or a specified subdirectory of your vault.

**Parameters:**
- `directory`: Directory to list (optional, defaults to root)

### `mcp__obsidian-mcp-tools__get_vault_file`
Get the content of a file from your vault.

**Parameters:**
- `filename`: The file to read (required)
- `format`: "json" or "markdown" (optional)

### `mcp__obsidian-mcp-tools__create_vault_file`
Create a new file in your vault or update an existing one.

**Parameters:**
- `filename`: The file path (required)
- `content`: File content (required)

### `mcp__obsidian-mcp-tools__append_to_vault_file`
Append content to a new or existing file.

**Parameters:**
- `filename`: The file path (required)
- `content`: Content to append (required)

### `mcp__obsidian-mcp-tools__patch_vault_file`
Insert or modify content in a file relative to a heading, block reference, or frontmatter field.

**Parameters:**
- `filename`: The file to modify (required)
- `content`: The actual content to insert, append, or use as replacement (required)
- `operation`: "append", "prepend", or "replace" (required)
- `target`: The identifier - heading path, block reference ID, or frontmatter field name (required)
- `targetType`: "heading", "block", or "frontmatter" (required)
- `contentType`: "application/json" or "text/markdown" (optional)
- `targetDelimiter`: Separator for heading paths, default "::" (optional)
- `trimTargetWhitespace`: Remove whitespace from target identifier, default false (optional)

### `mcp__obsidian-mcp-tools__delete_vault_file`
Delete a file from your vault.

**Parameters:**
- `filename`: The file to delete (required)

## Search Operations

### `mcp__obsidian-mcp-tools__search_vault`
Search for documents matching a specified query using either Dataview DQL or JsonLogic.

**Parameters:**
- `query`: The search query (required)
- `queryType`: "dataview" or "jsonlogic" (required)

### `mcp__obsidian-mcp-tools__search_vault_simple`
Search for documents matching a text query.

**Parameters:**
- `query`: The search text (required)
- `contextLength`: Number of context characters (optional)

### `mcp__obsidian-mcp-tools__search_vault_smart`
Search for documents semantically matching a text string.

**Parameters:**
- `query`: A search phrase for semantic search (required)
- `filter`: Object with optional properties:
  - `folders`: Array of folder names to include
  - `excludeFolders`: Array of folder names to exclude
  - `limit`: Maximum number of results

## Template Operations

### `mcp__obsidian-mcp-tools__execute_template`
Execute a Templater template with the given arguments.

**Parameters:**
- `name`: The full vault path to the template file (required)
- `arguments`: Object with string key-value pairs for template variables (required)
- `createFile`: "true" or "false" (optional)
- `targetPath`: Path to save the file; required if createFile is true (optional)

## Web Integration

### `mcp__obsidian-mcp-tools__fetch`
Reads and returns the content of any web page. Returns the content in Markdown format by default, or can return raw HTML if raw=true parameter is set. Supports pagination through maxLength and startIndex parameters.

**Parameters:**
- `url`: The URL to fetch (required)
- `raw`: Returns raw HTML content if true (optional)
- `maxLength`: Limit response length (optional)
- `startIndex`: Supports paginated retrieval of content (optional)

## Usage Guidelines

### Search Strategy
1. **Semantic Search** (`search_vault_smart`): Best for concept discovery and cross-cutting themes
2. **Simple Search** (`search_vault_simple`): Best for specific keywords or exact phrases
3. **Advanced Search** (`search_vault`): Best for complex queries using Dataview DQL

### File Operations Best Practices
- Use `patch_vault_file` for targeted edits under specific headings
- Use `append_to_vault_file` for adding new content to existing notes
- Use `create_vault_file` only when creating entirely new files
- Always check if files exist before creating to avoid overwrites

### Template Integration
- Store templates in a dedicated Templates folder
- Use clear parameter names in template arguments
- Test templates manually before automating with `execute_template`

### Web Content Integration
- Use `fetch` to bring external content into vault workflows
- Consider content length when fetching large pages
- Use raw=false (default) for clean Markdown conversion