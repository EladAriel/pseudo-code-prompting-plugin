#!/usr/bin/env python3
"""
Stage Output Filter Utility Module

Provides reusable extraction patterns and formatters for complete-process pipeline stages:
- Transform stage: Extract ONLY pseudo-code function
- Validate stage: Keep FULL validation report
- Optimize stage: Extract ONLY optimized code + TODOs

Each stage has specific filtering requirements to minimize context while preserving clarity.
"""

import re
from typing import Tuple, Optional, Dict, List


class StageOutputFilter:
    """Filter outputs based on transformation pipeline stage."""

    # Regex patterns for detecting stage markers
    WORKFLOW_MARKER_PATTERN = r'WORKFLOW_CONTINUES:\s*("YES"|"NO"|YES|NO)'
    NEXT_AGENT_PATTERN = r'NEXT_AGENT:\s*["\']?(\w+)["\']?'
    TODO_LIST_PATTERN = r'TODO_LIST:\s*\[(.*?)\](?:\s|$)'
    CHAIN_COMPLETE_PATTERN = r'CHAIN_COMPLETE:\s*(.+?)(?:\n|$)'

    # Stage output markers
    TRANSFORM_MARKER = r'Transformed:\s*'
    VALIDATE_MARKER = r'Validation Report:|VALIDATION REPORT:'
    OPTIMIZE_MARKER = r'Optimized:\s*'
    PSEUDO_CODE_PATTERN = r'(\w+\([^)]*\))'  # function_name(params)

    @staticmethod
    def detect_stage(output: str) -> Optional[str]:
        """
        Detect which stage just completed based on output markers.

        Args:
            output: Raw output from completed agent

        Returns:
            Stage name: 'transform', 'validate', 'optimize', or None if cannot detect
        """
        if not output:
            return None

        # Check workflow markers to identify stage progression
        workflow_match = re.search(StageOutputFilter.WORKFLOW_MARKER_PATTERN, output)
        next_agent_match = re.search(StageOutputFilter.NEXT_AGENT_PATTERN, output)

        if not workflow_match:
            return None

        workflow_continues = workflow_match.group(1).strip('"').upper() == 'YES'

        if not workflow_continues:
            # Pipeline complete - this is the optimize stage final output
            if re.search(StageOutputFilter.OPTIMIZE_MARKER, output):
                return 'optimize'
            return 'optimize'  # Default to optimize if no more steps

        # Still continuing - check next agent
        if next_agent_match:
            next_agent = next_agent_match.group(1).lower()

            if 'requirement-validator' in next_agent or 'validator' in next_agent:
                return 'transform'
            elif 'prompt-optimizer' in next_agent or 'optimizer' in next_agent:
                return 'validate'

        return None

    @staticmethod
    def filter_transform_output(output: str) -> str:
        """
        Filter transform stage output - extract ONLY the pseudo-code function.

        Args:
            output: Raw output from prompt-transformer agent

        Returns:
            Filtered output with only the pseudo-code function
        """
        lines = output.split('\n')
        extracted_lines = []
        in_function = False
        paren_depth = 0

        for line in lines:
            # Look for function definition pattern
            if re.search(r'^\w+\s*\(', line):
                in_function = True

            if in_function:
                extracted_lines.append(line)
                paren_depth += line.count('(') - line.count(')')

                # Complete function definition when parentheses balanced
                if paren_depth == 0 and '(' in ''.join(extracted_lines):
                    break

        if extracted_lines:
            filtered = '\n'.join(extracted_lines).strip()
            return f"[TRANSFORM_COMPLETE]\n{filtered}\n[PROCEEDING_TO_VALIDATION]"

        # Fallback: look for any pseudo-code-like function
        pseudo_code_match = re.search(
            r'(Transformed:\s*)?(\w+\([^)]*\))',
            output,
            re.DOTALL
        )
        if pseudo_code_match:
            function = pseudo_code_match.group(2)
            return f"[TRANSFORM_COMPLETE]\n{function}\n[PROCEEDING_TO_VALIDATION]"

        # Last resort: return output as-is with marker
        return f"[TRANSFORM_COMPLETE]\n{output}\n[PROCEEDING_TO_VALIDATION]"

    @staticmethod
    def filter_validate_output(output: str) -> str:
        """
        Filter validate stage output - keep FULL validation report.

        Args:
            output: Raw output from requirement-validator agent

        Returns:
            Filtered output with complete validation details
        """
        # For validation, we want ALL the details - just add stage markers
        validation_section = output

        # Extract main validation report if available
        validation_match = re.search(
            r'(Validation Report:|VALIDATION REPORT:)(.*?)(?=\nOptimized:|$)',
            output,
            re.DOTALL
        )

        if validation_match:
            validation_section = validation_match.group(0)

        return f"[VALIDATE_COMPLETE]\n{validation_section.strip()}\n[PROCEEDING_TO_OPTIMIZATION]"

    @staticmethod
    def filter_optimize_output(output: str) -> str:
        """
        Filter optimize stage output - extract ONLY optimized code + TODOs.

        Args:
            output: Raw output from prompt-optimizer agent

        Returns:
            Filtered output with optimized pseudo-code and TODOs
        """
        result_parts = []

        # Extract optimized pseudo-code
        optimized_match = re.search(
            r'(Optimized:)?\s*(\w+\([^)]*(?:\n[^)]*)*\))',
            output,
            re.DOTALL
        )

        if optimized_match:
            optimized_code = optimized_match.group(2).strip()
            result_parts.append(optimized_code)
        else:
            # Fallback: look for any multi-line function definition
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'^\w+\s*\(', line):
                    # Collect lines until closing paren
                    func_lines = [line]
                    paren_count = line.count('(') - line.count(')')
                    for next_line in lines[i+1:]:
                        func_lines.append(next_line)
                        paren_count += next_line.count('(') - next_line.count(')')
                        if paren_count == 0:
                            break
                    result_parts.append('\n'.join(func_lines))
                    break

        # Extract TODOs
        todo_match = re.search(
            r'TODO_LIST:\s*\[(.*?)\]|\[TODOS\](.*?)(?:\n\[|$)',
            output,
            re.DOTALL
        )

        todos_section = ""
        if todo_match:
            todos_content = todo_match.group(1) or todo_match.group(2)
            todos_section = f"\n[TODOS]\n{todos_content}"
        else:
            # Look for TODO-like items
            todo_lines = [line for line in output.split('\n') if re.search(r'^\s*[-•✓]\s+', line)]
            if todo_lines:
                todos_section = f"\n[TODOS]\n" + '\n'.join(todo_lines)

        result = '[OPTIMIZE_COMPLETE]\n' + '\n'.join(result_parts) + todos_section
        return result

    @staticmethod
    def extract_todos(output: str) -> List[str]:
        """
        Extract TODO items from optimize output.

        Args:
            output: Output containing TODO items

        Returns:
            List of TODO items
        """
        todos = []

        # Pattern 1: Quoted list items
        quoted_items = re.findall(r'["\'](.*?)["\'](?:,|\s|$)', output)
        todos.extend([item.strip() for item in quoted_items if item.strip()])

        # Pattern 2: Markdown list items
        md_items = re.findall(r'^\s*[-•*]\s+(.+?)$', output, re.MULTILINE)
        todos.extend([item.strip() for item in md_items if item.strip()])

        # Pattern 3: Numbered items
        numbered_items = re.findall(r'^\s*\d+\.\s+(.+?)$', output, re.MULTILINE)
        todos.extend([item.strip() for item in numbered_items if item.strip()])

        # Remove duplicates while preserving order
        seen = set()
        unique_todos = []
        for todo in todos:
            if todo not in seen:
                seen.add(todo)
                unique_todos.append(todo)

        return unique_todos

    @staticmethod
    def is_pipeline_complete(output: str) -> bool:
        """
        Check if pipeline is marked as complete.

        Args:
            output: Agent output to check

        Returns:
            True if pipeline completion marker detected
        """
        return bool(re.search(
            r'WORKFLOW_CONTINUES:\s*("NO"|NO)|CHAIN_COMPLETE:',
            output
        ))

    @staticmethod
    def extract_improvements(output: str) -> List[str]:
        """
        Extract list of improvements made by optimizer.

        Args:
            output: Optimizer agent output

        Returns:
            List of improvement descriptions
        """
        improvements = []

        # Look for improvements section
        improvements_match = re.search(
            r'(?:IMPROVEMENTS?|Improvements?)[:\s]*(?:MADE|Applied)?:?\s*(.*?)(?=\n\n|\n\[|$)',
            output,
            re.DOTALL | re.IGNORECASE
        )

        if improvements_match:
            improvements_text = improvements_match.group(1)
            # Extract bullet items
            items = re.findall(r'[-•*✓]\s+(.+?)(?=\n[-•*✓]|\n\n|$)', improvements_text, re.DOTALL)
            improvements.extend([item.strip() for item in items])

        return improvements

    @staticmethod
    def format_stage_transition(from_stage: str, to_stage: str) -> str:
        """
        Format a stage transition message.

        Args:
            from_stage: Current stage name
            to_stage: Next stage name

        Returns:
            Formatted transition message
        """
        stage_descriptions = {
            'transform': 'Query Transformation',
            'validate': 'Requirement Validation',
            'optimize': 'Optimization & Enhancement'
        }

        from_desc = stage_descriptions.get(from_stage, from_stage)
        to_desc = stage_descriptions.get(to_stage, to_stage)

        return f"\n✓ {from_desc} complete\n→ Proceeding to {to_desc}...\n"
