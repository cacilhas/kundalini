from unittest import TestCase
import math
from kundalini import Vector

__all__ = ['TestVector']


#-----------------------------------------------------------------------
class TestVector(TestCase):

    angle_345 = math.radians(53.13010235)


    def test_simple_2d_vector(self):
        vector = Vector(3, 4)
        self.assertEqual(vector, (3, 4, 0, 0))
        self.assertEqual(vector.x, 3)
        self.assertEqual(vector.y, 4)
        self.assertEqual(vector.z, 0)
        self.assertEqual(vector.w, 0)
        self.assertEqual(vector.magnitude, 5)
        self.assertAlmostEqual(vector.angles[0], self.angle_345)
        self.assertEqual(vector.angles[1:], (0, 0))


    def test_3d_vector(self):
        vector = Vector(3, 4, 4)
        self.assertEqual(vector, (3, 4, 4, 0))
        self.assertEqual(vector.x, 3)
        self.assertEqual(vector.y, 4)
        self.assertEqual(vector.z, 4)
        self.assertEqual(vector.w, 0)
        self.assertAlmostEqual(vector.magnitude, 6.4031, places=4)
        self.assertAlmostEqual(vector.angles[0], self.angle_345)
        self.assertAlmostEqual(vector.angles[1], self.angle_345)
        self.assertEqual(vector.angles[2], 0)


    def test_4d_vector(self):
        vector = Vector(3, 4, 4, 4)
        self.assertEqual(vector, (3, 4, 4, 4))
        self.assertEqual(vector.x, 3)
        self.assertEqual(vector.y, 4)
        self.assertEqual(vector.z, 4)
        self.assertEqual(vector.w, 4)
        self.assertAlmostEqual(vector.magnitude, 7.5498, places=4)
        self.assertAlmostEqual(vector.angles[0], self.angle_345)
        self.assertAlmostEqual(vector.angles[1], self.angle_345)
        self.assertAlmostEqual(vector.angles[2], self.angle_345)


    def test_abs(self):
        vector = abs(Vector(1, -2, 3))
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (1, 2, 3, 0))


    def test_neg(self):
        vector = -Vector(1, -2, 3)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (-1, 2, -3, 0))


    def test_pos(self):
        vector = +Vector(1, -2, 3)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (1, -2, 3, 0))


    def test_add(self):
        vector = Vector(1, 2, 3) + Vector(4, 5, 6)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (5, 7, 9, 0))


    def test_sub(self):
        vector = Vector(4, 2, 5) - Vector(1, 5, 0)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (3, -3, 5, 0))


    def test_mul(self):
        vector = Vector(1, -2, 3) * 2
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (2, -4, 6, 0))


    def test_rmul(self):
        vector = 2 * Vector(1, -2, 3)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (2, -4, 6, 0))


    def test_truediv(self):
        vector = Vector(4, -2, 3) / 2
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (2, -1, 1.5, 0))


    def test_rtruediv(self):
        vector = 1 / Vector(4, -2, 8)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (.25, -.5, .125, 0))


    def test_floordiv(self):
        vector = Vector(4, -2, 3) // 2
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (2, -1, 1, 0))


    def test_mod(self):
        vector = Vector(13, -3, 26) % 5
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (3, 2, 1, 0))


    def _test_divmod(self):
        vector, rest = divmod(Vector(13, -3, 26), 5)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (2, -1, 5, 0))
        self.assertTrue(isinstance(rest, Vector))
        self.assertEqual(vector, (3, 2, 1, 0))


    def test_pow(self):
        vector = Vector(4, -2, 3) ** 2
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (16, 4, 9, 0))


    def test_lshift(self):
        vector = Vector(4, -2, 3) << 1
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (8, -4, 6, 0))


    def test_rshift(self):
        vector = Vector(4, -2, 3) >> 1
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (2, -1, 1, 0))


    def test_and_1(self):
        vector = Vector(15, 33) & Vector(8, 32, 1)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (8, 32, 0, 0))


    def test_and_2(self):
        vector = Vector(15, 33) & 8
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (8, 0, 0, 0))


    def test_rand(self):
        vector = 8 & Vector(15, 33)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (8, 0, 0, 0))


    def test_or_1(self):
        vector = Vector(15, 33) | Vector(8, 32, 1)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (15, 33, 1, 0))


    def test_or_2(self):
        vector = Vector(15, 33) | 8
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (15, 41, 0, 0))


    def test_ror(self):
        vector = 8 | Vector(15, 33)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (15, 41, 0, 0))


    def test_xor_1(self):
        vector = Vector(15, 33) ^ Vector(8, 32, 1)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (7, 1, 1, 0))


    def test_xor_2(self):
        vector = Vector(15, 33) ^ 8
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (7, 41, 0, 0))


    def test_rxor(self):
        vector = 8 ^ Vector(15, 33)
        self.assertTrue(isinstance(vector, Vector))
        self.assertEqual(vector, (7, 41, 0, 0))
