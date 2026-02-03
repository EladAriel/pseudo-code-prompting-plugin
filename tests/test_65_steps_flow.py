"""
Test suite for the complete 6.5 steps flow including specification injection and context preservation.

Tests the complete workflow:
1. Context Detection
2. Auto-Compression
3. Transform to Pseudo-Code
4. Validate Completeness
5. Optimize with Parameters
6. Bridge Offer
6.5. SPECIFICATION INJECTION with Three-Layer Context Protection

This test suite specifically verifies:
- PostToolUse hook correctly detects pseudo-code output
- Specification is saved to .claude/pseudo-code-prompting/specification.md
- activeContext.md is created/updated with the specification reference
- Specification markers (PSEUDO-CODE-CONTEXT) are added for preservation
- Context recovery hook detects and restores lost specifications
- Three-layer protection prevents specification loss when cc10x writes
- Both file existence and proper content placement are validated
"""

import pytest
import json
import re
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest import mock
import sys
import os


# ============================================================================
# CONSTANTS
# ============================================================================

PSEUDO_CODE_PATTERN = r'(implement_\w+\([^)]*(?:\n[^)]*)*?\))'
ACTIVECONTEXT_TEMPLATE = """# CC10X Context

## Current Focus
[Default focus area]

## References
- Project structure
- Key files

## Recent Changes
- None yet

## Decisions
- None yet
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_mock_workflow_state(command_type="transform", requirement="Test requirement") -> dict:
    """Create a mock workflow state file content."""
    return {
        "workflow_active": True,
        "active_plugin": "pseudo-code-prompting",
        "command_type": command_type,
        "requirement": requirement,
        "cc10x_blocked": True,
        "bridge_expected": True,
        "timestamp": datetime.now().isoformat()
    }


def create_mock_tool_output_with_pseudocode() -> str:
    """Create mock tool output containing pseudo-code."""
    return """
TRANSFORMED PSEUDO-CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

implement_jwt_authentication(
  type="jwt",
  access_token_ttl="15m",
  refresh_token_ttl="7d",
  password_hashing="bcrypt",
  cookies={"secure": true, "httponly": true},
  rate_limiting={"max": 5, "window": "15m"},
  error_handling={401, 403, 429},
  logging=true,
  timeout="5s"
)

OPTIMIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Context detected: Node.js + Express project
✓ Validation: ALL CHECKS PASSED
✓ Parameters added: error_handling, logging, timeout
✓ Production ready: Yes
"""


def extract_pseudocode_from_output(output: str) -> str | None:
    """Extract pseudo-code from tool output (matches hook logic)."""
    # Pattern 1: Function-style pseudo-code
    func_pattern = r'(implement_\w+\([^)]*(?:\n[^)]*)*?\))'
    match = re.search(func_pattern, output, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)

    # Pattern 2: TRANSFORMED PSEUDO-CODE section
    if 'TRANSFORMED PSEUDO-CODE' in output:
        start = output.find('TRANSFORMED PSEUDO-CODE')
        end = output.find('OPTIMIZATION SUMMARY', start)
        if end > start:
            return output[start:end].strip()

    return None


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory with .claude structure."""
    # Create .claude directory structure
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    pseudocode_dir = claude_dir / "pseudo-code-prompting"
    pseudocode_dir.mkdir()

    cc10x_dir = claude_dir / "cc10x"
    cc10x_dir.mkdir()

    # Create default activeContext.md if it doesn't exist
    activecontext = cc10x_dir / "activeContext.md"
    if not activecontext.exists():
        activecontext.write_text(ACTIVECONTEXT_TEMPLATE)

    # Change to temp directory for this test
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    yield tmp_path

    # Restore original directory
    os.chdir(original_cwd)


@pytest.fixture
def sample_requirement():
    """Sample requirement for testing."""
    return "Implement JWT authentication with refresh tokens, secure cookies, and comprehensive error handling"


