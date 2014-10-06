from unittest import TestCase, skip
from kundalini import Vector
from kundalini.matrix import Matrix

__all__ = ['TestMatrix']


#-----------------------------------------------------------------------
class TestMatrix(TestCase):

    def test_default_matrix(self):
        m = Matrix()
        self.assertTrue((
            m == [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        ).all())


    def test_explicit_matrix(self):
        m = Matrix([[1, 0], [1, 1]])
        self.assertTrue((m == [[1, 0], [1, 1]]).all())


    def test_transform(self):
        v = Vector([3, 4, 5])
        m = Matrix()
        r = m.transform(v)
        self.assertTrue((r == v).all())


    @skip('TODO')
    def test_make_translation(self):
        pass


    @skip('TODO')
    def test_make_xyz_rotate(self):
        pass
