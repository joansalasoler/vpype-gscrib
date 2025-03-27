import math
import pytest
import numpy as np
from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal
from vpype_mecode.builder.transformer import Transformer
from vpype_mecode.builder.point import Point


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def transformer():
    return Transformer()

@pytest.fixture
def transformed():
    t = Transformer()
    t.translate(10, 20, 30)
    t.rotate(90)
    t.scale(2)
    return t


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

# Test initialization

def test_default_initialization():
    t = Transformer()
    assert_array_equal(t._current_matrix, np.eye(4))
    assert_array_equal(t._inverse_matrix, np.eye(4))
    assert len(t._matrix_stack) == 0

# Test matrix stack operations

def test_push_matrix(transformer):
    original = transformer._current_matrix.copy()
    transformer.push_matrix()
    transformer.translate(10, 0, 0)
    assert len(transformer._matrix_stack) == 1
    assert_array_equal(transformer._matrix_stack[0], original)

def test_pop_matrix(transformer):
    original = transformer._current_matrix.copy()
    transformer.push_matrix()
    transformer.translate(10, 0, 0)
    transformer.pop_matrix()
    assert_array_equal(transformer._current_matrix, original)
    assert len(transformer._matrix_stack) == 0

def test_pop_empty_stack(transformer):
    with pytest.raises(IndexError):
        transformer.pop_matrix()

def test_multiple_push_pop(transformer):
    transformer.push_matrix()
    transformer.translate(10, 0, 0)
    transformer.push_matrix()
    transformer.rotate(90)
    transformer.pop_matrix()
    transformer.pop_matrix()
    assert_array_equal(transformer._current_matrix, np.eye(4))

def test_context_manager(transformer):
    original = transformer._current_matrix.copy()

    with transformer as t:
        t.translate(10, 0, 0)
        point1 = t.apply_transform(Point(0, 0, 0))
        assert point1 == Point(10, 0, 0)

    point2 = t.apply_transform(Point(0, 0, 0))
    assert_array_equal(transformer._current_matrix, original)
    assert point2 == Point(0, 0, 0)

# Test basic transformations

def test_translation(transformer):
    transformer.translate(10, 20, 30)
    point = transformer.apply_transform(Point(0, 0, 0))
    assert point == Point(10, 20, 30)

def test_scale_uniform(transformer):
    transformer.scale(2)
    point = transformer.apply_transform(Point(1, 1, 1))
    assert point == Point(2, 2, 2)

def test_scale_non_uniform(transformer):
    transformer.scale(2, 3, 4)
    point = transformer.apply_transform(Point(1, 1, 1))
    assert point == Point(2, 3, 4)

def test_rotate_z_90_degrees(transformer):
    transformer.rotate(90, axis="z")
    point = transformer.apply_transform(Point(1, 0, 0))
    transformed_array = point.to_vector()[:3]
    expected_array = Point(0, 1, 0).to_vector()[:3]
    print(transformed_array)
    assert_array_almost_equal(transformed_array, expected_array)

def test_rotate_x_90_degrees(transformer):
    transformer.rotate(90, axis="x")
    point = transformer.apply_transform(Point(0, 1, 0))
    transformed_array = point.to_vector()[:3]
    expected_array = Point(0, 0, 1).to_vector()[:3]
    print(transformed_array)
    assert_array_almost_equal(transformed_array, expected_array)

def test_rotate_y_90_degrees(transformer):
    transformer.rotate(90, axis="y")
    point = transformer.apply_transform(Point(0, 0, 1))
    transformed_array = point.to_vector()[:3]
    expected_array = Point(1, 0, 0).to_vector()[:3]
    print(transformed_array)
    assert_array_almost_equal(transformed_array, expected_array)

def test_mirror_xy_plane(transformer):
    point = Point(1.0, 2.0, 3.0)
    transformer.mirror(plane="xy")
    result = transformer.apply_transform(point)
    assert result.x == pytest.approx(1.0)
    assert result.y == pytest.approx(2.0)
    assert result.z == pytest.approx(-3.0)

def test_mirror_yz_plane(transformer):
    point = Point(1.0, 2.0, 3.0)
    transformer.mirror(plane="yz")
    result = transformer.apply_transform(point)
    assert result.x == pytest.approx(-1.0)
    assert result.y == pytest.approx(2.0)
    assert result.z == pytest.approx(3.0)

def test_mirror_zx_plane(transformer):
    """Test mirroring across ZX plane."""
    point = Point(1.0, 2.0, 3.0)
    transformer.mirror(plane="zx")
    result = transformer.apply_transform(point)
    assert result.x == pytest.approx(1.0)
    assert result.y == pytest.approx(-2.0)
    assert result.z == pytest.approx(3.0)

def test_reflect_arbitrary_plane(transformer):
    point = Point(1.0, 1.0, 1.0)
    transformer.reflect([1, 1, 1])
    result = transformer.apply_transform(point)
    assert result.x == pytest.approx(-1)
    assert result.y == pytest.approx(-1)
    assert result.z == pytest.approx(-1)

