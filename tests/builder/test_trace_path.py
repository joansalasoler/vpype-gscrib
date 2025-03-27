import pytest
import numpy as np
from vpype_mecode.builder import TracePath, GCodeCore
from vpype_mecode.builder.enums import Direction
from vpype_mecode.builder.writers import BaseWriter


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def tracer(builder):
    return TracePath(builder)

@pytest.fixture
def mock_writer():
    return MockWriter()

@pytest.fixture
def builder(mock_writer):
    builder = GCodeCore()
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

    def write(self, data: bytes):
        self.written_lines.append(data.decode('utf-8').strip())


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

# Test initialization

def test_initialization(tracer):
    assert tracer._direction == Direction.CLOCKWISE
    assert tracer._resolution == 0.1

def test_select_resolution(tracer):
    tracer.select_resolution(0.5)
    assert tracer._resolution == 0.5

def test_select_direction(tracer):
    tracer.select_direction("ccw")
    assert tracer._direction == Direction.COUNTER
    tracer.select_direction(Direction.CLOCKWISE)
    assert tracer._direction == Direction.CLOCKWISE

# Test path functions

def test_arc_quarter_circle(tracer, builder):
    builder.move(x=10, y=0)
    tracer.select_resolution(2.0)
    tracer.arc(target=(0, 10), center=(-10, 0))
    final_pos = builder.position
    assert np.isclose(final_pos.x, 0, atol=0.1)
    assert np.isclose(final_pos.y, 10, atol=0.1)

def test_arc_with_z(tracer, builder):
    builder.move(x=10, y=0, z=0)
    tracer.select_resolution(2.0)
    tracer.arc(target=(0, 10, 5), center=(-10, 0))
    final_pos = builder.position
    assert np.isclose(final_pos.x, 0, atol=0.1)
    assert np.isclose(final_pos.y, 10, atol=0.1)
    assert np.isclose(final_pos.z, 5, atol=0.1)

def test_circle(tracer, builder):
    builder.move(x=10, y=0)
    tracer.select_resolution(2.0)
    tracer.circle(center=(-10, 0))
    final_pos = builder.position
    assert np.isclose(final_pos.x, 10, atol=0.1)
    assert np.isclose(final_pos.y, 0, atol=0.1)

def test_distance_modes(tracer, builder):
    # Test in absolute mode (default)
    builder.set_distance_mode("absolute")
    builder.set_axis_position((0, 0, 0))
    builder.move(x=10, y=0)
    tracer.select_resolution(2.0)
    tracer.arc(target=(0, 10), center=(-10, 0))
    absolute_commands = len(builder._writers[0].written_lines)
    absolute_final_pos = builder.position

    # Reset and test in relative mode
    builder._writers[0].written_lines.clear()
    builder.set_distance_mode("relative")
    builder.set_axis_position((0, 0, 0))
    builder.move(x=10, y=0)
    tracer.arc(target=(-10, 10), center=(-10, 0))
    relative_commands = len(builder._writers[0].written_lines)
    relative_final_pos = builder.position

    # Verify same number of points generated
    assert absolute_commands == relative_commands

    # Verify same final position reached
    assert np.isclose(absolute_final_pos.x, relative_final_pos.x, atol=0.1)
    assert np.isclose(absolute_final_pos.y, relative_final_pos.y, atol=0.1)

# Test resolution

def test_resolution_affects_segment_count(tracer, builder, mock_writer):
    builder.move(x=10, y=0)

    # Count moves with coarse resolution
    tracer.select_resolution(3.0)
    initial_moves = len(mock_writer.written_lines)
    tracer.arc(target=(0, 10), center=(-10, 0))
    coarse_moves = len(mock_writer.written_lines) - initial_moves

    # Reset and count moves with fine resolution
    mock_writer.written_lines.clear()
    builder.move(x=10, y=0)
    tracer.select_resolution(2.0)
    initial_moves = len(mock_writer.written_lines)
    tracer.arc(target=(0, 10), center=(-10, 0))
    fine_moves = len(mock_writer.written_lines) - initial_moves

    # Fine resolution should generate more moves
    assert fine_moves > coarse_moves

# Test error handling

def test_arc_invalid_radius(tracer):
    with pytest.raises(ValueError):
        tracer.arc(target=(10, 0), center=(0, 0))
