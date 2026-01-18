# Semantic Caching System

The Pseudo-Code Prompting plugin includes an intelligent semantic caching system that dramatically reduces API costs and response times by reusing previously generated patterns.

## Overview

### What is Semantic Caching?

Traditional caching systems require exact text matches. Semantic caching uses AI to understand the **meaning** of your query and matches it to similar previously-generated patterns, even if the wording is completely different.

**Example**:
- **Query 1**: "Implement Google OAuth authentication"
- **Query 2**: "Add Google login with OAuth 2.0"
- **Result**: Semantic match! Both queries have the same intent.

### Benefits

- **10x Cost Reduction**: Cache hits skip expensive generation phases
- **2-5x Faster Responses**: Loading from disk is faster than API generation
- **Consistent Patterns**: Reuse proven, tested implementations
- **Learning System**: Cache gets smarter as you use it more

### Architecture

```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Semantic Router     │ ◄── Claude Haiku API
│ (find_tag.py)       │     (fast, cheap)
└────────┬────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Match      No Match
    │         │
    │         ▼
    │    ┌──────────────────┐
    │    │ Generate Pattern │ ◄── Full Claude API
    │    │ (transform-query)│     (expensive)
    │    └──────────────────┘
    │
    ▼
┌──────────────────┐
│ Load from Cache  │
│ (.md file)       │
└──────────────────┘
```

## Quick Start

### 1. Setup

Install the required Python package:

```bash
pip install anthropic
```

Set your API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 2. Cache Your First Pattern

Generate a pseudo-code pattern as usual:

```bash
/transform-query implement user authentication with JWT
```

After getting the result, cache it for future use:

```bash
./hooks/cache/cache-success.sh
```

Follow the prompts:
1. Paste the generated pattern
2. Enter a tag name (e.g., `auth_jwt`)
3. Enter a description (e.g., "JWT authentication implementation")

### 3. Use Cached Patterns

Next time you need authentication:

```bash
/transform-query add JWT-based user login
```

If the semantic router recognizes the similarity, you'll see:

```
📦 Loaded cached pattern: auth_jwt
```

The cached pattern is returned **instantly** without generating a new one.

## Commands

### Cache Management

#### Save Pattern to Cache

```bash
./hooks/cache/cache-success.sh
```

Interactive script to save a pattern. You'll be prompted for:
- **Tag ID**: Unique identifier (lowercase, underscores, e.g., `auth_google_oauth`)
- **Description**: Semantic description for matching (e.g., "Google OAuth 2.0 authentication")

**Tips**:
- Use descriptive tag names that indicate what the pattern does
- Write descriptions that capture the intent, not implementation details
- Good: "Implements Google OAuth 2.0 authentication flow"
- Bad: "Code for auth"

#### List Cached Patterns

```bash
./hooks/cache/list-cache.sh
```

Displays all cached patterns with statistics:

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                         Cached Patterns                                        ║
╚════════════════════════════════════════════════════════════════════════════════╝

TAG ID                         USES       LAST USED            DESCRIPTION
────────────────────────────── ────────── ──────────────────── ────────────────────
auth_google_oauth              23         2026-01-15           Google OAuth 2.0 auth
api_rest_crud                  18         2026-01-14           REST API CRUD endpoints
database_postgres_setup        12         2026-01-13           PostgreSQL setup config

Total patterns: 3
```

#### Search Patterns

```bash
./hooks/cache/search-cache.sh <query>
```

Search patterns by tag or description:

```bash
./hooks/cache/search-cache.sh oauth
```

#### View Cache Statistics

```bash
./hooks/cache/cache-stats.sh
```

Shows comprehensive cache metrics:

```
╔════════════════════════════════════════════════════════════════╗
║              Semantic Cache Statistics                        ║
╚════════════════════════════════════════════════════════════════╝

Total Patterns:        15
Total Uses:            247
Average Uses:          16.47
Total Cache Size:      2.34 MB
Last Modified:         2026-01-15

═══════════════════════════════════════════════════════════════
  Top 5 Most Used Patterns
