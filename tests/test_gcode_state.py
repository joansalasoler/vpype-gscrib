import pytest
from vpype_mecode.excepts import ToolStateError, CoolantStateError
from vpype_mecode.renderer import GState
from vpype_mecode.builder.enums import *
from vpype_mecode.enums import *


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def gstate():
    return GState()


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

def test_initial_state(gstate):
    assert gstate.current_tool_power == 0
    assert gstate.current_tool_number == 0
    assert gstate.current_spin_mode == SpinMode.OFF
    assert gstate.current_power_mode == PowerMode.OFF
    assert gstate.current_distance_mode == DistanceMode.ABSOLUTE
    assert gstate.current_coolant_mode == CoolantMode.OFF
    assert not gstate.is_tool_active
    assert not gstate.is_coolant_active

def test_set_length_units(gstate):
    gstate.set_length_units(LengthUnits.INCHES)
    assert gstate.current_length_units == LengthUnits.INCHES

def test_set_plane(gstate):
    gstate.set_plane(Plane.XY)
    assert gstate.current_plane == Plane.XY

def test_set_tool_power(gstate):
    gstate.set_tool_power(50.0)
    assert gstate.current_tool_power == 50.0

def test_set_tool_power_invalid():
    gstate = GState()

    with pytest.raises(ValueError):
        gstate.set_tool_power(-1.0)

def test_set_distance_mode(gstate):
    gstate.set_distance_mode(DistanceMode.RELATIVE)
    assert gstate.current_distance_mode == DistanceMode.RELATIVE

def test_set_coolant_mode(gstate):
    gstate.set_coolant_mode(CoolantMode.MIST)
    gstate.set_coolant_mode(CoolantMode.OFF)
    gstate.set_coolant_mode(CoolantMode.FLOOD)
    assert gstate.current_coolant_mode == CoolantMode.FLOOD
    assert gstate.is_coolant_active

def test_set_coolant_mode_off(gstate):
    gstate.set_coolant_mode(CoolantMode.OFF)
    assert gstate.current_coolant_mode == CoolantMode.OFF
    assert not gstate.is_coolant_active

def test_coolant_mode_already_active(gstate):
    gstate.set_coolant_mode(CoolantMode.FLOOD)

    with pytest.raises(CoolantStateError):
        gstate.set_coolant_mode(CoolantMode.MIST)

def test_set_spin_mode(gstate):
    gstate.set_spin_mode(SpinMode.COUNTER, 2000)
    gstate.set_spin_mode(SpinMode.OFF)
    gstate.set_spin_mode(SpinMode.CLOCKWISE, 1000)
    assert gstate.current_spin_mode == SpinMode.CLOCKWISE
    assert gstate.current_tool_power == 1000
    assert gstate.is_tool_active

def test_set_spin_mode_off(gstate):
    gstate.set_spin_mode(SpinMode.OFF)
    assert gstate.current_spin_mode == SpinMode.OFF
    assert not gstate.is_tool_active

def test_spin_mode_already_active(gstate):
    gstate.set_spin_mode(SpinMode.CLOCKWISE)

    with pytest.raises(ToolStateError):
        gstate.set_spin_mode(SpinMode.CLOCKWISE)

def test_spin_mode_off_already_active(gstate):
    gstate.set_spin_mode(SpinMode.CLOCKWISE)
    gstate.set_spin_mode(SpinMode.OFF)
    assert gstate.current_spin_mode == SpinMode.OFF
    assert gstate.current_tool_power == 0

def test_set_power_mode(gstate):
    gstate.set_power_mode(PowerMode.DYNAMIC, 100.0)
    gstate.set_power_mode(PowerMode.OFF)
    gstate.set_power_mode(PowerMode.CONSTANT, 75.0)
    assert gstate.current_power_mode == PowerMode.CONSTANT
    assert gstate.current_tool_power == 75.0
    assert gstate.is_tool_active

def test_set_power_mode_off(gstate):
    gstate.set_power_mode(PowerMode.OFF)
    assert gstate.current_power_mode == PowerMode.OFF
    assert not gstate.is_tool_active

def test_power_mode_already_active(gstate):
    gstate.set_power_mode(PowerMode.CONSTANT, 75.0)

    with pytest.raises(ToolStateError):
        gstate.set_power_mode(PowerMode.DYNAMIC, 50.0)

def test_power_mode_off_already_active(gstate):
    gstate.set_power_mode(PowerMode.DYNAMIC, 50.0)
    gstate.set_power_mode(PowerMode.OFF)
    assert gstate.current_power_mode == PowerMode.OFF
    assert gstate.current_tool_power == 0

def test_set_tool_number(gstate):
    gstate.set_tool_number(ToolSwapMode.MANUAL, 101)
    assert gstate.current_tool_swap_mode == ToolSwapMode.MANUAL
    assert gstate.current_tool_number == 101

def test_set_tool_invalid_tool():
    gstate = GState()

    with pytest.raises(ValueError):
        gstate.set_tool_number(ToolSwapMode.MANUAL, 0)

    with pytest.raises(ValueError):
        gstate.set_tool_number(ToolSwapMode.MANUAL, -1)

def test_set_tool_with_active_tool(gstate):
    gstate.set_power_mode(PowerMode.CONSTANT, 75.0)

    with pytest.raises(ToolStateError):
        gstate.set_tool_number(ToolSwapMode.MANUAL, 1)

def test_set_tool_with_active_coolant(gstate):
    gstate.set_coolant_mode(CoolantMode.FLOOD)

    with pytest.raises(CoolantStateError):
        gstate.set_tool_number(ToolSwapMode.MANUAL, 1)

def test_set_halt_mode(gstate):
    gstate.set_halt_mode(HaltMode.PAUSE)
    assert gstate.current_halt_mode == HaltMode.PAUSE

def test_set_halt_mode_off(gstate):
    gstate.set_coolant_mode(CoolantMode.FLOOD)
    gstate.set_halt_mode(HaltMode.OFF)
    assert gstate.current_halt_mode == HaltMode.OFF

def test_set_halt_mode_with_active_tool(gstate):
    gstate.set_power_mode(PowerMode.CONSTANT, 75.0)

    with pytest.raises(ToolStateError):
        gstate.set_halt_mode(HaltMode.OPTIONAL_PAUSE)

def test_set_halt_mode_with_active_coolant(gstate):
    gstate.set_coolant_mode(CoolantMode.FLOOD)

    with pytest.raises(CoolantStateError):
        gstate.set_halt_mode(HaltMode.END_WITH_RESET)
