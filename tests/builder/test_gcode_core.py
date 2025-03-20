import math
import pytest
from math import inf

from vpype_mecode.builder import Point
from vpype_mecode.builder import CoreGBuilder
from vpype_mecode.builder.writers import BaseWriter


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def mock_writer():
    return MockWriter()

@pytest.fixture
def builder(mock_writer):
    builder = CoreGBuilder()
    builder._writers = [mock_writer]
    return builder

class MockWriter(BaseWriter):
    def __init__(self):
        self.written_lines = []
        self.is_connected = False

    def connect(self):
        self.is_connected = True

    def disconnect(self, wait=True):
        self.is_connected = False

    def write(self, data: bytes, requires_response=False):
        self.written_lines.append(data.decode('utf-8').strip())


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

# Test Initialization

def test_default_initialization():
    builder = CoreGBuilder()
    assert builder.position == Point.unknown()
    assert not builder.is_relative
    assert len(builder._writers) > 0

def test_custom_initialization():
    builder = CoreGBuilder(
        output="test.gcode",
        print_lines=True,
        decimal_places=3,
        comment_symbols=";",
        x_axis="A",
        y_axis="B",
        z_axis="C"
    )
    assert len(builder._writers) >= 2  # File and stdout writers
    assert builder.formatter._decimal_places == 3
    assert builder.formatter._labels == {"x": "A", "y": "B", "z": "C"}

# Test distance modes

def test_absolute_mode(builder, mock_writer):
    builder.absolute()
    assert not builder.is_relative
    assert "G90" in mock_writer.written_lines

def test_relative_mode(builder, mock_writer):
    builder.relative()
    assert builder.is_relative
    assert "G91" in mock_writer.written_lines

def test_mode_switching(builder, mock_writer):
    builder.relative()
    builder.absolute()
    builder.relative()
    assert "G91" in mock_writer.written_lines
    assert "G90" in mock_writer.written_lines
    assert builder.is_relative

# Test position management

def test_set_axis_position(builder, mock_writer):
    builder.set_axis_position(x=10, y=20, z=30)
    assert builder.position == Point(10, 20, 30)
    assert "G92 X10 Y20 Z30" in mock_writer.written_lines

def test_set_axis_position_partial(builder, mock_writer):
    builder.set_axis_position(x=10)
    assert builder.position == Point(10, -inf, -inf)
    assert "G92 X10" in mock_writer.written_lines

def test_set_axis_position_additional_axis(builder, mock_writer):
    builder.set_axis_position(x=10, E=20)
    assert builder.position == Point(10, -inf, -inf)
    assert "G92 X10 E20" in mock_writer.written_lines
    assert builder.get_parameter('E') == 20

def test_get_parameter(builder):
    builder.move(x=10, y=20, F=1000)
    assert builder.get_parameter('F') == 1000

# Test movement commands

def test_rapid_move(builder, mock_writer):
    builder.rapid(x=10, y=20, z=30)
    assert builder.position == Point(10, 20, 30)
    assert "G0 X10 Y20 Z30" in mock_writer.written_lines

def test_linear_move(builder, mock_writer):
    builder.move(x=10, y=20, z=30)
    assert builder.position == Point(10, 20, 30)
    assert "G1 X10 Y20 Z30" in mock_writer.written_lines

def test_relative_moves(builder, mock_writer):
    builder.relative()
    builder.move(x=10, y=20)
    builder.move(x=10, y=20)
    assert builder.position == Point(20, 40, 0)

def test_absolute_moves(builder, mock_writer):
    builder.absolute()
    builder.move(x=10, y=20)
    builder.move(x=5, y=15)
    assert builder.position == Point(5, 15, 0)

# Test transformations

def test_translation(builder, mock_writer):
    builder.translate(10, 20, 0)
    builder.move(x=0, y=0)
    assert "G1 X10 Y20" in mock_writer.written_lines

def test_rotation(builder, mock_writer):
    builder.rotate(math.pi / 2)  # 90 degrees
    builder.move(x=10, y=0)
    written_line = mock_writer.written_lines[-1]
    assert "G1" in written_line
    assert "Y10" in written_line
    assert "X0" in written_line

def test_scaling(builder, mock_writer):
    builder.scale(2)
    builder.move(x=10, y=10)
    assert "G1 X20 Y20" in mock_writer.written_lines

def test_reflection(builder, mock_writer):
    builder.reflect([1, 1, 0])
    builder.move(x=10, y=10)
    assert "G1 X-10 Y-10" in mock_writer.written_lines

def test_matrix_stack(builder, mock_writer):
    builder.translate(10, 0)
    builder.push_matrix()
    builder.translate(10, 0)
    builder.move(x=0, y=0)
    builder.pop_matrix()
    builder.move(x=0, y=0)
    assert "G1 X20 Y0" in mock_writer.written_lines
    assert "G1 X10 Y0" in mock_writer.written_lines

def test_combined_transformations(builder, mock_writer):
    builder.translate(10, 0)
    builder.rotate(math.pi / 2)
    builder.scale(2)
    builder.move(x=5, y=0)
    assert builder.position == Point(5, 0, 0)
    assert "G1 X0 Y30" in mock_writer.written_lines[-1]

def test_relative_with_transformations(builder, mock_writer):
    builder.translate(10, 0)
    builder.relative()
    builder.move(x=5, y=0)
    builder.move(x=5, y=0)
    assert builder.position == Point(10, 0, 0)
    assert "G1 X15 Y0" in mock_writer.written_lines
    assert "G1 X20 Y0" in mock_writer.written_lines

# Test comments

def test_comment_writing(builder, mock_writer):
    builder.comment("Test comment")
    assert "; Test comment" in mock_writer.written_lines

def test_comment_with_args(builder, mock_writer):
    builder.comment("Position", "X:", 10, "Y:", 20)
    assert "; Position X: 10 Y: 20" in mock_writer.written_lines

# Test multiple writers

def test_multiple_writers():
    writer1 = MockWriter()
    writer2 = MockWriter()
    builder = CoreGBuilder()
    builder._writers = [writer1, writer2]

    builder.move(x=10)
    assert len(writer1.written_lines) == 1
    assert len(writer2.written_lines) == 1
    assert writer1.written_lines == writer2.written_lines

# Test resource management

def test_context_manager():
    mock_writer = MockWriter()

    with CoreGBuilder() as builder:
        builder._writers = [mock_writer]
        builder.move(x=10)

    assert not mock_writer.is_connected

def test_teardown(builder, mock_writer):
    builder.move(x=10)
    builder.teardown()
    assert not mock_writer.is_connected