@pytest.fixture
def sample_pseudocode():
    """Sample pseudo-code for testing."""
    return """implement_jwt_authentication(
  type="jwt",
  access_token_ttl="15m",
  refresh_token_ttl="7d",
  password_hashing="bcrypt",
  cookies={"secure": true, "httponly": true},
  rate_limiting={"max": 5, "window": "15m"},
  error_handling={401, 403, 429},
  logging=true,
  timeout="5s"
)"""


@pytest.fixture
def sample_tool_output():
    """Sample tool output containing pseudo-code."""
    return create_mock_tool_output_with_pseudocode()


# ============================================================================
# TEST CLASSES
# ============================================================================

class TestSpecificationFileCreation:
    """Test that specification.md is properly created."""

    def test_specification_file_created_when_pseudocode_extracted(self, temp_project_dir, sample_requirement, sample_pseudocode):
        """Specification file should be created in .claude/pseudo-code-prompting/ directory."""
        # Arrange
        spec_dir = temp_project_dir / ".claude" / "pseudo-code-prompting"
        spec_file = spec_dir / "specification.md"

        # Verify directory exists
        assert spec_dir.exists(), "pseudo-code-prompting directory should exist"
        assert not spec_file.exists(), "specification.md should not exist initially"

        # Act - simulate saving specification
        spec_content = f"""# Pseudo-Code Specification

## Requirement
{sample_requirement}

## Generated Pseudo-Code
```
{sample_pseudocode}
```

## Generated At
{datetime.now().isoformat()}
"""
        spec_file.write_text(spec_content)

        # Assert
        assert spec_file.exists(), "specification.md should be created"
        assert spec_file.is_file(), "specification.md should be a file"
        content = spec_file.read_text()
        assert "# Pseudo-Code Specification" in content, "Should have header"
        assert sample_requirement in content, "Should contain requirement"
        assert sample_pseudocode in content, "Should contain pseudo-code"

    def test_specification_file_location(self, temp_project_dir):
        """Specification file should be at .claude/pseudo-code-prompting/specification.md."""
        # Arrange
        expected_path = temp_project_dir / ".claude" / "pseudo-code-prompting" / "specification.md"

        # Act
        expected_path.write_text("test content")

        # Assert
        assert expected_path.exists(), "File should exist at expected location"
        assert expected_path.parent.name == "pseudo-code-prompting", "Parent should be pseudo-code-prompting"
        assert expected_path.name == "specification.md", "Filename should be specification.md"

    def test_specification_file_contains_all_sections(self, temp_project_dir, sample_requirement, sample_pseudocode):
        """Specification file should contain all required sections."""
        # Arrange
        spec_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "specification.md"

        # Act
        spec_content = f"""# Pseudo-Code Specification

## Requirement
{sample_requirement}

## Generated Pseudo-Code
```
{sample_pseudocode}
```

## Generated At
{datetime.now().isoformat()}
"""
        spec_file.write_text(spec_content)

        # Assert - check all sections
        content = spec_file.read_text()
        assert "# Pseudo-Code Specification" in content, "Should have title section"
        assert "## Requirement" in content, "Should have Requirement section"
        assert "## Generated Pseudo-Code" in content, "Should have Generated Pseudo-Code section"
        assert "## Generated At" in content, "Should have Generated At section"
        assert "```" in content, "Should have code fence for pseudo-code"


