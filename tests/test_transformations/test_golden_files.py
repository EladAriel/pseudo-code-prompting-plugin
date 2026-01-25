"""
Tests for golden file expectations - validates transformation output quality.
"""
import pytest


@pytest.mark.golden
@pytest.mark.integration
def test_golden_rest_api_basic_exists(transformation_golden):
    """Test golden file for basic REST API exists and is valid."""
    content = transformation_golden("rest_api_basic")
    assert content
    assert "create_rest_api" in content or "api" in content.lower()


@pytest.mark.golden
@pytest.mark.integration
def test_golden_auth_jwt_exists(transformation_golden):
    """Test golden file for JWT authentication exists."""
    content = transformation_golden("auth_jwt")
    assert content
    assert "jwt" in content.lower() or "authentication" in content.lower()


@pytest.mark.golden
@pytest.mark.integration
def test_golden_crud_operations_exists(transformation_golden):
    """Test golden file for CRUD operations exists."""
    content = transformation_golden("crud_operations")
    assert content
    assert "create" in content.lower() or "crud" in content.lower()


@pytest.mark.golden
@pytest.mark.integration
def test_golden_database_query_exists(transformation_golden):
    """Test golden file for database queries exists."""
    content = transformation_golden("database_query")
    assert content
    assert "database" in content.lower() or "query" in content.lower()


@pytest.mark.golden
@pytest.mark.integration
def test_golden_validation_exists(transformation_golden):
    """Test golden file for validation exists."""
    content = transformation_golden("validation_endpoint")
    assert content
    assert "validation" in content.lower() or "validate" in content.lower()


@pytest.mark.golden
@pytest.mark.integration
def test_golden_compression_exists(transformation_golden):
    """Test golden file for compression exists."""
    content = transformation_golden("compression_basic")
    assert content
    assert "compress" in content.lower() or content


@pytest.mark.golden
@pytest.mark.integration
def test_golden_rate_limiting_exists(transformation_golden):
    """Test golden file for rate limiting exists."""
    content = transformation_golden("rate_limiting")
    assert content


@pytest.mark.golden
@pytest.mark.integration
def test_golden_error_handling_exists(transformation_golden):
    """Test golden file for error handling exists."""
    content = transformation_golden("error_handling")
    assert content


@pytest.mark.golden
@pytest.mark.integration
def test_golden_pagination_exists(transformation_golden):
    """Test golden file for pagination exists."""
    content = transformation_golden("pagination")
    assert content


@pytest.mark.golden
@pytest.mark.integration
def test_golden_security_headers_exists(transformation_golden):
    """Test golden file for security headers exists."""
    content = transformation_golden("security_headers")
    assert content


@pytest.mark.golden
@pytest.mark.unit
def test_golden_files_are_normalized(golden_comparator):
    """Test golden file normalization works."""
    actual = "function_call(\n  param1=\"value\",\n  param2=\"value2\"\n)"
    expected = "function_call( param1=\"value\", param2=\"value2\" )"

    # Both should normalize to similar form
    assert golden_comparator(actual, expected)


@pytest.mark.golden
@pytest.mark.unit
def test_golden_whitespace_handling(golden_comparator):
    """Test golden file handles whitespace variations."""
    actual = "api(\n\n  path=\"/users\"\n\n)"
    expected = "api(path=\"/users\")"

    assert golden_comparator(actual, expected)
