# GitHub Actions Workflows

This directory contains CI/CD workflows for the pseudo-code-prompting-plugin.

## Workflows

### 1. ci.yml - Continuous Integration
Runs on: Push to main/master/develop, Pull Requests

**Jobs:**
- JSON validation (plugin.json, marketplace.json, hooks.json)
- Bash script validation (shellcheck + syntax)
- Python script validation (syntax + execution tests)
- Markdown linting and link checking
- Integration tests (hook execution, tree generation)

### 2. plugin-validation.yml - Plugin Validation
Runs on: Push to main/master/develop, Pull Requests

**Jobs:**
- Manifest validation (schema checks)
- Hook validation (registration + script existence)
- Command/Agent validation (frontmatter + counting)
- Documentation validation (required files, CHANGELOG format)
- Integration validation (complete workflow test)

### 3. release.yml - Release Automation
Runs on: Push to main/master

**Jobs:**
- release-please (conventional commits → automated releases)
- Update plugin version files post-release
- Validate release artifacts
- Create enhanced release notes with statistics

### 4. version-check.yml - PR Version Check
Runs on: Pull Requests to main/master

**Jobs:**
- Version bump detection
- CHANGELOG modification check
- Version consistency across files
- Conventional commit validation
- Modified file validation

## Setup Instructions

### 1. Enable GitHub Actions

Go to repository Settings → Actions → General:
- ✅ Allow all actions and reusable workflows
- ✅ Read and write permissions (for release.yml)
- ✅ Allow GitHub Actions to create and approve pull requests

### 2. Configure Permissions

The release workflow requires special permissions. You have two options:

#### Option A: Enable PR Creation Permission (Recommended)

1. Go to Settings → Actions → General → Workflow permissions
2. Select "Read and write permissions"
3. ✅ **Check** "Allow GitHub Actions to create and approve pull requests"
4. Save

This allows `release-please` to automatically create release PRs.

#### Option B: Use Personal Access Token (Alternative)

If you prefer not to grant PR creation permission:

1. Create a Personal Access Token (classic) with `repo` scope
2. Add it as a repository secret named `RELEASE_TOKEN`
3. Update `.github/workflows/release.yml`:

```yaml
- name: Run Release Please
  uses: google-github-actions/release-please-action@v4
  with:
    token: ${{ secrets.RELEASE_TOKEN }}
    # ... rest of config
```

### 3. Branch Protection (Highly Recommended)

Protect your `main` branch from accidental force pushes, deletions, and require CI checks before merging.

#### Step-by-Step Setup

1. **Go to Repository Settings**
   - Navigate to your repository on GitHub
   - Click **Settings** (requires admin permissions)

2. **Access Branch Protection Rules**
   - In the left sidebar, click **Branches**
   - Under "Branch protection rules", click **Add rule**