═══════════════════════════════════════════════════════════════

TAG ID                         USES       DESCRIPTION
────────────────────────────── ────────── ────────────────────
auth_google_oauth              23         Google OAuth 2.0 auth
api_rest_crud                  18         REST API endpoints
...
```

#### Delete Pattern

```bash
./hooks/cache/delete-cache.sh <tag_id>
```

Removes a pattern from cache (creates backup first):

```bash
./hooks/cache/delete-cache.sh auth_google_oauth
```

#### Update Pattern

```bash
./hooks/cache/update-cache.sh <tag_id>
```

Update an existing pattern with new content. Automatically:
- Backs up the current version
- Increments the version number
- Updates metadata

#### Validate Cache Integrity

```bash
./hooks/cache/validate-cache.sh
```

Checks cache health:
- Registry JSON validity
- Missing pattern files
- Orphaned files
- File size consistency
- Directory structure

## How It Works

### Semantic Router

The semantic router (`find_tag.py`) uses Claude Haiku to match queries to cached patterns:

1. **Loads lightweight index** from `registry.json` (only tag IDs and descriptions)
2. **Constructs prompt** with available patterns and user query
3. **Calls Claude Haiku** (<500 tokens, fast and cheap)
4. **Returns match** or "None"

**Cost**: ~$0.0001 per lookup (vs ~$0.01+ for full generation)

### Registry Structure

The registry (`registry.json`) is the central index:

```json
{
  "patterns": [
    {
      "tag_id": "auth_google_oauth",
      "description": "Google OAuth 2.0 authentication implementation",
      "file_path": "patterns/auth_google_oauth.md",
      "stats": {
        "usage_count": 23,
        "last_used": "2026-01-15T10:30:00Z",
        "created_at": "2026-01-10T14:20:00Z",
        "file_size_bytes": 4521
      },
      "metadata": {
        "tags": [],
        "author": "username",
        "version": "1.0"
      }
    }
  ],
  "version": "1.0",
  "metadata": {
    "created_at": "2026-01-10T14:20:00Z",
    "last_modified": "2026-01-15T10:30:00Z",
    "pattern_count": 1
  }
}
```

### Pattern Files

Patterns are stored as markdown files in `.claude/prompt_cache/patterns/`:

```
.claude/
└── prompt_cache/
    ├── registry.json          # Central index
    ├── patterns/              # Pattern files
    │   ├── auth_google_oauth.md
    │   ├── api_rest_crud.md
    │   └── database_postgres_setup.md
    └── backups/               # Automatic backups
        └── auth_google_oauth_v1.0_20260115_103000.md
```

## Integration with Transform-Query

The caching system is **automatically integrated** with the `/transform-query` command:

### Cache Hit Flow

```
User: /transform-query implement Google OAuth
   ↓
Step 0: Semantic Cache Lookup
   ↓
Router: Match found → auth_google_oauth
   ↓
Load: .claude/prompt_cache/patterns/auth_google_oauth.md
   ↓
Output: 📦 Loaded cached pattern: auth_google_oauth
   ↓
Return cached content (Steps 1-2 skipped)
```

### Cache Miss Flow

```
User: /transform-query create a new feature X
   ↓
Step 0: Semantic Cache Lookup
   ↓
Router: No match found
   ↓
💡 Tip: Use '/cache-success' to save this for reuse
   ↓
Step 1: Context-Aware Mode Check
   ↓
Step 2: Generate Transformation (full API call)
   ↓
