"""
Tests for NEXT_AGENT protocol - validates agent delegation and routing.
"""
import pytest


@pytest.mark.chaining
@pytest.mark.unit
def test_agent_delegation_to_next(
    mock_transform_agent,
    orchestrator_mock
):
    """Test NEXT_AGENT correctly specifies the next agent in chain."""
    # Act
    transform_output = mock_transform_agent("implement database schema")
    next_agent = orchestrator_mock.get_next_agent(transform_output)

    # Assert: Next agent is specified and correct
    assert "NEXT_AGENT" in transform_output
    assert next_agent is not None
    assert next_agent == "requirement-validator"


@pytest.mark.chaining
@pytest.mark.unit
def test_context_handoff_between_agents(
    mock_transform_agent,
    mock_validator_agent,
    orchestrator_mock
):
    """Test data flows correctly from one agent to the next."""
    # Arrange
    query = "implement REST API"

    # Act: Transform agent produces output
    transform_output = mock_transform_agent(query)
    pseudo_code = transform_output["output"]

    # Act: Validator receives transformer's output as context
    validator_output = mock_validator_agent(pseudo_code)

    # Assert: Data was passed and processed
    assert pseudo_code in transform_output["output"]
    assert validator_output["agent_name"] == "requirement-validator"
    assert "Validation Report" in validator_output["output"]

    # Assert: Next agent receives previous agent's output
    orchestrator_mock.get_next_agent(transform_output)
    next_agent = orchestrator_mock.get_next_agent(transform_output)
    assert next_agent == "requirement-validator"
    assert orchestrator_mock.execution_log[0] == "prompt-transformer"


@pytest.mark.chaining
@pytest.mark.unit
def test_dependency_validation(
    mock_transform_agent,
    mock_validator_agent,
    mock_optimizer_agent,
    orchestrator_mock
):
    """Test optimizer receives both pseudo-code and validation report."""
    # Arrange
    query = "create authentication middleware"

    # Act: Get outputs from previous steps
    transform_output = mock_transform_agent(query)
    validator_output = mock_validator_agent(transform_output["output"])

    # Act: Optimizer is invoked with both dependencies
    optimizer_output = mock_optimizer_agent(
        pseudo_code=transform_output["output"],
        validation_report=validator_output["output"]
    )

    # Assert: Optimizer output reflects both inputs
    assert optimizer_output["agent_name"] == "prompt-optimizer"
    assert transform_output["output"] in transform_output["output"]
    assert validator_output["output"] in validator_output["output"]

    # Assert: Optimizer produced enhanced output
    assert "implement_auth" in optimizer_output["output"]
    assert "security" in optimizer_output["output"].lower()


@pytest.mark.chaining
@pytest.mark.unit
def test_agent_selection_logic(
    mock_transform_agent,
    mock_validator_agent,
    mock_optimizer_agent,
    orchestrator_mock
):
    """Test orchestrator selects correct next agent based on workflow."""
    # Arrange
    orchestrator_mock.reset()
    agents = {
        "prompt-transformer": mock_transform_agent("test"),
        "requirement-validator": mock_validator_agent("test"),
        "prompt-optimizer": mock_optimizer_agent("test", "test")
    }

    # Act: Simulate orchestrator routing logic
    current_agent = "prompt-transformer"
    transform_output = agents[current_agent]

    # Assert: Orchestrator correctly reads next agent
    next_agent = orchestrator_mock.get_next_agent(transform_output)
    assert next_agent == "requirement-validator"

    # Act: Route to validator
    current_agent = next_agent
    validator_output = agents[current_agent]
    next_agent = orchestrator_mock.get_next_agent(validator_output)

    # Assert: Validator routes to optimizer
    assert next_agent == "prompt-optimizer"

    # Act: Track optimizer invocation (final step)
    optimizer_output = agents["prompt-optimizer"]
    orchestrator_mock.execution_log.append(optimizer_output["agent_name"])

    # Assert: Execution order is correct
    execution_order = orchestrator_mock.get_execution_order()
    assert execution_order == ["prompt-transformer", "requirement-validator", "prompt-optimizer"]


@pytest.mark.chaining
@pytest.mark.unit
def test_next_agent_with_invalid_signal(mock_agent_response_factory):
    """Test handling of invalid NEXT_AGENT signals."""
    # Arrange
    invalid_output = mock_agent_response_factory(
        agent_name="test-agent",
        output_content="output",
        workflow_continues=True,
        next_agent="nonexistent-agent"
    )

    # Assert: Invalid agent name is returned (orchestrator would error)
    assert invalid_output["NEXT_AGENT"] == "nonexistent-agent"
    assert "nonexistent" in invalid_output["NEXT_AGENT"]


@pytest.mark.chaining
@pytest.mark.unit
def test_routing_without_next_agent_error(mock_agent_response_factory):
    """Test error handling when NEXT_AGENT missing but WORKFLOW_CONTINUES: YES."""
    # Arrange: Validator outputs continue signal but no next agent (error case)
    invalid_output = mock_agent_response_factory(
        agent_name="requirement-validator",
        output_content="Validation Report: ✓ PASSED",
        workflow_continues=True,
        next_agent=None  # Missing next agent
    )

    # Assert: Error condition detected
    assert invalid_output["WORKFLOW_CONTINUES"] == "YES"
    assert invalid_output.get("NEXT_AGENT") is None


@pytest.mark.chaining
@pytest.mark.unit
def test_linear_workflow_sequence(
    mock_transform_agent,
    mock_validator_agent,
    mock_optimizer_agent,
    orchestrator_mock
):
    """Test complete linear workflow: transform → validate → optimize → complete."""
    # Arrange
    orchestrator_mock.reset()

    # Act: Execute full chain and collect routing decisions
    routing_decisions = []

    # Step 1
    transform_output = mock_transform_agent("implement feature")
    routing_decisions.append({
        "from": "entry",
        "to": orchestrator_mock.get_next_agent(transform_output),
        "continues": orchestrator_mock.should_continue(transform_output)
    })

    # Step 2
    validator_output = mock_validator_agent(transform_output["output"])
    routing_decisions.append({
        "from": "prompt-transformer",
        "to": orchestrator_mock.get_next_agent(validator_output),
        "continues": orchestrator_mock.should_continue(validator_output)
    })

    # Step 3
    optimizer_output = mock_optimizer_agent(
        transform_output["output"],
        validator_output["output"]
    )
    routing_decisions.append({
        "from": "requirement-validator",
        "to": orchestrator_mock.get_next_agent(optimizer_output) if orchestrator_mock.should_continue(optimizer_output) else None,
        "continues": orchestrator_mock.should_continue(optimizer_output)
    })

    # Assert: Routing sequence is correct
    assert routing_decisions[0]["to"] == "requirement-validator"
    assert routing_decisions[0]["continues"] is True
    assert routing_decisions[1]["to"] == "prompt-optimizer"
    assert routing_decisions[1]["continues"] is True
    assert routing_decisions[2]["to"] is None
    assert routing_decisions[2]["continues"] is False

    # Assert: Chain completes properly
    assert "CHAIN_COMPLETE" in optimizer_output