3. **Configure Branch Name Pattern**
   - Branch name pattern: `main` (or `master` if that's your default branch)

4. **Enable Protection Rules**

   **Required Status Checks** (Recommended):
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - Select these status checks:
     - `CI Summary` (from ci.yml)
     - `Validation Summary` (from plugin-validation.yml)
     - `PR Check Summary` (from version-check.yml, for PRs only)

   **Protect Against Force Push** (Highly Recommended):
   - ✅ **Do not allow bypassing the above settings**
   - ✅ **Do not allow force pushes**
   - ✅ **Do not allow deletions**

   **Additional Options** (Optional but useful):
   - ✅ **Require a pull request before merging**
     - Require approvals: `1` (for team projects)
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ **Require conversation resolution before merging**
   - ✅ **Require linear history** (prevents merge commits, forces rebase/squash)

5. **Save Changes**
   - Scroll down and click **Create** or **Save changes**

#### What This Protects Against

| Protection | What It Prevents | Why It Matters |
|-----------|------------------|----------------|
| **Require status checks** | Merging code that fails tests | Catches bugs before they reach main |
| **No force pushes** | Rewriting history on main | Prevents breaking others' local repos |
| **No deletions** | Accidentally deleting main | Protects against catastrophic mistakes |
| **Require PR** | Direct pushes to main | Enables code review process |
| **Conversation resolution** | Unresolved review comments | Ensures all feedback is addressed |

#### Viewing Protection Status

After setup, you'll see:
- A shield icon next to the `main` branch
- "Protected" label in branch list
- Warning messages when trying to force push

#### Testing Protection Rules

Try these to verify protection is working:

```bash
# This should be blocked (force push)
git push --force origin main
# Expected: ! [remote rejected] main -> main (protected branch hook declined)

# This should be blocked (delete branch)
git push origin :main
# Expected: ! [remote rejected] main (deletion of the current branch prohibited)

# This should require PR + passing checks
git push origin feature-branch
# Create PR → CI runs → Can only merge after CI passes
```

#### Bypassing Protection (Admins Only)

If you're an admin and need to bypass protection:

1. Go to Settings → Branches → Edit rule
2. Enable "Allow force pushes" for administrators
3. Make your change
4. **Immediately re-enable protection**

**Warning**: Only do this in emergencies. It defeats the purpose of branch protection.

## Workflow Triggers

| Workflow | Push (main) | Push (develop) | Pull Request | Manual |
|----------|-------------|----------------|--------------|--------|
| ci.yml | ✅ | ✅ | ✅ | ✅ |
| plugin-validation.yml | ✅ | ✅ | ✅ | ✅ |
| release.yml | ✅ | ❌ | ❌ | ❌ |
| version-check.yml | ❌ | ❌ | ✅ | ❌ |

## Conventional Commits

The release workflow uses conventional commits for automatic versioning:

- `feat:` → Minor version bump (1.3.0 → 1.4.0)
- `fix:` → Patch version bump (1.3.0 → 1.3.1)
- `feat!:` or `BREAKING CHANGE:` → Major version bump (1.3.0 → 2.0.0)
- `docs:`, `chore:`, `refactor:`, `test:` → No version bump (added to CHANGELOG)

### Examples:

```bash
git commit -m "feat: add new transformation command"
git commit -m "fix(hooks): resolve tree generation timeout"
git commit -m "docs: update README with examples"
git commit -m "feat!: redesign plugin API structure"
```

## Troubleshooting

### "GitHub Actions is not permitted to create or approve pull requests"

**Solution**: Follow [Setup Instructions](#2-configure-permissions) above to enable PR creation.

### CI failing on markdown links

If you see `❌ Broken link in docs/...`:
- Check that linked files exist
- Anchor links (starting with `#`) are automatically skipped
- External URLs (starting with `http://` or `https://`) are skipped

### Version consistency errors

If `version-check.yml` fails:
- Ensure `plugin.json` and `.claude-plugin/marketplace.json` have the same version
- Update CHANGELOG.md with the new version section
- Use semantic versioning format (x.y.z)

### Shellcheck warnings

If bash scripts fail validation:
- Run locally: `shellcheck hooks/*.sh`
- Fix suggestions or add `# shellcheck disable=SC####` for false positives

## Local Testing

### Test JSON validation:
```bash
jq empty plugin.json
jq empty .claude-plugin/marketplace.json
jq empty hooks/hooks.json
```

### Test bash scripts:
```bash
bash -n hooks/*.sh
shellcheck hooks/*.sh
```

### Test Python scripts:
```bash
python -m py_compile hooks/*.py
python hooks/get_context_tree.py --help
```

### Test hook execution:
```bash
echo '{"prompt":"implement feature","cwd":"'$(pwd)'"}' | bash hooks/context-aware-tree-injection.sh
```

## Release Process

1. **Make changes** with conventional commits
2. **Push to main** branch
3. **release-please** creates/updates a release PR
4. **Review the PR** (check CHANGELOG, version bump)
5. **Merge the PR** → Automatic release is created
6. **Version files** are automatically updated post-release

## Notes

- Workflows are simplified compared to more complex plugins (no mem0, MCP, coordination tests)
- All validations run on every push and PR
- Release automation only runs on main branch
- Failed checks will block PR merging if branch protection is enabled
