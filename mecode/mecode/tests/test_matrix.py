#! /usr/bin/env python

from os.path import abspath, dirname, join
import unittest
import sys
import math

HERE = dirname(abspath(__file__))

try:
    from mecode import GMatrix
except:
    sys.path.append(abspath(join(HERE, '..', '..')))
    from mecode import GMatrix

from test_main import TestGFixture

class TestGMatrix(TestGFixture):

    def getGClass(self):
        return GMatrix

    def test_matrix_push_pop(self):
        # See if we can rotate our rectangel drawing by 90 degrees.
        self.g.push_matrix()
        self.g.rotate(math.pi/2)
        self.g.rapid(z=5)
        self.g.rect(10, 5)
        self.expect_cmd("""
        G0 Z5
        G1 X-5 Y0
        G1 X0 Y10
        G1 X5 Y-0
        G1 X-0 Y-10
        """)
        self.g.pop_matrix()
        self.assert_output()
        self.assert_almost_position({'x':0, 'y':0, 'z':5})

        # This makes sure that the pop matrix worked.
        self.g.rapid(z=5)
        self.g.rect(10, 5)
        self.expect_cmd("""
        G0 Z5
        G1 X0 Y5
        G1 X10 Y0
        G1 X0 Y-5
        G1 X-10 Y0
        """)
        self.assert_output()
        self.assert_position({'x': 0, 'y': 0, 'z': 10})

    def test_multiple_matrix_operations(self):
        # See if we can rotate our rectangle drawing by 90 degrees, but
        # get to 90 degrees by rotating twice.
        self.g.push_matrix()
        self.g.rotate(math.pi/4)
        self.g.rotate(math.pi/4)
        self.g.rapid(z=5)
        self.g.rect(10, 5)
        self.expect_cmd("""
        G0 Z5
        G1 X-5 Y0
        G1 X0 Y10
        G1 X5 Y-0
        G1 X-0 Y-10
        """)
        self.g.pop_matrix()
        self.assert_output()
        self.assert_almost_position({'x': 0, 'y': 0, 'z': 5})

    def test_matrix_scale(self):
        self.g.push_matrix()
        self.g.scale(2)
        self.g.rapid(z=5)
        self.g.rect(10, 5)
        self.expect_cmd("""
        G0 Z10
        G1 X0 Y10
        G1 X20 Y0
        G1 X0 Y-10
        G1 X-20 Y0
        """)
        self.g.pop_matrix()
        self.assert_output()

    def test_abs_move_and_rotate(self):
        self.g.rapid(z=5)
        self.g._abs_move(x=5.0)
        self.assert_almost_position({'x' : 5.0, 'y':0, 'z':5})
        self.g.rapid(z=5)
        self.g.rotate(math.pi)
        self.assert_almost_position({'x' : -5.0, 'y':0, 'z':10})

    def test_abs_zmove_with_flip(self):
        self.g.rapid(z=5)
        self.g.rotate(math.pi)
        self.g._abs_move(x=1)
        self.assert_almost_position({'x': 1.0, 'y': 0, 'z': 5})
        self.g._abs_move(z=2)
        self.assert_almost_position({'x': 1.0, 'y': 0, 'z': 2})

        self.expect_cmd("""
        G0 Z5
        G90 ; absolute
        G1 X-1 Y0 Z5
        G91 ; relative
        G90 ; absolute
        G1 X-1 Y0 Z2
        G91 ; relative
        """)
        self.assert_output()

    def test_abs_zmove_with_rotate(self):
        self.g.rapid(z=5)
        self.g.rotate(math.pi/2.0)
        self.g._abs_move(x=1)
        self.assert_almost_position({'x': 1.0, 'y': 0, 'z': 5})
        self.g._abs_move(z=2)
        self.assert_almost_position({'x': 1.0, 'y': 0, 'z': 2})
        self.expect_cmd("""
        G0 Z5
        G90 ; absolute
        G1 X0 Y1 Z5
        G91 ; relative
        G90 ; absolute
        G1 X0 Y1 Z2
        G91 ; relative
        """)
        self.assert_output()

    def test_scale_and_abs_move(self):
        self.g.rapid(z=5)
        self.g._abs_move(x=1)
        self.g.scale(2.0)
        self.assert_almost_position({'x': .5, 'y': 0, 'z': 2.5})
        self.g._abs_move()
        self.assert_almost_position({'x': .5, 'y': 0, 'z': 2.5})
        self.g._abs_move(z=3)
        self.assert_almost_position({'x': .5, 'y': 0, 'z': 3})

    def test_arc(self):
        self.g.rapid(z=5)
        self.g.rotate(math.pi/2)
        self.g.arc(x=10, y=0, linearize=False)
        self.expect_cmd("""
        G0 Z5
        G17 ; XY plane
        G2 X0 Y10 R5
        """)
        self.assert_output()
        self.assert_almost_position({'x': 10, 'y': 0, 'z': 5})

    def test_arc_reflect(self):
        self.g.rapid(z=5)
        self.g.reflect(0.0)
        self.g.arc(x=10,y=0)
        # Without the reflect this would be a G2.
        self.expect_cmd("""
        G0 Z5
        G17 ; XY plane
        G3 X10 Y0 R5
        """)
        self.assert_output()
        self.assert_almost_position({'x': 10, 'y': 0, 'z': 5})

    def test_arc_scale(self):
        self.g.scale(2.0)
        self.g.rapid(z=5)
        self.g.rotate(math.pi/2)
        self.g.arc(x=10, y=0, linearize=False)
        self.expect_cmd("""
        G0 Z10
        G17 ; XY plane
        G2 X0 Y20 R10
        """)
        self.assert_output()
        self.assert_almost_position({'x': 10, 'y': 0, 'z': 5})

    def test_current_position(self):
        self.g.push_matrix()
        self.g.move(5, 0)
        self.assert_almost_position({'x':5, 'y':0, 'z':0})
        self.g.move(-5, 0)
        self.assert_almost_position({'x':0, 'y':0, 'z':0})
        self.g.rotate(math.pi/4)
        self.g.move(1, 0)
        self.assert_almost_position({'x':1, 'y':0, 'z':0})
        self.assertAlmostEqual(math.cos(math.pi/4), self.g._current_position['x'])
        self.assertAlmostEqual(math.cos(math.pi/4), self.g._current_position['y'])
        self.g.move(-1, 0)
        self.g.pop_matrix()
        self.assert_almost_position({'x':0, 'y':0, 'z':0})
        self.g.move(0,0,-1)
        self.assert_almost_position({'x':0, 'y':0, 'z':-1})

    def test_matrix_math(self):
        self.assertAlmostEqual(self.g._matrix_transform_length(2), 2.0)
        self.g.rotate(math.pi/3)
        self.assertAlmostEqual(self.g._matrix_transform_length(2), 2.0)
        self.g.scale(2.0)
        self.assertAlmostEqual(self.g._matrix_transform_length(2), 4.0)
        self.g.scale(.25)
        self.assertAlmostEqual(self.g._matrix_transform_length(2), 1.0)

    def test_reflect(self):
        self.g.push_matrix()
        self.g.rapid(z=5)
        self.g.move(10,20)
        self.g.reflect(0)
        self.g.move(10,20)
        self.g.reflect(math.pi/2)
        self.g.move(10,20)
        self.g.reflect(0)
        self.g.reflect(math.pi/2)
        self.g.move(10,20)
        self.expect_cmd("""
        G0 Z5
        G1 X10 Y20
        G1 X10 Y-20
        G1 X-10 Y-20
        G1 X10 Y20
        """)
        self.g.pop_matrix()
        self.assert_output()

    def test_rotate_and_reflect(self):
        self.g.rapid(z=5)
        self.g.move(10, 0)
        self.g.push_matrix()
        self.g.rotate(math.pi/2)
        self.g.move(10, 0)
        self.g.reflect(math.pi/2)
        self.g.move(10, 0)
        self.expect_cmd("""
        G0 Z5
        G1 X10 Y0
        G1 X0 Y10
        G1 X-0 Y-10
        """)
        self.g.pop_matrix()
        self.assert_output()

if __name__ == '__main__':
    unittest.main()