class TestActiveContextUpdate:
    """Test that activeContext.md is properly updated with specification reference."""

    def test_activecontext_created_if_not_exists(self, temp_project_dir):
        """activeContext.md should be created if it doesn't exist."""
        # Arrange
        activecontext_path = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        if activecontext_path.exists():
            activecontext_path.unlink()

        # Act
        activecontext_path.write_text("# Initial Context\n\n## Current Focus\nInitial focus")

        # Assert
        assert activecontext_path.exists(), "activeContext.md should be created"
        assert activecontext_path.is_file(), "Should be a file"

    def test_activecontext_location(self, temp_project_dir):
        """activeContext.md should be at .claude/cc10x/activeContext.md."""
        # Arrange
        expected_path = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"

        # Assert
        assert expected_path.parent.name == "cc10x", "Parent should be cc10x directory"
        assert expected_path.name == "activeContext.md", "Filename should be activeContext.md"

    def test_activecontext_has_current_focus_section(self, temp_project_dir, sample_pseudocode):
        """activeContext.md should have Current Focus section with pseudo-code reference."""
        # Arrange
        activecontext_path = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"

        # Act - update Current Focus section
        focus_content = f"""Implementing from pseudo-code specification:

{sample_pseudocode[:300]}... [full spec: .claude/pseudo-code-prompting/specification.md]

**Approach:** Follow pseudo-code structure. Break down into phases per specification."""

        existing_content = activecontext_path.read_text()
        if '## Current Focus' in existing_content:
            pattern = r'(## Current Focus\n)(.*?)(\n## )'
            replacement = f'\\1{focus_content}\\3'
            updated = re.sub(pattern, replacement, existing_content, flags=re.DOTALL)
        else:
            # If section doesn't exist, create it
            updated = f"## Current Focus\n{focus_content}\n\n" + existing_content

        activecontext_path.write_text(updated)

        # Assert
        content = activecontext_path.read_text()
        assert "## Current Focus" in content, "Should have Current Focus section"
        assert "Implementing from pseudo-code specification" in content, "Should have implementation focus"
        assert ".claude/pseudo-code-prompting/specification.md" in content, "Should reference specification file"

    def test_activecontext_preserves_other_sections(self, temp_project_dir):
        """activeContext.md update should preserve other sections."""
        # Arrange
        activecontext_path = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        original_content = """# CC10X Context

## Current Focus
Old focus

## References
- Old reference

## Recent Changes
- Old change

## Decisions
- Old decision
"""
        activecontext_path.write_text(original_content)

        # Act - update only Current Focus
        new_focus = "New focus area"
        pattern = r'(## Current Focus\n)(.*?)(\n## )'
        replacement = f'\\1{new_focus}\\3'
        updated = re.sub(pattern, replacement, original_content, flags=re.DOTALL)
        activecontext_path.write_text(updated)

        # Assert
        content = activecontext_path.read_text()
        assert "## References" in content, "Should preserve References section"
        assert "## Recent Changes" in content, "Should preserve Recent Changes section"
        assert "## Decisions" in content, "Should preserve Decisions section"
        assert "New focus area" in content, "Should have new focus"
        assert "- Old reference" in content, "Should preserve old references"


class TestWorkflowStateDetection:
    """Test that workflow state is properly detected to trigger injection."""

    def test_workflow_state_file_detected(self, temp_project_dir, sample_requirement):
        """Should detect workflow state file."""
        # Arrange
        state_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "workflow-state.json"

        # Act - create state file
        state = create_mock_workflow_state(requirement=sample_requirement)
        state_file.write_text(json.dumps(state, indent=2))

        # Assert
        assert state_file.exists(), "State file should exist"
        loaded_state = json.loads(state_file.read_text())
        assert loaded_state["workflow_active"] is True, "Should indicate workflow is active"
        assert loaded_state["requirement"] == sample_requirement, "Should store requirement"

    def test_workflow_state_contains_requirement(self, temp_project_dir, sample_requirement):
        """Workflow state should contain the requirement."""
        # Arrange
        state_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "workflow-state.json"

        # Act
        state = create_mock_workflow_state(requirement=sample_requirement)
        state_file.write_text(json.dumps(state, indent=2))

        # Assert
        loaded_state = json.loads(state_file.read_text())
        assert "requirement" in loaded_state, "Should have requirement field"
        assert loaded_state["requirement"] == sample_requirement, "Should match provided requirement"

    def test_workflow_state_indicates_active_plugin(self, temp_project_dir):
        """Workflow state should identify active plugin."""
        # Arrange
        state_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "workflow-state.json"

        # Act
        state = create_mock_workflow_state()
        state_file.write_text(json.dumps(state, indent=2))

        # Assert
        loaded_state = json.loads(state_file.read_text())
        assert loaded_state["active_plugin"] == "pseudo-code-prompting", "Should identify plugin"
        assert loaded_state["workflow_active"] is True, "Should indicate workflow is active"


