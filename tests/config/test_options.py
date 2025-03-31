import pytest

from vpype_gscrib.config import BuilderConfig, RenderConfig
from vpype_gscrib.vpype_options import command_options


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def config_fields():
    return (
        RenderConfig.model_fields |
        BuilderConfig.model_fields
    )


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

def test_config_fields_unique():
    builder_fields = set(BuilderConfig.model_fields.keys())
    renderer_fields = set(RenderConfig.model_fields.keys())
    common_fields = builder_fields & renderer_fields
    assert not common_fields, f"Found overlapping fields: {common_fields}"

def test_config_fields_exist_for_options(config_fields):
    for option in (o for o in command_options if o.name != "config"):
        field = option.name.replace("-", "_")
        assert field in config_fields, f"Missing field: {field}"
