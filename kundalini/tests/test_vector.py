from unittest import TestCase
from numpy import array
from kundalini import Vector

__all__ = ['TestVector']


#-----------------------------------------------------------------------
class TestVector(TestCase):

    angle_345 = 53.13010235


    def test_simple_2d_vector(self):
        vector = Vector([3, 4])
        self.assertTrue((vector == array([3, 4])).all())
        self.assertEqual(vector.x, 3)
        self.assertEqual(vector.y, 4)
        self.assertEqual(vector.magnitude, 5)
        self.assertAlmostEqual(vector.angle_xy, self.angle_345)


    def test_simple_2d_from_angle(self):
        vector = Vector.from_angles((self.angle_345, ), magnitude=5)
        self.assertAlmostEqual(vector.x, 3, places=4)
        self.assertAlmostEqual(vector.y, 4, places=4)


    def test_3d_vector(self):
        vector = Vector([3, 4, 4])
        self.assertTrue((vector == array([3, 4, 4])).all())
        self.assertEqual(vector.x, 3)
        self.assertEqual(vector.y, 4)
        self.assertEqual(vector.z, 4)
        self.assertAlmostEqual(vector.magnitude, 6.4031, places=4)
        self.assertAlmostEqual(vector.angle_xy, self.angle_345)
        self.assertAlmostEqual(vector.angle_xz, self.angle_345)


    def test_3d_from_angle(self):
        angle_345 = self.angle_345
        vector = Vector.from_angles((angle_345, angle_345), magnitude=6.4031)
        self.assertAlmostEqual(vector.x, 3, places=4)
        self.assertAlmostEqual(vector.y, 4, places=4)
        self.assertAlmostEqual(vector.z, 4, places=4)


    def test_4d_vector(self):
        vector = Vector([3, 4, 4, 4])
        self.assertTrue((vector == array([3, 4, 4, 4])).all())
        self.assertEqual(vector.x, 3)
        self.assertEqual(vector.y, 4)
        self.assertEqual(vector.z, 4)
        self.assertEqual(vector.w, 4)
        self.assertAlmostEqual(vector.magnitude, 7.5498, places=4)
        self.assertAlmostEqual(vector.angle_xy, self.angle_345)
        self.assertAlmostEqual(vector.angle_xz, self.angle_345)
        self.assertAlmostEqual(vector.angle_xw, self.angle_345)


    def test_4d_from_angle(self):
        angle_345 = self.angle_345
        vector = Vector.from_angles((angle_345, angle_345, angle_345), magnitude=7.5498)
        self.assertAlmostEqual(vector.x, 3, places=4)
        self.assertAlmostEqual(vector.y, 4, places=4)
        self.assertAlmostEqual(vector.z, 4, places=4)
        self.assertAlmostEqual(vector.w, 4, places=4)


    def test_abs(self):
        vector = abs(Vector([1, -2, 3]))
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([1, 2, 3])).all())


    def test_neg(self):
        vector = -Vector([1, -2, 3])
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([-1, 2, -3])).all())


    def test_add(self):
        vector = Vector([1, 2, 3]) + Vector([4, 5, 6])
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([5, 7, 9])).all())


    def test_sub(self):
        vector = Vector([4, 2, 5]) - Vector([1, 5, 0])
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([3, -3, 5])).all())


    def test_mul(self):
        vector = Vector([1, -2, 3]) * 2
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([2, -4, 6])).all())


    def test_rmul(self):
        vector = 2 * Vector([1, -2, 3])
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([2, -4, 6])).all())


    def test_truediv(self):
        vector = Vector([4, -2, 3]) / 2
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([2, -1, 1.5])).all())


    def test_rtruediv(self):
        vector = 1 / Vector([4, -2, 8])
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([.25, -.5, .125])).all())


    def test_floordiv(self):
        vector = Vector([4, -2, 3]) // 2
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([2, -1, 1])).all())


    def test_mod(self):
        vector = Vector([13, -3, 26]) % 5
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([3, 2, 1])).all())


    def _test_divmod(self):
        vector, rest = divmod(Vector([13, -3, 26]), 5)
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([1, -1, 5])).all())
        self.assertTrue(isinstance(rest, Vector))
        self.assertTrue((vector == array([3, 2, 1])).all())


    def test_pow(self):
        vector = Vector([4, -2, 3]) ** 2
        self.assertTrue(isinstance(vector, Vector))
        self.assertTrue((vector == array([16, 4, 9])).all())