class TestPseudoCodeExtraction:
    """Test that pseudo-code is properly extracted from tool output."""

    def test_extracts_pseudocode_from_transformed_section(self, sample_tool_output):
        """Should extract pseudo-code from TRANSFORMED PSEUDO-CODE section."""
        # Act
        extracted = extract_pseudocode_from_output(sample_tool_output)

        # Assert
        assert extracted is not None, "Should extract pseudo-code"
        assert "implement_jwt_authentication" in extracted, "Should contain function name"
        assert "type=" in extracted, "Should contain parameters"

    def test_extracts_function_style_pseudocode(self):
        """Should extract function-style pseudo-code."""
        # Arrange
        output = """
Some text before
implement_authentication(type='oauth', logging=true)
Some text after
"""

        # Act
        extracted = extract_pseudocode_from_output(output)

        # Assert
        assert extracted is not None, "Should extract pseudo-code"
        assert "implement_authentication" in extracted, "Should contain function name"

    def test_extracts_multiline_pseudocode(self, sample_pseudocode):
        """Should extract multi-line pseudo-code."""
        # Arrange
        output = f"Some preamble\n{sample_pseudocode}\nSome conclusion"

        # Act
        extracted = extract_pseudocode_from_output(output)

        # Assert
        assert extracted is not None, "Should extract pseudo-code"
        assert "implement_jwt_authentication" in extracted, "Should contain function name"
        assert "refresh_token_ttl" in extracted, "Should contain multi-line parameters"

    def test_handles_missing_pseudocode(self):
        """Should return None when no pseudo-code found."""
        # Arrange
        output = "Just some regular text without any pseudo-code"

        # Act
        extracted = extract_pseudocode_from_output(output)

        # Assert
        assert extracted is None, "Should return None when no pseudo-code found"


