# Welcome Message and Menu System

When users invoke the plugin using trigger phrases like "use pseudo-code prompting plugin" or "use pseudo-code prompting with ralph", you MUST display a welcome message with an interactive menu.

## Welcome Message Structure

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Welcome to Pseudo-Code Prompting Plugin! 🎯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Transform natural language into structured, validated pseudo-code.

📖 **Help & Documentation**
   Type 'help' or ask 'how does this work?'

⚡ **Available Commands**
   • transform-query - Transform natural language to pseudo-code
   • validate-requirements - Validate pseudo-code completeness
   • optimize-prompt - Enhance pseudo-code with missing parameters
   • compress-context - Compress verbose requirements
   • complete-process - Full workflow (transform + validate + optimize)

🤖 **Ralph Loop Integration**
   Want automated implementation with Ralph Loop?
   Say 'use ralph' or 'with ralph' to start

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Quick: help | transform | validate | optimize | ralph
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Menu Display Triggers

Display the welcome menu when the user's message contains ANY of these patterns:

- "use pseudo-code prompting plugin"
- "use pseudocode prompting plugin"
- "use pseudo-code prompting with ralph"
- "use pseudocode prompting with ralph"
- "invoke complete-process"
- "show plugin menu"

## State Management for Menu Persistence

**CRITICAL**: After displaying the welcome menu, you MUST maintain awareness of the menu context throughout the conversation using the following strategy:

### Instruction-Based State Management

Since Claude Code doesn't have technical state management between turns, menu persistence is achieved through **behavioral instructions**:

1. **After Displaying Menu**: In EVERY subsequent response until user makes a selection, you MUST:
   - Check if user's message references any menu keywords
   - If YES: Route to appropriate skill
   - If NO: Provide helpful response AND append menu reminder footer

2. **Menu Reminder Footer**: Append this to all responses while menu is active:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   💡 Quick access: help | transform | validate | optimize | ralph
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

3. **Context Window Memory**: Use the last 2-3 messages to detect if menu was shown

### Menu State Tracking

Track these conceptual states (via conversation context, not technical state):

- `menu_displayed`: Was welcome menu shown in recent turns?
- `selection_made`: Has user selected a specific command/skill?
- `ralph_mode_requested`: Did user mention "ralph" or "with ralph"?

## User Selection Routing

When user's message contains menu keywords, route as follows:

| Keyword Detected | Action | Skill to Invoke |
|------------------|--------|-----------------|
| "help", "how does this work", "documentation" | Show comprehensive help | Display plugin documentation |
| "commands", "list commands", "what can you do" | List all available skills | Show all command descriptions |
| "transform", "transform-query" | Transform natural language to pseudo-code | `pseudo-code-prompting:prompt-structurer` |
| "validate", "validate-requirements" | Validate pseudo-code | `pseudo-code-prompting:requirement-validator` |
| "optimize", "optimize-prompt" | Optimize pseudo-code | `pseudo-code-prompting:prompt-optimizer` |
| "compress", "compress-context" | Compress verbose text | `pseudo-code-prompting:context-compressor` |
| "complete", "complete-process", "full workflow" | Run full pipeline | Execute complete mode workflow |
| "ralph", "with ralph", "use ralph" | Show Ralph consent then invoke | See Ralph Consent Flow below |

### Keyword Detection Logic

```
on_user_message:
  if menu_was_displayed_recently:
    detected_keywords = parse_for_menu_keywords(user_message)

    if detected_keywords.length > 0:
      if detected_keywords.includes("ralph"):
        show_ralph_consent_flow()
      else:
        route_to_skill(detected_keywords[0])
    else:
      respond_to_user_question()
      append_menu_reminder_footer()
```

## Ralph Consent Flow

When user mentions "ralph", "with ralph", or "use ralph", you MUST:

1. **Show Consent Message**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 Ralph Loop Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ralph Loop will automate the complete implementation with iterative
development, including:
  • Complexity estimation
  • Promise generation from validation
  • Automated iteration planning
  • Progressive implementation

This will run multiple automated iterations. Continue?

Options:
  • Say 'yes', 'confirm', or 'proceed' to start Ralph Loop
  • Say 'no', 'cancel', or 'manual' for manual workflow

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

2. **Wait for Explicit Confirmation**: Do NOT proceed until user explicitly confirms

3. **Detect Confirmation Keywords**:
   - **YES**: "yes", "confirm", "proceed", "use ralph", "start", "go ahead"
   - **NO**: "no", "cancel", "skip", "manual mode", "manual", "not now"
   - **AMBIGUOUS**: Any other response → Ask again with clearer options

4. **On Confirmation**: Invoke skill `pseudo-code-prompting:ralph-process-integration`

5. **On Rejection**: Return to menu, remind user of other options

## Menu Exit Conditions

Stop displaying menu reminders when ANY of these occur:

1. User explicitly selects a command/skill
2. User says "exit", "cancel", or "close menu"
3. User asks 3+ unrelated questions in a row (menu no longer relevant)
4. Skill execution completes successfully
5. User explicitly requests to stop seeing reminders

## Error Handling for Menu System

| Error Scenario | Handling Strategy |
|----------------|-------------------|
| Skill invocation fails | Show error, redisplay menu with "try again?" |
| Invalid menu selection | "I didn't recognize that command. Available options: ..." |
| User confusion | Rephrase menu with simpler language |
| Timeout (menu shown but no selection for 5+ turns) | Ask: "Still interested in using the plugin? (yes/no)" |

## Menu Examples

### Example 1: User Invokes Plugin

**User**: "use pseudo-code prompting plugin"

**Assistant**: *Displays welcome menu*

**User**: "help"

**Assistant**: *Shows comprehensive plugin documentation*

### Example 2: Ralph Integration Flow

**User**: "use pseudo-code prompting with ralph"

**Assistant**: *Displays welcome menu*

**User**: "use ralph"

**Assistant**: *Shows Ralph consent message*

**User**: "yes"

**Assistant**: *Invokes `pseudo-code-prompting:ralph-process-integration`*

### Example 3: Menu Persistence

**User**: "use pseudo-code prompting plugin"

**Assistant**: *Displays welcome menu*

**User**: "how does the validate command work?"

**Assistant**: *Explains validation feature AND appends menu reminder footer*

**User**: "transform"

**Assistant**: *Invokes `pseudo-code-prompting:prompt-structurer`*
