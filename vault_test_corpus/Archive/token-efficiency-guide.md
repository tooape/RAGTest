# Token Efficiency Guide for Claude Code

## High-Impact Strategies

### 1. Batch Tool Calls (CRITICAL)
```
❌ Low Efficiency: 3 separate messages, 3 responses
Message 1: search for X
Message 2: search for Y  
Message 3: search for Z

✅ High Efficiency: 1 message, 1 response
Single message with 3 parallel tool calls
```

### 2. Strategic Search Patterns
```
❌ Token Heavy: Read entire files to find small details
✅ Token Light: Use targeted grep/search with specific patterns

❌ Broad: search_vault_simple "function"
✅ Targeted: grep with pattern "function.*processData" 
```

### 3. File Access Optimization
```
❌ Multiple file reads for context
✅ Use list_vault_files + targeted reads only when needed

❌ Read large files completely 
✅ Use search tools to find specific sections first
```

## Tool Efficiency Rankings

### Most Token-Efficient Tools:
1. `mcp__obsidian-mcp-tools__search_vault_simple` - minimal output
2. `mcp__obsidian-mcp-tools__list_vault_files` - structured, brief
3. `Grep` with `files_with_matches` mode - just filenames
4. `Bash` for simple commands - direct results

### Moderate Efficiency:
1. `mcp__obsidian-mcp-tools__search_vault_smart` - semantic but focused
2. `mcp__obsidian-mcp-tools__get_vault_file` - only when necessary
3. `Grep` with `content` mode - shows matching lines

### Use Sparingly:
1. Large file reads without specific targets
2. Multiple sequential searches for same information
3. Directory traversals without clear purpose

## Batching Examples

### Example 1: Research Task
```python
# Instead of 5 separate messages:
# ❌ search for "config"
# ❌ search for "settings"  
# ❌ search for "environment"
# ❌ list files in root
# ❌ check for package.json

# ✅ Single message with 5 parallel calls:
search_vault_simple("config")
search_vault_simple("settings")
search_vault_simple("environment") 
list_vault_files()
search_vault_simple("package.json")
```

### Example 2: File Analysis
```python
# ❌ Sequential approach (multiple responses):
# get file A → analyze → get file B → analyze → get file C

# ✅ Batch approach (single response):
get_vault_file("fileA.md")
get_vault_file("fileB.md") 
get_vault_file("fileC.md")
# Then analyze all in one response
```

## Token Conservation Tips

1. **Precise Questions**: Ask specific, focused questions
2. **Avoid Repeated Context**: Don't re-explain same information
3. **Use References**: Reference previous findings instead of re-searching
4. **Strategic Pauses**: Let me complete full tasks before new requests
5. **Batch Related Requests**: Group similar tasks together

## Usage Limit Maximization

- **Morning Strategy**: Start with complex, batch-heavy tasks
- **Midday Strategy**: Focus on targeted, specific operations  
- **Evening Strategy**: Simple maintenance and quick tasks

## Red Flags (Token Waste)
- Asking me to "explore" without specific goals
- Requesting broad overviews of large codebases
- Multiple similar searches with slight variations
- Back-and-forth clarification that could be avoided with precise initial requests