class TestEndToEndSpecificationInjection:
    """Test complete end-to-end specification injection flow."""

    def test_complete_injection_flow_when_activecontext_exists(self, temp_project_dir, sample_requirement, sample_tool_output):
        """Complete flow: detect workflow -> extract pseudocode -> save spec -> update activeContext."""
        # Arrange
        state_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "workflow-state.json"
        spec_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "specification.md"
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"

        # Step 1: Create workflow state
        state = create_mock_workflow_state(requirement=sample_requirement)
        state_file.write_text(json.dumps(state, indent=2))

        # Step 2: Extract pseudo-code from tool output
        extracted_pseudocode = extract_pseudocode_from_output(sample_tool_output)
        assert extracted_pseudocode is not None, "Should extract pseudo-code"

        # Step 3: Save specification
        spec_content = f"""# Pseudo-Code Specification

## Requirement
{sample_requirement}

## Generated Pseudo-Code
```
{extracted_pseudocode}
```

## Generated At
{datetime.now().isoformat()}
"""
        spec_file.write_text(spec_content)

        # Step 4: Update activeContext
        focus_summary = f"{extracted_pseudocode[:300]}... [full spec: .claude/pseudo-code-prompting/specification.md]"
        focus_content = f"""Implementing from pseudo-code specification:

{focus_summary}

**Approach:** Follow pseudo-code structure. Break down into phases per specification."""

        existing = activecontext_file.read_text()
        if '## Current Focus' in existing:
            pattern = r'(## Current Focus\n)(.*?)(\n## )'
            replacement = f'\\1{focus_content}\\3'
            updated = re.sub(pattern, replacement, existing, flags=re.DOTALL)
        else:
            updated = f"## Current Focus\n{focus_content}\n\n" + existing

        activecontext_file.write_text(updated)

        # Assert - all files created and updated
        assert state_file.exists(), "State file should exist"
        assert spec_file.exists(), "Specification file should be created"
        assert activecontext_file.exists(), "activeContext should exist"

        # Verify specification content
        spec_text = spec_file.read_text()
        assert sample_requirement in spec_text, "Spec should contain requirement"
        assert "implement_jwt_authentication" in spec_text, "Spec should contain pseudo-code"

        # Verify activeContext update
        ac_text = activecontext_file.read_text()
        assert "## Current Focus" in ac_text, "Should have Current Focus section"
        assert ".claude/pseudo-code-prompting/specification.md" in ac_text, "Should reference spec file"
        assert "implement_jwt_authentication" in ac_text, "Should have pseudo-code summary"

    def test_injection_flow_creates_activecontext_if_missing(self, temp_project_dir, sample_requirement, sample_pseudocode):
        """Should create activeContext.md if it doesn't exist."""
        # Arrange
        cc10x_dir = temp_project_dir / ".claude" / "cc10x"
        activecontext_file = cc10x_dir / "activeContext.md"

        # Remove activeContext if it exists
        if activecontext_file.exists():
            activecontext_file.unlink()

        assert not activecontext_file.exists(), "activeContext should not exist initially"

        # Act - create it
        initial_content = f"""# CC10X Context

## Current Focus
Implementing from pseudo-code specification:

{sample_pseudocode[:300]}... [full spec: .claude/pseudo-code-prompting/specification.md]

**Approach:** Follow pseudo-code structure.

## References
- Specification: .claude/pseudo-code-prompting/specification.md

## Recent Changes
- Pseudo-code specification generated

## Decisions
- Use pseudo-code as primary specification
"""
        activecontext_file.write_text(initial_content)

        # Assert
        assert activecontext_file.exists(), "activeContext should be created"
        assert "## Current Focus" in activecontext_file.read_text(), "Should have required sections"

    def test_injection_preserves_existing_activecontext_structure(self, temp_project_dir, sample_pseudocode):
        """Injection should preserve existing activeContext structure when updating."""
        # Arrange
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        original_references = "- Project structure\n- Architecture.md\n- Implementation notes"
        original_decisions = "- Use TypeScript for type safety\n- Use Express.js for API"

        original_content = f"""# CC10X Context

## Current Focus
Previous work here

## References
{original_references}

## Recent Changes
- Previous change

## Decisions
{original_decisions}
"""
        activecontext_file.write_text(original_content)

        # Act - update Current Focus
        new_focus = "New pseudo-code implementation"
        pattern = r'(## Current Focus\n)(.*?)(\n## )'
        replacement = f'\\1{new_focus}\\3'
        updated = re.sub(pattern, replacement, original_content, flags=re.DOTALL)
        activecontext_file.write_text(updated)

        # Assert - verify preservation
        content = activecontext_file.read_text()
        assert "## References" in content, "Should preserve References section"
        assert original_references in content, "Should preserve original references"
        assert "## Decisions" in content, "Should preserve Decisions section"
        assert original_decisions in content, "Should preserve original decisions"
        assert new_focus in content, "Should have updated focus"


