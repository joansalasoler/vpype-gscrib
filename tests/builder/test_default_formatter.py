import pytest
import numpy as np
from typeguard import TypeCheckError
from vpype_mecode.builder.formatters import DefaultFormatter


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def formatter():
    return DefaultFormatter()


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

# Test initialization

def test_default_initialization(formatter):
    assert formatter._decimal_places == 5
    assert formatter._labels == {"x": "X", "y": "Y", "z": "Z"}
    assert formatter._comment_template == "; {}"

# Test axis label settings

def test_set_axis_label_valid(formatter):
    formatter.set_axis_label("x", "A")
    assert formatter._labels["x"] == "A"

def test_set_axis_label_invalid_axis(formatter):
    with pytest.raises(ValueError):
        formatter.set_axis_label("w", "A")

def test_set_axis_label_empty(formatter):
    with pytest.raises(ValueError):
        formatter.set_axis_label("x", "  ")

# Test comment symbols

def test_set_comment_symbols_standard(formatter):
    formatter.set_comment_symbols(";")
    assert formatter._comment_template == "; {}"

def test_set_comment_symbols_parentheses(formatter):
    formatter.set_comment_symbols("(")
    assert formatter._comment_template == "( {} )"

def test_set_comment_symbols_empty(formatter):
    with pytest.raises(ValueError):
        formatter.set_comment_symbols("  ")

# Test decimal places

def test_set_decimal_places_valid(formatter):
    formatter.set_decimal_places(3)
    assert formatter._decimal_places == 3

def test_set_decimal_places_zero(formatter):
    formatter.set_decimal_places(0)
    assert formatter._decimal_places == 0

def test_set_decimal_places_negative(formatter):
    with pytest.raises(ValueError):
        formatter.set_decimal_places(-1)

# Test comment formatting

def test_format_comment_default(formatter):
    assert formatter.format_comment("Test") == "; Test"

def test_format_comment_empty(formatter):
    formatter.set_comment_symbols("[")
    assert formatter.format_comment("") == "[  ]"

# Test number formatting

def test_format_number_comprehensive(formatter):
    assert formatter.format_number(42) == "42"
    assert formatter.format_number(3.14159) == "3.14159"
    assert formatter.format_number(-42.123) == "-42.123"
    assert formatter.format_number(0) == "0"
    assert formatter.format_number(-0) == "0"
    assert formatter.format_number(0.0) == "0"
    assert formatter.format_number(1e-4) == "0.0001"
    assert formatter.format_number(1.2e1) == "12"
    assert formatter.format_number(np.int32(42)) == "42"
    assert formatter.format_number(np.float64(-0.9)) == "-0.9"

def test_format_number_decimal_edge_cases(formatter):
    formatter.set_decimal_places(3)
    assert formatter.format_number(0.1234) == "0.123"
    assert formatter.format_number(0.999) == "0.999"
    assert formatter.format_number(0.9999) == "1"
    assert formatter.format_number(-0.9999) == "-1"
    assert formatter.format_number(0.001) == "0.001"
    assert formatter.format_number(-0.001) == "-0.001"
    assert formatter.format_number(0.0001) == "0"

def test_format_number_trailing_zeros(formatter):
    formatter.set_decimal_places(3)
    assert formatter.format_number(1.100) == "1.1"
    assert formatter.format_number(1.000) == "1"
    assert formatter.format_number(10.10) == "10.1"

def test_format_number_leading_zeros(formatter):
    assert formatter.format_number(.5) == "0.5"
    assert formatter.format_number(-.5) == "-0.5"

def test_format_number_invalid_types(formatter):
    with pytest.raises(ValueError):
        formatter.format_number(float("inf"))

    with pytest.raises(ValueError):
        formatter.format_number(float("-inf"))

    with pytest.raises(ValueError):
        formatter.format_number(float("nan"))

    with pytest.raises(TypeError):
        formatter.format_number(1 + 2j)

    with pytest.raises(TypeError):
        formatter.format_number(complex(1, 2))

    with pytest.raises(TypeCheckError):
        formatter.format_number("123")

    with pytest.raises(TypeCheckError):
        formatter.format_number(None)

# Test parameters formatting

def test_format_parameters_empty(formatter):
    assert formatter.format_parameters({}) == ""

def test_format_parameters_axes(formatter):
    params = {"x": 10.123, "y": 20.459, "z": 0}
    formatter.set_decimal_places(2)
    assert formatter.format_parameters(params) == "X10.12 Y20.46 Z0"

def test_format_parameters_custom(formatter):
    params = {"x": 10, "F": 1000, "comment": "test"}
    assert formatter.format_parameters(params) == "X10 F1000 commenttest"

# Test command formatting

def test_format_command_no_params(formatter):
    assert formatter.format_command("G0") == "G0"

def test_format_command_with_params(formatter):
    params = {"x": 10, "y": 20}
    assert formatter.format_command("G1", params) == "G1 X10 Y20"

def test_format_command_with_mixed_params(formatter):
    params = {"x": 10, "F": 1000, "T": "0102"}
    assert formatter.format_command("G1", params) == "G1 X10 F1000 T0102"

# Test line formatting

def test_format_line_simple(formatter):
    result = formatter.format_line("G1 X0 Y0")
    assert result.endswith(formatter._line_endings)
    assert result.rstrip() == "G1 X0 Y0"

def test_format_line_with_trailing_spaces(formatter):
    result = formatter.format_line("G1 X0 Y0   ")
    assert result.rstrip() == "G1 X0 Y0"

def test_format_line_endings(formatter):
    formatter.set_line_endings("!")
    result = formatter.format_line("G1 X0 Y0  ")
    assert result.endswith(formatter._line_endings)
    assert result == "G1 X0 Y0!"

# Test complex scenarios

def test_full_gcode_line(formatter):
    params = {"x": 10.1231, "y": 20.45609, "F": 1000}
    formatter.set_decimal_places(3)
    command = formatter.format_command("G1", params)
    line = formatter.format_line(command)
    assert line.rstrip() == "G1 X10.123 Y20.456 F1000"

def test_custom_axis_labels_affect_formatting(formatter):
    params = {"x": 10, "y": 20, "z": 30}
    formatter.set_axis_label("x", "A")
    formatter.set_axis_label("y", "B")
    formatter.set_axis_label("z", "C")
    assert formatter.format_command("G1", params) == "G1 A10 B20 C30"
