# Plugin Documentation

Quick reference guide for all commands and architecture.

## Commands (1-minute reads)

Each command doc includes:
- What it does
- Goal
- When to use
- How to invoke (natural language)
- Workflow diagram with mermaid
- Agents, hooks, and skills involved
- Example output
- Why use this plugin

### Core Commands

| Command | Purpose | Read Time |
|---------|---------|-----------|
| **[smart](smart.md)** (NEW) | **Smart router: Intelligent command routing with context caching** | **1 min** |
| [complete-process](complete-process.md) | Full pipeline: transform → validate → optimize | 1 min |
| [transform-query](transform-query.md) | Convert natural language to pseudo-code | 1 min |
| [compress-context](compress-context.md) | Reduce verbose requirements by 80-95% | 1 min |
| [validate-requirements](validate-requirements.md) | Check completeness and security | 1 min |
| [optimize-prompt](optimize-prompt.md) | Add missing security and validation | 1 min |
| [context-aware-transform](context-aware-transform.md) | Architecture-aware with real paths | 1 min |

## Architecture

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | End-to-end system flow with diagrams | 2 min |

### What's in ARCHITECTURE.md

- Complete end-to-end flow diagram
- Component layers (hooks, commands, agents, skills)
- Data flow with sequence diagram
- Directory structure
- Token efficiency metrics
- Performance characteristics
- Why this architecture

## Quick Navigation

**New to the plugin?**
1. Start with [complete-process.md](complete-process.md) - it's the main command
2. Learn about [smart](smart.md) - new meta-command for token efficiency
3. Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
4. Explore individual commands as needed

**Multi-command workflows (NEW)?**
- Use [smart](smart.md) for 40-70% token savings on multiple commands
- Automatic context reuse across transform → validate → optimize
- See smart doc for real-world workflow examples

**Need a specific transformation?**
- Multiple commands → [smart](smart.md) (saves tokens!)
- Long requirements → [compress-context.md](compress-context.md)
- Basic structuring → [transform-query.md](transform-query.md)
- Quality check → [validate-requirements.md](validate-requirements.md)
- Enhancement → [optimize-prompt.md](optimize-prompt.md)
- Architecture-aware → [context-aware-transform.md](context-aware-transform.md)

**Want to understand the internals?**
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for complete system design

## Total Read Time

- **All Commands**: 7 minutes (including new smart command)
- **Architecture**: 2 minutes
- **Complete Documentation**: 9 minutes

You can become proficient with the entire plugin (including new smart meta-command) in under 10 minutes!