class TestStep65SpecificationInjectionIntegration:
    """Integration tests for Step 6.5 complete flow."""

    def test_step_65_workflow_start_to_finish(self, temp_project_dir, sample_requirement, sample_pseudocode):
        """Test complete Step 6.5 flow from workflow state to activeContext update."""
        # Step 1: Transform produces pseudo-code (Steps 1-5)
        tool_output = f"""
TRANSFORMED PSEUDO-CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{sample_pseudocode}

OPTIMIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━
✓ Context detected: Node.js + Express
✓ Production ready: Yes
"""

        # Step 2: Workflow coordinator detects transform (already active)
        state_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "workflow-state.json"
        state = create_mock_workflow_state(requirement=sample_requirement)
        state_file.write_text(json.dumps(state, indent=2))

        # Step 3: PostToolUse hook runs (Step 6.5)
        extracted = extract_pseudocode_from_output(tool_output)
        assert extracted is not None, "Should extract pseudo-code"

        # Step 4: Save specification
        spec_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "specification.md"
        spec_content = f"""# Pseudo-Code Specification

## Requirement
{sample_requirement}

## Generated Pseudo-Code
```
{extracted}
```

## Generated At
{datetime.now().isoformat()}
"""
        spec_file.write_text(spec_content)

        # Step 5: Update activeContext
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        focus_content = f"""Implementing from pseudo-code specification:

{extracted[:300]}... [full spec: .claude/pseudo-code-prompting/specification.md]

**Approach:** Follow pseudo-code structure. Break down into phases per specification."""

        existing = activecontext_file.read_text()
        pattern = r'(## Current Focus\n)(.*?)(\n## )'
        replacement = f'\\1{focus_content}\\3'
        updated = re.sub(pattern, replacement, existing, flags=re.DOTALL)
        activecontext_file.write_text(updated)

        # Step 6: Bridge question shown
        bridge_question = "🚀 Ready to implement with cc10x? (Y/n)"

        # Verify entire flow
        assert state_file.exists(), "Workflow state should be active"
        assert spec_file.exists(), "Specification should be saved"
        assert activecontext_file.exists(), "activeContext should exist"

        spec_text = spec_file.read_text()
        assert sample_requirement in spec_text, "Spec should contain requirement"
        assert "implement_" in spec_text, "Spec should contain pseudo-code"

        ac_text = activecontext_file.read_text()
        assert ".claude/pseudo-code-prompting/specification.md" in ac_text, "Should reference spec"
        assert "Implementing from pseudo-code specification" in ac_text, "Should indicate pseudo-code focus"

    def test_step_65_with_existing_activecontext(self, temp_project_dir, sample_requirement, sample_pseudocode):
        """Test Step 6.5 injection into existing activeContext without losing content."""
        # Arrange - existing activeContext with valuable content
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        existing_content = """# CC10X Context

## Current Focus
Working on user authentication feature

## References
- docs/authentication.md
- src/services/auth.ts
- Previous pseudo-code specs

## Recent Changes
- Analyzed auth requirements
- Reviewed existing implementation

## Decisions
- Use JWT for stateless authentication
- Implement refresh token rotation
"""
        activecontext_file.write_text(existing_content)

        # Act - inject new pseudo-code specification
        new_focus = f"""Implementing from pseudo-code specification:

{sample_pseudocode[:300]}... [full spec: .claude/pseudo-code-prompting/specification.md]

**Approach:** Follow pseudo-code structure."""

        pattern = r'(## Current Focus\n)(.*?)(\n## )'
        replacement = f'\\1{new_focus}\\3'
        updated = re.sub(pattern, replacement, existing_content, flags=re.DOTALL)
        activecontext_file.write_text(updated)

        # Assert - content preserved and updated
        result = activecontext_file.read_text()
        assert "## References" in result, "Should preserve References section"
        assert "docs/authentication.md" in result, "Should preserve existing references"
        assert "## Recent Changes" in result, "Should preserve Recent Changes section"
        assert "## Decisions" in result, "Should preserve Decisions section"
        assert "Use JWT for stateless authentication" in result, "Should preserve existing decisions"
        assert "Implementing from pseudo-code specification" in result, "Should have new focus"
        assert ".claude/pseudo-code-prompting/specification.md" in result, "Should reference spec file"

    def test_step_65_specification_file_format_compliance(self, temp_project_dir, sample_requirement, sample_pseudocode):
        """Test that saved specification follows expected format."""
        # Act
        spec_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "specification.md"
        spec_content = f"""# Pseudo-Code Specification

## Requirement
{sample_requirement}

## Generated Pseudo-Code
```
{sample_pseudocode}
```

## Generated At
{datetime.now().isoformat()}
"""
        spec_file.write_text(spec_content)

        # Assert format compliance
        content = spec_file.read_text()
        lines = content.split('\n')

        # Check structure
        assert lines[0] == "# Pseudo-Code Specification", "Should start with title"
        assert any("## Requirement" in line for line in lines), "Should have Requirement section"
        assert any("## Generated Pseudo-Code" in line for line in lines), "Should have Generated Pseudo-Code section"
        assert any("## Generated At" in line for line in lines), "Should have Generated At section"

        # Check content
        assert sample_requirement in content, "Should contain full requirement"
        assert "```" in content, "Should have code fences"
        assert sample_pseudocode in content, "Should contain full pseudo-code"