Output: Generated pseudo-code
```

## Performance Optimization

### Cost Savings

**Scenario**: You frequently implement authentication features

- **Without Cache**:
  - 10 auth requests × $0.01 per generation = **$0.10**

- **With Cache** (after first generation):
  - 1st request: $0.01 (generation)
  - 9 requests: 9 × $0.0001 (semantic lookup) = **$0.0009**
  - **Total: $0.0109** (~90% savings)

### Speed Improvements

- **Cache Hit**: ~2 seconds (API call + disk read)
- **Cache Miss**: ~10-30 seconds (tree generation + transformation)
- **Improvement**: **5-15x faster**

### Token Minimization

The semantic router is optimized for minimal token usage:

- **Only loads metadata** (not full pattern content)
- **Limits to top 50 patterns** by usage count
- **Uses Claude Haiku** (cheapest model)
- **Target**: <500 tokens per router call

## Advanced Features

### Automatic Usage Tracking

Every cache hit automatically:
- Increments `usage_count`
- Updates `last_used` timestamp
- Informs future semantic matching (popular patterns prioritized)

### Concurrency Safety

All registry updates use:
- **File locking** to prevent race conditions
- **Atomic writes** (write to temp, then rename)
- **Stale lock detection** (auto-cleanup after 60s)

### Backup System

Automatic backups are created:
- When overwriting patterns
- When deleting patterns
- Before cache repairs

Backups stored in `.claude/prompt_cache/backups/`

### Graceful Degradation

The cache system never blocks normal operation:
- API failures → proceed as cache miss
- Router timeout → proceed as cache miss
- Registry corrupted → auto-repair from patterns directory
- Missing dependencies → skip cache, proceed normally

## Best Practices

### When to Cache

✅ **Cache these**:
- Frequently used patterns (authentication, CRUD, setup)
- Complex configurations (database, deployment, CI/CD)
- Boilerplate code (API endpoints, middleware, models)
- Architecture patterns (MVC, microservices, event-driven)

❌ **Don't cache these**:
- One-off implementations
- Highly project-specific code
- Simple queries
- Rapidly changing requirements

### Writing Good Descriptions

The description is crucial for semantic matching.

**Good descriptions**:
- "Implements Google OAuth 2.0 authentication with refresh tokens"
- "Creates RESTful CRUD API endpoints with validation"
- "Sets up PostgreSQL with connection pooling and migrations"

**Bad descriptions**:
- "Auth code"
- "API stuff"
- "Database"

**Tips**:
- Include the technology/framework
- Mention key features
- Use action verbs (implements, creates, sets up)
- Be specific but not too narrow

### Tag Naming Conventions

Use descriptive, hierarchical tag names:

```
auth_google_oauth
auth_jwt_basic
auth_jwt_refresh_tokens
api_rest_crud
api_graphql_setup
database_postgres_setup
database_postgres_migrations
deploy_docker_nginx
deploy_kubernetes_basic
```

Pattern: `<domain>_<technology>_<specific_feature>`

## Troubleshooting

### Cache Not Working

**Issue**: Queries don't match cached patterns

**Solutions**:
1. Check API key: `echo $ANTHROPIC_API_KEY`
2. Verify Python installed: `python3 --version`
3. Check logs: `tail -f ~/.claude/logs/semantic_router.log`
4. Validate cache: `./hooks/cache/validate-cache.sh`

### Registry Corrupted

**Issue**: Cache validation shows JSON errors

**Solution**: Run validation script with auto-repair:

```bash
./hooks/cache/validate-cache.sh
```

The system will automatically:
1. Backup corrupted registry
2. Rebuild from pattern files
3. Restore all valid patterns

### Semantic Router Timeout

**Issue**: Cache lookups taking too long

**Causes**:
- Too many patterns (>50 slows down)
- Network issues with Anthropic API
- Large registry file

**Solutions**:
1. Delete unused patterns: `./hooks/cache/delete-cache.sh <tag>`
2. Check network connection
3. Increase timeout in `find_tag.sh` (line with `timeout 15s`)

### Permissions Errors

**Issue**: Cannot write to cache directory

**Solution**:

```bash
chmod -R 755 .claude/prompt_cache
```

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Required for semantic routing
- `SEMANTIC_CACHE_DEBUG=1`: Enable verbose logging

### File Locations

- **Registry**: `.claude/prompt_cache/registry.json`
- **Patterns**: `.claude/prompt_cache/patterns/*.md`
- **Backups**: `.claude/prompt_cache/backups/`
- **Logs**: `~/.claude/logs/semantic_router.log`

### Limits

- **Max patterns**: 500 (recommended <100 for best performance)
- **Max pattern size**: 5MB
- **Max description length**: 500 characters
- **Router timeout**: 15 seconds
- **Lock timeout**: 5 seconds

## API Reference

### find_tag.py

**Synopsis**:
```bash
python3 hooks/find_tag.py "<user_query>"
```

**Output**:
- `<tag_id>` - Match found
- `None` - No match
- `ERROR:<message>` - Error occurred

**Exit Codes**:
- `0` - Success
- `1` - Error

### find_tag.sh

**Synopsis**:
```bash
bash hooks/find_tag.sh "<user_query>"
```

Wrapper script that:
1. Validates environment
2. Calls `find_tag.py`
3. Updates usage statistics on cache hit
4. Handles errors gracefully

### cache-success.sh

**Synopsis**:
```bash
./hooks/cache/cache-success.sh
```

Interactive script for saving patterns. Reads from stdin.

**Workflow**:
1. Captures content from stdin
2. Prompts for tag name
3. Sanitizes input
4. Checks for collisions
5. Saves pattern file
6. Updates registry

## Examples

### Example 1: Authentication Pattern

**Save pattern**:

```bash
# Generate authentication pattern
/transform-query implement JWT authentication with refresh tokens

# Cache the result
./hooks/cache/cache-success.sh
# Tag: auth_jwt_refresh
# Description: JWT authentication with access and refresh tokens
```

**Later usage**:

```bash
/transform-query add JWT login with token refresh
# 📦 Loaded cached pattern: auth_jwt_refresh
```

### Example 2: API Endpoints

**Save pattern**:

```bash
# Generate CRUD API
/transform-query create REST API with CRUD operations

# Cache it
./hooks/cache/cache-success.sh
# Tag: api_rest_crud
# Description: RESTful CRUD API endpoints with validation
```

**Later usage**:

```bash
/transform-query add REST endpoints for user management
# 📦 Loaded cached pattern: api_rest_crud
```

### Example 3: Database Setup

**Save pattern**:

```bash
# Generate database config
/transform-query setup PostgreSQL with connection pooling

# Cache it
./hooks/cache/cache-success.sh
# Tag: database_postgres_pool
# Description: PostgreSQL database setup with connection pooling and error handling
```

**Later usage**:

```bash
/transform-query configure Postgres database connection
# 📦 Loaded cached pattern: database_postgres_pool
```

## FAQs

### Q: Do I need to use exact keywords for cache hits?

**A**: No! That's the power of semantic matching. "implement OAuth" and "add Google login" can match the same pattern if the semantic meaning is similar.

### Q: How much does semantic routing cost?

**A**: About $0.0001 per lookup using Claude Haiku. Compare this to $0.01+ for full pattern generation.

### Q: Can I share cached patterns with my team?

**A**: Yes! Commit `.claude/prompt_cache/` to your repository. Team members will automatically benefit from cached patterns.

### Q: What happens if the API is down?

**A**: The system gracefully degrades. Cache lookups fail silently, and the normal generation flow proceeds without interruption.

### Q: Can I edit cached patterns manually?

**A**: Yes! Patterns are plain markdown files. Edit them directly or use `./hooks/cache/update-cache.sh <tag>`.

### Q: How do I clear the entire cache?

**A**: Delete the cache directory:
```bash
rm -rf .claude/prompt_cache
```

On next use, it will automatically reinitialize.

## Support

### Logs

Check logs for debugging:

```bash
# Semantic router logs
tail -f ~/.claude/logs/semantic_router.log

# General cache logs
tail -f ~/.claude/logs/semantic_cache.log
```

### Validation

Run integrity check:

```bash
./hooks/cache/validate-cache.sh
```

### Stats

View cache metrics:

```bash
./hooks/cache/cache-stats.sh
```

## Contributing

Found a bug or have a feature request? Please file an issue in the repository.

## License

Same as the Pseudo-Code Prompting Plugin license.
