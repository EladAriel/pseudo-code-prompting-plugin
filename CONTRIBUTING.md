# Contributing to Pseudo-Code Prompting Plugin

Welcome to the Pseudo-Code Prompting Plugin for Claude Code! We're excited that you're interested in contributing. This plugin transforms natural language requirements into structured, validated pseudo-code using the PROMPTCONVERTER methodology.

## How to Contribute

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pseudo-code-prompting.git
   cd pseudo-code-prompting/pseudo-code-prompting-plugin
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/issue-description
   ```
4. **Make your changes** following the guidelines below
5. **Test your changes** thoroughly with Claude Code
6. **Submit a Pull Request** to the `main` branch

### Branch Naming Convention

- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring without functional changes

## Plugin Structure

```
pseudo-code-prompting-plugin/
├── .claude/
│   ├── agent-registry.json      # Agent coordination and workflows
│   ├── settings.json            # Hook configuration
│   ├── agents/                  # Agent definitions
│   │   ├── prompt-analyzer.md
│   │   ├── prompt-transformer.md
│   │   ├── requirement-validator.md
│   │   ├── prompt-optimizer.md
│   │   └── context-compressor.md
│   ├── commands/                # User-invocable commands
│   │   ├── transform-query.md
│   │   ├── validate-requirements.md
│   │   ├── optimize-prompt.md
│   │   └── compress-context.md
│   ├── hooks/                   # Lifecycle hooks
│   │   ├── user-prompt-submit.sh
│   │   ├── post-transform-validation.sh
│   │   └── context-compression-helper.sh
│   └── skills/                  # Skill definitions
│       ├── prompt-structurer/
│       ├── prompt-analyzer/
│       ├── prompt-optimizer/
│       ├── context-compressor/
│       └── requirement-validator/
├── .claude-plugin/             # Legacy plugin structure
├── plugin.json                 # Plugin metadata and configuration
├── README.md                   # Main documentation
├── SKILL.md                    # Quick reference guide
├── CHANGELOG.md                # Version history
└── CONTRIBUTING.md             # This file
```

## Adding New Skills

Skills provide specialized knowledge and patterns for transformation, validation, or optimization.

### Skill Structure

Each skill should have:
```
.claude/skills/your-skill-name/
├── capabilities.json           # Tier 1: Discovery (100 tokens)
├── SKILL.md                    # Tier 2: Overview (300-800 tokens)
├── references/                 # Tier 3: Specific patterns
│   └── *.md
└── templates/                  # Tier 4: Code generation (optional)
    └── *.md
```

### Creating a New Skill

1. **Create the skill directory**:
   ```bash
   mkdir -p .claude/skills/your-skill-name/{references,templates}
   ```

2. **Create `capabilities.json`** (Tier 1 - Discovery):
   ```json
   {
     "skill_id": "your-skill-name",
     "name": "Your Skill Name",
     "version": "1.0.0",
     "description": "Brief description of what this skill does",
     "tags": ["category", "type", "domain"],
     "capabilities": [
       "specific-capability-1",
       "specific-capability-2"
     ],
     "triggers": {
       "keywords": ["keyword1", "keyword2"],
       "patterns": ["pattern.*regex"]
     },
     "provides": [
       "deliverable-1",
       "deliverable-2"
     ],
     "dependencies": ["other-skill-id"],
     "progressive_loading": {
       "tier_2": "SKILL.md",
       "tier_3": ["references/*.md"],
       "tier_4": ["templates/*.md"]
     }
   }
   ```

3. **Create `SKILL.md`** (Tier 2 - Overview):
   ```markdown
   # Your Skill Name

   Description of the skill and its purpose.

   ## When to Use

   - Use case 1
   - Use case 2

   ## Key Patterns

   ### Pattern 1
   Description and example

   ### Pattern 2
   Description and example

   ## Examples

   Concrete examples of using this skill

   ## Integration

   How this skill works with other skills
   ```

4. **Add reference files** (Tier 3 - Specific):
   - Create focused reference files in `references/`
   - Each file should be 90-300 tokens
   - Cover specific patterns, checklists, or examples

5. **Add templates** (Tier 4 - Generation):
   - Optional: Add code generation templates
   - Keep templates focused and reusable

6. **Update `plugin.json`**:
   ```json
   {
     "skills": [
       {
         "id": "your-skill-name",
         "name": "Your Skill Name",
         "path": "./.claude/skills/your-skill-name",
         "description": "Brief description",
         "tags": ["category", "type"]
       }
     ]
   }
   ```

### Skill Best Practices

- **Keep it focused**: Each skill should have a single, clear purpose
- **Use progressive loading**: Structure content in 4 tiers for token efficiency
- **Provide examples**: Include concrete examples for each pattern
- **Document triggers**: Clear keywords and patterns for semantic discovery
- **Test thoroughly**: Verify the skill works in various scenarios

## Adding New Agents

Agents are specialized sub-processes that execute specific tasks within the plugin.

### Agent Structure

Create agent definition in `.claude/agents/your-agent-name.md`:

```markdown
---
name: your-agent-name
description: What this agent does and when to use it
tools: Read, Write, Grep
model: sonnet
permissionMode: plan
---

# Your Agent Name

