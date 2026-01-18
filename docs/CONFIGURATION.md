# Configuration

This plugin uses auto-discovery and requires no manual configuration. All skills, agents, commands, and hooks are automatically loaded.

## Optional: Customize Hook Behavior

If you want to customize hook behavior in your workspace, create `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/user-prompt-submit.sh",
            "statusMessage": "Checking for transformation commands...",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**Note**: This is optional. The plugin already registers hooks via `hooks/hooks.json` in the plugin folder.

## Customizing Skills

Skills are automatically discovered from the plugin's `skills/` folder. Each skill has:

- `capabilities.json` - Discovery triggers and metadata
- `SKILL.md` - Main skill content
- `references/` - Domain-specific patterns (optional)
- `templates/` - Code generation templates (optional)

To add custom domain patterns, you can extend skills by adding files to your workspace `.claude/skills/` folder (separate from the plugin).

## Advanced Usage

### Extending Skills with Custom Patterns

The plugin's skills are in the plugin folder and automatically loaded. To add custom domain-specific patterns:

1. **Option A**: Contribute to the plugin by adding patterns to the skill's `references/` folder
2. **Option B**: Create workspace-specific extensions (advanced users only)

### Example: Custom Validation Checklist

If you want to extend the `requirement-validator` skill with ML-specific patterns, you could:

```markdown
# Your custom checklist (for plugin contribution)
# Location: skills/requirement-validator/references/ml-validation-checklist.md

## Machine Learning Feature Validation

### Data Requirements
- [ ] Training data source specified
- [ ] Data preprocessing pipeline defined
- [ ] Train/validation/test split ratios
- [ ] Data augmentation strategy

### Model Requirements
- [ ] Model architecture specified
- [ ] Hyperparameters defined
- [ ] Training stopping criteria
- [ ] Checkpoint strategy

### Evaluation Requirements
- [ ] Metrics specified (accuracy, F1, etc.)
- [ ] Evaluation frequency
- [ ] Experiment tracking platform
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding new skills and patterns.
