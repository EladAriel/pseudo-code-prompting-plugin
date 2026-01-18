#!/usr/bin/env python3
"""
Semantic Pattern Router for Claude Code Caching System
Matches user queries to cached patterns using Claude API
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

try:
    from anthropic import Anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)


class SemanticRouter:
    """Routes user queries to cached patterns using semantic matching"""

    def __init__(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.cache_dir = self.plugin_dir / ".claude" / "prompt_cache"
        self.registry_path = self.cache_dir / "registry.json"
        self.log_dir = Path.home() / ".claude" / "logs"
        self.log_file = self.log_dir / "semantic_router.log"

        # API configuration
        self.model = "claude-3-haiku-20240307"
        self.max_tokens = 100
        self.temperature = 0.1
        self.timeout = 10

    def log(self, message, level="INFO"):
        """Log messages to file with timestamp"""
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().isoformat()
            log_entry = f"[{timestamp}] [{level}] {message}\n"
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"WARNING: Failed to write log: {e}", file=sys.stderr)

    def validate_api_key(self):
        """Check if API key exists in environment"""
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            self.log("ANTHROPIC_API_KEY not found in environment", "ERROR")
            print("ERROR: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
            return False
        return True

    def load_registry(self):
        """Load pattern registry from disk"""
        try:
            if not self.registry_path.exists():
                self.log("Registry not found, creating empty registry", "INFO")
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                empty_registry = {
                    "patterns": [],
                    "version": "1.0",
                    "metadata": {
                        "created_at": datetime.now().isoformat(),
                        "last_modified": datetime.now().isoformat(),
                        "pattern_count": 0
                    }
                }
                with open(self.registry_path, 'w', encoding='utf-8') as f:
                    json.dump(empty_registry, f, indent=2)
                return empty_registry

            with open(self.registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)

            # Validate schema
            if not isinstance(registry.get('patterns'), list):
                raise ValueError("Invalid registry: 'patterns' must be an array")

            self.log(f"Loaded registry with {len(registry['patterns'])} patterns", "INFO")
            return registry

        except json.JSONDecodeError as e:
            self.log(f"Registry corrupted: {e}", "ERROR")
            print("ERROR: Registry file corrupted", file=sys.stderr)
            return None
        except Exception as e:
            self.log(f"Failed to load registry: {e}", "ERROR")
            print(f"ERROR: {e}", file=sys.stderr)
            return None

    def extract_lightweight_index(self, registry):
        """Extract only tag_id, description, usage_count, and query_type for prompt"""
        patterns = registry.get('patterns', [])

        # Sort by usage_count descending, limit to 50 patterns
        sorted_patterns = sorted(
            patterns,
            key=lambda p: p.get('stats', {}).get('usage_count', 0),
            reverse=True
        )[:50]

        index = []
        for pattern in sorted_patterns:
            query_type = pattern.get('metadata', {}).get('query_type', 'regular')
            index.append({
                'tag_id': pattern.get('tag_id', ''),
                'description': pattern.get('description', ''),
                'usage_count': pattern.get('stats', {}).get('usage_count', 0),
                'query_type': query_type,
                'weight': 1.5 if query_type == 'optimized' else 1.0
            })

        return index

    def construct_prompt(self, patterns, user_query):
        """Build prompt for semantic matching with optimized pattern scoring"""
        if not patterns:
            return None

        pattern_list = "\n".join([
            f"- {p['tag_id']} [{p['query_type']}] (weight: {p['weight']}x, used {p['usage_count']} times): {p['description']}"
            for p in patterns
        ])

        prompt = f"""You are a semantic pattern matcher for a caching system.

Available cached patterns:
{pattern_list}

User query: {user_query}

Task: Determine if any cached pattern matches the user's intent.

Rules:
- Regular patterns require >70% semantic similarity
- Optimized patterns (marked with [optimized]) require only >65% similarity and have 1.5x priority
- Return ONLY the tag_id if confident match
- Return "None" if no good match
- Consider synonyms and related concepts
- When multiple patterns match, prefer optimized patterns (higher weight)
- Prioritize patterns with higher usage_count within same weight class

Output format: tag_id
Example outputs: "auth_google_oauth" or "None"
"""
        return prompt

    def call_claude_api(self, prompt):
        """Make API call to Claude for semantic matching"""
        try:
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            if not api_key:
                return None

            client = Anthropic(api_key=api_key, timeout=self.timeout)

            start_time = datetime.now()

            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            self.log(f"API call completed in {elapsed:.0f}ms", "INFO")

            result = response.content[0].text.strip()
            return result

        except Exception as e:
            self.log(f"API call failed: {e}", "ERROR")
            return None

    def validate_tag_exists(self, tag_id, registry):
        """Verify the returned tag_id exists in registry"""
        if tag_id == "None" or not tag_id:
            return False

        patterns = registry.get('patterns', [])
        for pattern in patterns:
            if pattern.get('tag_id') == tag_id:
                # Verify file actually exists
                pattern_file = self.cache_dir / "patterns" / f"{tag_id}.md"
                if pattern_file.exists():
                    return True
                else:
                    self.log(f"Tag {tag_id} found in registry but file missing", "WARNING")
                    return False

        return False

    def route(self, user_query):
        """Main routing logic"""
        # Validate API key
        if not self.validate_api_key():
            return "None"

        # Load registry
        registry = self.load_registry()
        if not registry:
            return "None"

        # Check if registry is empty
        if not registry.get('patterns'):
            self.log("No patterns in cache", "INFO")
            return "None"

        # Extract lightweight index
        patterns = self.extract_lightweight_index(registry)
        if not patterns:
            self.log("No patterns available after indexing", "INFO")
            return "None"

        # Construct prompt
        prompt = self.construct_prompt(patterns, user_query)
        if not prompt:
            return "None"

        # Call API
        self.log(f"Querying semantic match for: {user_query[:100]}", "INFO")
        result = self.call_claude_api(prompt)

        if not result:
            self.log("API call returned no result", "WARNING")
            return "None"

        # Clean up result (remove quotes, whitespace)
        result = result.strip().strip('"').strip("'")

        # Validate result
        if result == "None" or result.lower() == "none":
            self.log("No semantic match found", "INFO")
            return "None"

        # Verify tag exists
        if self.validate_tag_exists(result, registry):
            self.log(f"Match found: {result}", "INFO")
            return result
        else:
            self.log(f"Invalid tag returned: {result}", "WARNING")
            return "None"


def main():
    """Entry point"""
    if len(sys.argv) < 2:
        print("ERROR: No user query provided", file=sys.stderr)
        print("Usage: find_tag.py <user_query>", file=sys.stderr)
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])

    router = SemanticRouter()
    result = router.route(user_query)

    # Output only the result (tag_id or "None")
    print(result)
    sys.exit(0)


if __name__ == "__main__":
    main()
