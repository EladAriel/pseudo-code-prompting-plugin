"""
Tests for WORKFLOW_CONTINUES protocol - validates workflow state transitions.
"""
import pytest


@pytest.mark.chaining
@pytest.mark.unit
def test_agent_continues_on_task_completion(mock_transform_agent, orchestrator_mock):
    """Test agent outputs WORKFLOW_CONTINUES: YES upon task completion."""
    # Arrange
    query = "implement authentication"

    # Act
    transform_output = mock_transform_agent(query)
    should_continue = orchestrator_mock.should_continue(transform_output)

    # Assert
    assert transform_output["WORKFLOW_CONTINUES"] == "YES"
    assert should_continue is True
    assert "NEXT_AGENT" in transform_output
    assert transform_output["NEXT_AGENT"] == "requirement-validator"


@pytest.mark.chaining
@pytest.mark.unit
def test_workflow_state_persistence(
    mock_transform_agent,
    mock_validator_agent,
    mock_optimizer_agent,
    orchestrator_mock,
    workflow_memory_state,
    empty_active_context,
    empty_patterns,
    empty_progress
):
    """Test memory persists across workflow steps."""
    # Arrange: Take snapshot of initial state
    workflow_memory_state.snapshot("initial")
    orchestrator_mock.reset()

    # Act: Execute transform step
    transform_output = mock_transform_agent("implement auth")
    orchestrator_mock.get_next_agent(transform_output)
    orchestrator_mock.update_memory("step", "transform_completed")

    # Act: Execute validator step
    validator_output = mock_validator_agent(transform_output["output"])
    orchestrator_mock.get_next_agent(validator_output)
    orchestrator_mock.update_memory("step", "validator_completed")

    # Act: Execute optimizer step
    optimizer_output = mock_optimizer_agent(
        transform_output["output"],
        validator_output["output"]
    )
    # Track optimizer manually since it's the final step
    orchestrator_mock.execution_log.append(optimizer_output["agent_name"])
    orchestrator_mock.update_memory("step", "optimizer_completed")

    # Assert: Memory updates were tracked
    assert len(orchestrator_mock.memory_updates) == 3
    assert orchestrator_mock.memory_updates[0]["key"] == "step"
    assert orchestrator_mock.memory_updates[1]["value"] == "validator_completed"
    assert orchestrator_mock.memory_updates[2]["value"] == "optimizer_completed"

    # Assert: Execution order is correct
    execution_order = orchestrator_mock.get_execution_order()
    assert execution_order == [
        "prompt-transformer",
        "requirement-validator",
        "prompt-optimizer"
    ]


@pytest.mark.chaining
@pytest.mark.unit
def test_multi_step_execution_chain(
    mock_transform_agent,
    mock_validator_agent,
    mock_optimizer_agent,
    orchestrator_mock
):
    """Test complete chain execution: transform → validate → optimize."""
    # Arrange
    query = "create REST API with authentication"
    orchestrator_mock.reset()

    # Act: Step 1 - Transform
    transform_output = mock_transform_agent(query)
    assert orchestrator_mock.should_continue(transform_output)
    next_agent_1 = orchestrator_mock.get_next_agent(transform_output)
    assert next_agent_1 == "requirement-validator"

    # Act: Step 2 - Validate
    validator_output = mock_validator_agent(transform_output["output"])
    assert orchestrator_mock.should_continue(validator_output)
    next_agent_2 = orchestrator_mock.get_next_agent(validator_output)
    assert next_agent_2 == "prompt-optimizer"

    # Act: Step 3 - Optimize
    optimizer_output = mock_optimizer_agent(
        transform_output["output"],
        validator_output["output"]
    )
    # Track optimizer invocation manually (not through get_next_agent since it terminates)
    orchestrator_mock.execution_log.append(optimizer_output["agent_name"])
    assert not orchestrator_mock.should_continue(optimizer_output)
    assert optimizer_output["WORKFLOW_CONTINUES"] == "NO"

    # Assert: Chain complete signals
    assert "CHAIN_COMPLETE" in optimizer_output
    assert optimizer_output["CHAIN_COMPLETE"] == "All steps finished"
    assert "TODO_LIST" in optimizer_output
    assert len(optimizer_output["TODO_LIST"]) > 0

    # Assert: Execution order is sequential
    execution_order = orchestrator_mock.get_execution_order()
    assert len(execution_order) == 3
    assert execution_order[0] == "prompt-transformer"
    assert execution_order[1] == "requirement-validator"
    assert execution_order[2] == "prompt-optimizer"


@pytest.mark.chaining
@pytest.mark.unit
def test_error_recovery_continuation(
    mock_agent_response_factory,
    orchestrator_mock
):
    """Test workflow continues gracefully when validation issues found."""
    # Arrange: Create validator output with warnings but continue signal
    validator_output = mock_agent_response_factory(
        agent_name="requirement-validator",
        output_content=(
            "Validation Report:\n"
            "⚠️ WARNINGS (2):\n"
            "- Missing error handling\n"
            "- Consider adding rate limiting\n"
            "\n✓ PASSED: Structure valid"
        ),
        workflow_continues=True,
        next_agent="prompt-optimizer",
        chain_progress="prompt-transformer ✓ → requirement-validator [2/3] → prompt-optimizer"
    )

    # Act: Check if workflow should continue despite warnings
    should_continue = orchestrator_mock.should_continue(validator_output)
    next_agent = orchestrator_mock.get_next_agent(validator_output)

    # Assert: Workflow continues to optimizer even with warnings
    assert should_continue is True
    assert next_agent == "prompt-optimizer"
    assert "WARNINGS" in validator_output["output"]
    assert validator_output["WORKFLOW_CONTINUES"] == "YES"


@pytest.mark.chaining
@pytest.mark.unit
def test_chain_progress_tracking(
    mock_transform_agent,
    mock_validator_agent,
    mock_optimizer_agent
):
    """Test CHAIN_PROGRESS signals show correct step numbers."""
    # Act
    transform_output = mock_transform_agent("implement feature")
    validator_output = mock_validator_agent(transform_output["output"])
    optimizer_output = mock_optimizer_agent(
        transform_output["output"],
        validator_output["output"]
    )

    # Assert: Progress indicators show correct step numbers
    assert "[1/3]" in transform_output["CHAIN_PROGRESS"]
    assert "[2/3]" in validator_output["CHAIN_PROGRESS"]
    assert "[3/3]" in optimizer_output["CHAIN_PROGRESS"]

    # Assert: Progress shows completion markers
    assert "✓" in validator_output["CHAIN_PROGRESS"]
    assert "✓" in optimizer_output["CHAIN_PROGRESS"]


@pytest.mark.chaining
@pytest.mark.unit
def test_workflow_termination_on_final_step(mock_optimizer_agent):
    """Test workflow terminates with NO signal on final step."""
    # Act
    optimizer_output = mock_optimizer_agent("pseudo_code", "validation_report")

    # Assert: Final step terminates chain
    assert optimizer_output["WORKFLOW_CONTINUES"] == "NO"
    assert "NEXT_AGENT" not in optimizer_output
    assert "CHAIN_COMPLETE" in optimizer_output
    assert "TODO_LIST" in optimizer_output
    assert isinstance(optimizer_output["TODO_LIST"], list)
    assert len(optimizer_output["TODO_LIST"]) > 0