# Test complex transformations

def test_combined_transformations(transformer):
    point = Point(1, 0, 0)
    transformer.translate(1, 0, 0)
    transformer.rotate(90, "z")
    transformer.scale(2)

    transformed_point = transformer.apply_transform(point)
    transformed_array = transformed_point.to_vector()[:3]
    expected_array = Point(0, 4, 0).to_vector()[:3]
    assert_array_almost_equal(transformed_array, expected_array)

def test_nested_transformations(transformer):
    point = Point(1, 0, 0)
    transformer.translate(1, 0, 0)
    transformer.push_matrix()
    transformer.rotate(90, "z")
    transformer.scale(2)
    point1 = transformer.apply_transform(point)
    transformer.pop_matrix()
    point2 = transformer.apply_transform(point)

    expected1 = Point(0, 4, 0).to_vector()[:3]
    expected2 = Point(2, 0, 0).to_vector()[:3]
    assert_array_almost_equal(point1.to_vector()[:3], expected1)
    assert_array_almost_equal(point2.to_vector()[:3], expected2)

# Test edge and special cases

def test_identity_transformation(transformer):
    point = Point(1, 2, 3)
    transformed = transformer.apply_transform(point)
    assert point == transformed

def test_multiple_rotations(transformer):
    origin = Point(1, 2, 3)
    transformer.rotate(90, "z")
    transformer.rotate(90, "z")
    transformer.rotate(90, "z")
    transformer.rotate(90, "z")
    point = transformer.apply_transform(origin)
    transformed_array = point.to_vector()[:3]
    expected_array = origin.to_vector()[:3]
    assert_array_almost_equal(transformed_array, expected_array)

def test_reverse_transform(transformer):
    transformer.scale(2)
    transformer.rotate(60)
    transformer.translate(10, 20, 30)
    original = Point(1, 2, 3)
    transformed = transformer.apply_transform(original)
    restored = transformer.reverse_transform(transformed)
    original_array = original.to_vector()[:3]
    restored_array = restored.to_vector()[:3]
    assert_array_almost_equal(original_array, restored_array)

def test_extreme_values(transformer):
    transformer.translate(1e15, 1e15, 1e15)
    transformer.scale(1e-15)
    point = transformer.apply_transform(Point(1, 1, 1))
    assert not np.any(np.isnan(point.to_vector()))

def test_double_reflection_identity(transformer):
    point = Point(1.0, 2.0, 3.0)
    transformer.reflect([0, 0, 1])
    transformer.reflect([0, 0, 1])
    result = transformer.apply_transform(point)
    assert result.x == pytest.approx(point.x)
    assert result.y == pytest.approx(point.y)
    assert result.z == pytest.approx(point.z)

def test_reflection_preserves_distances(transformer):
    p1 = Point(1.0, 2.0, 3.0)
    p2 = Point(4.0, 5.0, 6.0)

    orig_dist = np.sqrt(
        (p2.x - p1.x) ** 2 +
        (p2.y - p1.y) ** 2 +
        (p2.z - p1.z) ** 2
    )

    transformer.reflect([1, 0, 0])
    r1 = transformer.apply_transform(p1)
    r2 = transformer.apply_transform(p2)

    new_dist = np.sqrt(
        (r2.x - r1.x) ** 2 +
        (r2.y - r1.y) ** 2 +
        (r2.z - r1.z) ** 2
    )

    assert new_dist == pytest.approx(orig_dist)

# Test precision and accuracy

def test_transformation_precision():
    t = Transformer()
    small_angle = 1e-10
    t.rotate(small_angle)
    point = t.apply_transform(Point(1, 0, 0))
    assert abs(point.x - 1) < 1e-9
    assert abs(point.y) < 1e-9

def test_matrix_determinant_stability():
    t = Transformer()

    for _ in range(100):
        t.rotate(0.1)
        t.scale(0.99)

    determinant = np.linalg.det(t._current_matrix)
    assert determinant != 0  # Matrix should not become singular

# Test error handling

def test_invalid_transform_matrix():
    with pytest.raises(ValueError):
        transformer = Transformer()
        transformer.chain_transform(np.eye(3))

def test_reflect_invalid_normal(transformer):
    with pytest.raises(ValueError):
        transformer.reflect([0, 0, 0])

def test_invalid_rotation_axis(transformer):
    with pytest.raises(KeyError):
        transformer.rotate(90, axis="w")

def test_invalid_mirror_plane(transformer):
    with pytest.raises(ValueError):
        transformer.mirror("vw")

def test_invalid_scale_args(transformer):
    with pytest.raises(ValueError):
        transformer.scale(0)

    with pytest.raises(ValueError):
        transformer.scale(0, 1, 1)

    with pytest.raises(ValueError):
        transformer.scale(1, 2, 3, 4)