Agent prompt and instructions...

## Your Task

Specific task description...

## Process

Step-by-step process...

## Output Format

Expected output format...

## Examples

Concrete examples...
```

### Registering the Agent

Add to `.claude/agent-registry.json`:

```json
{
  "agents": {
    "your-agent-name": {
      "display_name": "Your Agent Name",
      "color": "blue",
      "model_preference": {
        "default": "sonnet"
      },
      "capabilities": [
        "capability-1",
        "capability-2"
      ],
      "can_solve_examples": [
        "Example task 1",
        "Example task 2"
      ],
      "skills_used": ["skill-id-1", "skill-id-2"],
      "tools": ["Read", "Write"],
      "boundaries": {
        "allowed": [".claude/skills/**"],
        "forbidden": ["src/**"]
      },
      "handoff_to": ["other-agent-name"],
      "pipeline_position": 1
    }
  }
}
```

And update `plugin.json`:

```json
{
  "agents": [
    {
      "id": "your-agent-name",
      "name": "Your Agent Name",
      "display_name": "Your Agent Name",
      "path": "./.claude/agents/your-agent-name.md",
      "color": "blue",
      "triggers": {
        "keywords": ["keyword1", "keyword2"],
        "patterns": ["pattern.*"]
      },
      "capabilities": ["capability-1", "capability-2"],
      "skills_used": ["skill-id"]
    }
  ]
}
```

## Adding New Commands

Commands are user-invocable shortcuts for common operations.

### Command Structure

Create command file in `.claude/commands/your-command.md`:

```markdown
---
description: Brief description of what this command does
argument-hint: [expected-arguments]
---

# Your Command Name

Description of the command and its purpose.

## Task

Command execution instructions...

## Usage Examples

Example invocations and expected results...
```

### Registering the Command

Update `plugin.json`:

```json
{
  "commands": [
    {
      "id": "your-command",
      "name": "Your Command",
      "file": "./.claude/commands/your-command.md",
      "description": "Brief description"
    }
  ]
}
```

## Adding New Hooks

Hooks execute at specific lifecycle events to automate workflows or enforce policies.

### Hook Structure

Create hook script in `.claude/hooks/your-hook.sh`:

```bash
#!/bin/bash
set -e

# Read hook input from stdin (JSON format)
INPUT=$(cat)

# Extract relevant data
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')

# Your hook logic here
if [[ condition ]]; then
  cat <<EOF
[Your context injection or message]
EOF
  exit 0
fi

# Pass through unchanged
exit 0
```

Make it executable:
```bash
chmod +x .claude/hooks/your-hook.sh
```

### Registering the Hook

Update `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/your-hook.sh",
            "statusMessage": "Running your hook..."
          }
        ]
      }
    ]
  }
}
```

And update `plugin.json`:

```json
{
  "hooks": [
    {
      "id": "your-hook",
      "type": "user-prompt-submit",
      "file": "./.claude/hooks/your-hook.sh",
      "description": "What this hook does",
      "security_risk": "LOW"
    }
  ]
}
```

## Testing Your Changes

1. **Install the plugin locally**:
   ```bash
   # Symlink to Claude Code plugins directory
   ln -s $(pwd) ~/.claude/plugins/pseudo-code-prompting
   ```

2. **Test with Claude Code**:
   ```bash
   # Start a new session
   claude-code

   # Try your new feature
   /your-command test input
   ```

3. **Verify progressive loading**:
   - Check that skills load incrementally
   - Monitor token usage in Claude Code logs
   - Ensure discovery phase works correctly

4. **Test agent coordination**:
   - Verify agents are triggered correctly
   - Check handoff between agents works
   - Validate output format

## Code Quality Guidelines

### Skill Files
- Use clear, concise language
- Include concrete examples for every pattern
- Structure content for progressive loading
- Keep Tier 1 (capabilities.json) under 110 tokens
- Keep Tier 3 (references) files under 300 tokens each

### Agent Definitions
- Clearly define the agent's purpose and scope
- Specify all required tools
- Document expected input and output formats
- Include quality checks and validation steps

### Hooks
- Keep hooks focused on a single responsibility
- Exit with code 0 for pass-through behavior
- Use clear, informative status messages
- Handle edge cases gracefully
- Log errors appropriately

### Documentation
- Update README.md for major features
- Add entries to CHANGELOG.md
- Include usage examples
- Document any breaking changes

## Pull Request Process

1. **Update documentation**:
   - Update README.md if adding major features
   - Add entry to CHANGELOG.md
   - Update SKILL.md if changing plugin overview

2. **Test thoroughly**:
   - Test all affected workflows
   - Verify progressive loading works
   - Check agent coordination

3. **Submit PR** with:
   - Clear title describing the change
   - Description of what was added/changed/fixed
   - Examples of usage (if applicable)
   - Screenshots/recordings (if UI changes)

4. **Address review feedback**:
   - Respond to comments promptly
   - Make requested changes
   - Update PR description if scope changes

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them contribute
- Focus on what is best for the community
- Show empathy towards other contributors

## Questions?

- Open an issue for bug reports or feature requests
- Join discussions for design questions
- Check existing issues before creating new ones

Thank you for contributing to the Pseudo-Code Prompting Plugin!
