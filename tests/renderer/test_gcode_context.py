import pytest
from unittest.mock import Mock
from dataclasses import FrozenInstanceError
from gscrib import GCodeBuilder
from vpype_gscrib.renderer import GContext
from vpype_gscrib.config import RenderConfig
from gscrib.enums import LengthUnits
from vpype_gscrib.heightmaps import BaseHeightMap


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def mock_gbuilder():
    return Mock(spec=GCodeBuilder)

@pytest.fixture
def mock_gcontext(mock_gbuilder, render_config):
    return GContext(mock_gbuilder, render_config)

@pytest.fixture
def render_config():
    return create_test_render_config({
        'length_units': LengthUnits.MILLIMETERS,
        'work_speed': 1000.0,
        'plunge_speed': 500.0,
        'travel_speed': 2000.0,
        'plunge_z': 2.0,
        'work_z': 1.0,
    })

def create_test_render_config(values_dict):
    return RenderConfig.model_validate(values_dict)


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

def test_gcontext_initialization(mock_gbuilder, render_config):
    ctx = GContext(mock_gbuilder, render_config)
    assert ctx.g == mock_gbuilder
    assert getattr(ctx, 'plunge_z') == 2.0
    assert getattr(ctx, 'work_z') == 1.0
    assert isinstance(ctx.height_map, BaseHeightMap)

def test_gcontext_property_immutability(mock_gcontext):
    with pytest.raises(FrozenInstanceError):
        mock_gcontext.work_speed = 2000.0

def test_format_config_values(mock_gcontext):
    result = mock_gcontext.format_config_values()
    assert isinstance(result, dict)
    assert 'length_units' in result
    assert 'travel_speed' in result
    assert 'work_z' in result

def test_scale_length_millimeters(mock_gbuilder):
    render_config = create_test_render_config({
        'length_units': LengthUnits.MILLIMETERS,
    })

    ctx = GContext(mock_gbuilder, render_config)
    value_in_mm = ctx.scale_length(100.0) # 100px
    expected_value = 100.0 * 25.4 / 96.0 # px to mm
    assert value_in_mm == pytest.approx(expected_value)

def test_scale_length_inches(mock_gbuilder):
    render_config = create_test_render_config({
        'length_units': LengthUnits.INCHES,
    })

    ctx = GContext(mock_gbuilder, render_config)
    value_in_inches = ctx.scale_length(100.0) # 1000px
    expected_value = 100.0 / 96.0 # px to inch
    assert value_in_inches == pytest.approx(expected_value)

def test_scaled_properties(mock_gbuilder, render_config):
    for field_name in GContext._scale_speeds:
        setattr(render_config, field_name, 1000.0) # 1000px
        ctx = GContext(mock_gbuilder, render_config)
        scaled_value = getattr(ctx, field_name) # mm
        expected = 1000.0 * 25.4 / 96.0 # px to mm
        assert scaled_value == pytest.approx(expected)