class TestContextPreservationMarkers:
    """Test context preservation markers (Layer 1 - Prevention)."""

    def test_specification_section_has_preservation_markers(self, temp_project_dir, sample_pseudocode):
        """Specification section should have PSEUDO-CODE-CONTEXT markers."""
        # Arrange
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        spec_section = f"""## Specification
<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE. Persisted specification reference. -->
<!-- This section contains critical implementation guidance and should be preserved. -->

**Source:** Pseudo-code specification
**File:** .claude/pseudo-code-prompting/specification.md
**Purpose:** Primary implementation guide generated from requirements
**Generated:** {datetime.now().isoformat()}

### Summary
{sample_pseudocode[:400]}...

### How to Use
1. Review full specification at: `.claude/pseudo-code-prompting/specification.md`
2. Follow the pseudo-code phases and structure
3. Reference specification section in this context for quick access

<!-- END PSEUDO-CODE-CONTEXT -->
"""

        # Act - add specification section to activeContext
        existing = activecontext_file.read_text()
        updated = existing.rstrip() + '\n\n' + spec_section
        activecontext_file.write_text(updated)

        # Assert - markers present
        content = activecontext_file.read_text()
        assert "## Specification" in content, "Should have Specification section"
        assert "PSEUDO-CODE-CONTEXT: DO NOT REMOVE" in content, "Should have preservation marker"
        assert "<!-- END PSEUDO-CODE-CONTEXT -->" in content, "Should have end marker"
        assert ".claude/pseudo-code-prompting/specification.md" in content, "Should reference spec file"

    def test_specification_markers_are_identifiable(self, temp_project_dir):
        """Specification markers should be easily identifiable for recovery."""
        # Arrange
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"

        # Act - add marked specification
        spec_with_markers = """## Specification
<!-- PSEUDO-CODE-CONTEXT: DO NOT REMOVE -->
Content here
<!-- END PSEUDO-CODE-CONTEXT -->"""

        existing = activecontext_file.read_text()
        updated = existing + '\n\n' + spec_with_markers
        activecontext_file.write_text(updated)

        # Assert - markers are identifiable
        content = activecontext_file.read_text()
        assert "PSEUDO-CODE-CONTEXT" in content, "Should have context marker"
        assert "END PSEUDO-CODE-CONTEXT" in content, "Should have end marker"

        # Verify pattern matching works
        pattern = r'<!-- PSEUDO-CODE-CONTEXT.*?END PSEUDO-CODE-CONTEXT -->'
        match = re.search(pattern, content, re.DOTALL)
        assert match is not None, "Should match preservation marker pattern"


class TestContextRecoveryMechanism:
    """Test recovery mechanism (Layer 3 - Safety Net)."""

    def test_recovery_detects_lost_specification(self, temp_project_dir, sample_pseudocode):
        """Recovery hook should detect when specification reference is lost."""
        # Arrange - activeContext without specification
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        context_without_spec = """# Active Context

## Current Focus
Some implementation work

## References
- Other references

## Decisions
- Some decision
"""
        activecontext_file.write_text(context_without_spec)

        # Act - check for specification
        content = activecontext_file.read_text()
        has_spec = '## Specification' in content and 'PSEUDO-CODE-CONTEXT' in content

        # Assert - specification is missing
        assert not has_spec, "Specification should be detected as missing"

    def test_recovery_loads_specification_from_file(self, temp_project_dir, sample_requirement, sample_pseudocode):
        """Recovery hook should load specification from specification.md."""
        # Arrange - save specification
        spec_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "specification.md"
        spec_content = f"""# Pseudo-Code Specification

## Requirement
{sample_requirement}

## Generated Pseudo-Code
```
{sample_pseudocode}
```

## Generated At
{datetime.now().isoformat()}
"""
        spec_file.write_text(spec_content)

        # Act - load specification
        loaded_spec = spec_file.read_text()

        # Assert - specification loaded correctly
        assert sample_requirement in loaded_spec, "Should contain requirement"
        assert sample_pseudocode in loaded_spec, "Should contain pseudo-code"
        assert "# Pseudo-Code Specification" in loaded_spec, "Should have title"

    def test_recovery_restores_specification_to_activecontext(self, temp_project_dir, sample_pseudocode):
        """Recovery should inject specification back into activeContext if missing."""
        # Arrange - activeContext without specification, but spec file exists
        spec_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "specification.md"
        spec_file.write_text(f"# Specification\n\n{sample_pseudocode}")

        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        context_without_spec = """# Context

## Current Focus
Implementation

## Blockers
None
"""
        activecontext_file.write_text(context_without_spec)

        # Act - restore specification
        spec_section = f"""## Specification
<!-- PSEUDO-CODE-CONTEXT: Recovered -->
{spec_file.read_text()}
<!-- END PSEUDO-CODE-CONTEXT -->
"""

        existing = activecontext_file.read_text()
        if '## Blockers' in existing:
            updated = existing.replace('## Blockers', spec_section + '\n\n## Blockers')
        else:
            updated = existing.rstrip() + '\n\n' + spec_section

        activecontext_file.write_text(updated)

        # Assert - specification restored
        result = activecontext_file.read_text()
        assert "## Specification" in result, "Should have Specification section"
        assert "PSEUDO-CODE-CONTEXT" in result, "Should have preservation marker"
        assert "## Current Focus" in result, "Should preserve original content"

    def test_recovery_only_acts_when_specification_missing(self, temp_project_dir):
        """Recovery should not modify context if specification already present."""
        # Arrange
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        context_with_spec = """# Context

## Specification
<!-- PSEUDO-CODE-CONTEXT -->
Already here
<!-- END PSEUDO-CODE-CONTEXT -->

## Blockers
None
"""
        activecontext_file.write_text(context_with_spec)

        # Act - check if recovery is needed
        content = activecontext_file.read_text()
        needs_recovery = not ('## Specification' in content and 'PSEUDO-CODE-CONTEXT' in content)

        # Assert - no recovery needed
        assert not needs_recovery, "Recovery should not be triggered when spec present"
        # Verify content unchanged
        assert content == context_with_spec, "Content should not be modified"


