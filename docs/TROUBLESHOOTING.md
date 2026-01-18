# Troubleshooting

## Commands Not Working

**Issue:** Commands like `/transform-query` not found

**Solution:**
```bash
# Verify plugin installation
/plugin list

# Check if pseudo-code-prompting is loaded
# Reinstall if needed:
/plugin install pseudo-code-prompting
```

## Hook Not Triggering

**Issue:** Hooks not executing on user input or file edits

**Solution:**
```bash
# Check hook scripts are executable
ls -la ~/.claude/plugins/pseudo-code-prompting/hooks/*.sh

# Should show -rwxr-xr-x permissions
# If not, make executable:
cd ~/.claude/plugins/pseudo-code-prompting/hooks
chmod +x *.sh

# Verify hooks.json exists
cat hooks/hooks.json
```

## Skills Not Auto-Invoked

**Issue:** Skills not triggering on keywords like "transform" or "validate"

**Solution:**
Skills are auto-discovered from the `skills/` folder. Each skill has a `capabilities.json` with trigger patterns.

```bash
# Verify skills exist
ls ~/.claude/plugins/pseudo-code-prompting/skills/

# Check a skill's triggers
cat ~/.claude/plugins/pseudo-code-prompting/skills/prompt-structurer/capabilities.json

# Use explicit keywords: "transform to pseudo-code", "validate requirements"

# Reload plugin
/plugin reload pseudo-code-prompting
```

## Validation Too Strict

**Issue:** Too many warnings/errors flagged

**Solution:**

The validation skill follows security best practices. If you need to adjust validation behavior:

1. **Review the validation checklists** in the skill:
   - [skills/requirement-validator/references/validation-checklists.md](../skills/requirement-validator/references/validation-checklists.md)

2. **Provide context** when using validation:
   ```
   /validate-requirements [your-pseudo-code]

   Context: This is a prototype/internal tool/low-risk feature
   ```

3. **Skip certain checks** explicitly:
   ```
   /validate-requirements [your-pseudo-code]

   Skip: Rate limiting (internal API), CORS (same-origin only)
   ```

The validation is intentionally comprehensive to catch security issues early.
