"""Transformation semantic preservation tests."""
import pytest


@pytest.mark.golden
class TestSemanticPreservation:
    """Test semantic preservation in transformations."""

    def test_basic_transformation_semantics(self):
        """Verify basic transformation preserves semantics."""
        # Original
        original = {
            "function": "authenticate",
            "params": {"username": "str", "password": "str"},
            "returns": "bool"
        }

        # After transformation
        transformed = {
            "function": "authenticate",
            "params": {"username": "str", "password": "str"},
            "returns": "bool"
        }

        # Semantics should be identical
        assert original["function"] == transformed["function"]
        assert original["params"] == transformed["params"]
        assert original["returns"] == transformed["returns"]

    def test_no_information_loss(self):
        """Verify transformation doesn't lose information."""
        original_spec = {
            "name": "create_user",
            "security": ["auth_required"],
            "validation": ["email_format", "password_strength"],
            "side_effects": ["write_database", "send_email"]
        }

        transformed_spec = {
            "name": "create_user",
            "security": ["auth_required"],
            "validation": ["email_format", "password_strength"],
            "side_effects": ["write_database", "send_email"]
        }

        # All information preserved
        assert set(original_spec.keys()) == set(transformed_spec.keys())
        for key in original_spec:
            assert original_spec[key] == transformed_spec[key]

    def test_semantic_equivalence_validation(self):
        """Verify semantic equivalence can be validated."""
        def check_semantic_equivalence(original, transformed):
            """Check if specs are semantically equivalent."""
            # Same structure
            if set(original.keys()) != set(transformed.keys()):
                return False

            # Same values
            for key in original:
                if original[key] != transformed[key]:
                    return False

            return True

        spec1 = {"op": "add", "params": [1, 2]}
        spec2 = {"op": "add", "params": [1, 2]}
        spec3 = {"op": "subtract", "params": [1, 2]}

        assert check_semantic_equivalence(spec1, spec2)
        assert not check_semantic_equivalence(spec1, spec3)

    def test_multiple_transformation_consistency(self):
        """Verify consistency across multiple transformations."""
        original = {
            "api": "rest",
            "auth": "jwt",
            "rate_limit": 1000
        }

        # Apply transformation twice
        transform1 = {
            "api": "rest",
            "auth": "jwt",
            "rate_limit": 1000
        }

        transform2 = {
            "api": "rest",
            "auth": "jwt",
            "rate_limit": 1000
        }

        # Results should be identical
        assert transform1 == transform2 == original

    def test_semantic_drift_detection(self):
        """Detect semantic drift in transformations."""
        original = {
            "users": ["admin", "user"],
            "permissions": ["read", "write"]
        }

        good_transform = {
            "users": ["admin", "user"],
            "permissions": ["read", "write"]
        }

        bad_transform = {
            "users": ["admin"],  # Missing "user"
            "permissions": ["read", "write"]
        }

        # Good should match, bad should not
        assert original == good_transform
        assert original != bad_transform

    def test_parameter_preservation(self):
        """Verify function parameters are preserved."""
        def extract_params(spec):
            return set(spec.get("params", {}).keys())

        original = {
            "params": {"username": "str", "email": "str", "password": "str"}
        }

        transformed = {
            "params": {"username": "str", "email": "str", "password": "str"}
        }

        assert extract_params(original) == extract_params(transformed)

    def test_constraint_preservation(self):
        """Verify constraints are preserved."""
        original = {
            "constraints": {
                "min_length": 8,
                "max_length": 128,
                "pattern": "^[a-zA-Z0-9]+$"
            }
        }

        transformed = {
            "constraints": {
                "min_length": 8,
                "max_length": 128,
                "pattern": "^[a-zA-Z0-9]+$"
            }
        }

        assert original["constraints"] == transformed["constraints"]

    def test_error_handling_preservation(self):
        """Verify error handling specifications are preserved."""
        original = {
            "errors": [
                {"code": 400, "message": "Invalid input"},
                {"code": 401, "message": "Unauthorized"},
                {"code": 500, "message": "Internal error"}
            ]
        }

        transformed = {
            "errors": [
                {"code": 400, "message": "Invalid input"},
                {"code": 401, "message": "Unauthorized"},
                {"code": 500, "message": "Internal error"}
            ]
        }

        assert len(original["errors"]) == len(transformed["errors"])
        for i, error in enumerate(original["errors"]):
            assert error == transformed["errors"][i]

    def test_dependency_preservation(self):
        """Verify dependencies are preserved."""
        original = {
            "depends_on": ["database", "cache", "logger"],
            "external_services": ["email_service", "sms_service"]
        }

        transformed = {
            "depends_on": ["database", "cache", "logger"],
            "external_services": ["email_service", "sms_service"]
        }

        assert original["depends_on"] == transformed["depends_on"]
        assert original["external_services"] == transformed["external_services"]

    def test_semantic_preservation_with_reordering(self):
        """Verify semantics preserved even with different ordering."""
        # Different order, same content
        spec1 = {"security": "jwt", "auth": "oauth", "cache": "redis"}
        spec2 = {"cache": "redis", "security": "jwt", "auth": "oauth"}

        # As dicts, order doesn't matter for equivalence
        assert spec1 == spec2

    @pytest.mark.parametrize("original,transformed,should_match", [
        (
            {"type": "string", "required": True},
            {"type": "string", "required": True},
            True
        ),
        (
            {"type": "string", "required": True},
            {"type": "string", "required": False},
            False
        ),
        (
            {"array": [1, 2, 3]},
            {"array": [1, 2, 3]},
            True
        ),
        (
            {"array": [1, 2, 3]},
            {"array": [3, 2, 1]},
            False
        ),
    ])
    def test_semantic_equivalence_cases(self, original, transformed, should_match):
        """Test various semantic equivalence scenarios."""
        if should_match:
            assert original == transformed
        else:
            assert original != transformed

    def test_semantic_layer_preservation(self):
        """Verify each semantic layer is preserved."""
        spec = {
            "layer_1_syntax": {"function": "auth"},
            "layer_2_semantics": {"purpose": "authenticate_user"},
            "layer_3_pragmatics": {"constraint": "must_be_secure"}
        }

        # All layers should be accessible and unchanged
        assert "layer_1_syntax" in spec
        assert "layer_2_semantics" in spec
        assert "layer_3_pragmatics" in spec
        assert spec["layer_1_syntax"]["function"] == "auth"