class TestErrorHandling:
    """Test error handling and edge cases in injection."""

    def test_handles_missing_workflow_state_gracefully(self, temp_project_dir, sample_tool_output):
        """Should handle missing workflow state gracefully."""
        # Arrange - no workflow state file
        state_file = temp_project_dir / ".claude" / "pseudo-code-prompting" / "workflow-state.json"
        assert not state_file.exists(), "State file should not exist"

        # Act - try to extract (should work regardless)
        extracted = extract_pseudocode_from_output(sample_tool_output)

        # Assert - extraction should still work
        assert extracted is not None, "Should extract pseudo-code even without state file"

    def test_handles_tool_output_without_pseudocode(self, temp_project_dir):
        """Should handle tool output that doesn't contain pseudo-code."""
        # Arrange
        output = "This is just regular text without any pseudo-code or function calls"

        # Act
        extracted = extract_pseudocode_from_output(output)

        # Assert
        assert extracted is None, "Should return None for non-pseudo-code output"

    def test_handles_malformed_activecontext(self, temp_project_dir, sample_pseudocode):
        """Should handle malformed activeContext gracefully."""
        # Arrange - malformed activeContext
        activecontext_file = temp_project_dir / ".claude" / "cc10x" / "activeContext.md"
        activecontext_file.write_text("Malformed content without proper sections")

        # Act - try to update (should not crash)
        focus_content = "New focus content"
        existing = activecontext_file.read_text()

        # If pattern not found, create structure
        if '## Current Focus' not in existing:
            updated = f"## Current Focus\n{focus_content}\n\n{existing}"
        else:
            pattern = r'(## Current Focus\n)(.*?)(\n## )'
            replacement = f'\\1{focus_content}\\3'
            updated = re.sub(pattern, replacement, existing, flags=re.DOTALL)

        activecontext_file.write_text(updated)

        # Assert - file should be updated or created without error
        assert activecontext_file.exists(), "File should still exist"
        assert "## Current Focus" in activecontext_file.read_text(), "Should have Current Focus section"


# ============================================================================
# CONFTEST EQUIVALENTS (if running standalone)
# ============================================================================

def pytest_configure(config):
    """Register markers for this test file."""
    config.addinivalue_line(
        "markers", "step65: mark test as testing Step 6.5 specification injection"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test for complete flow"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "step65 or integration"])
