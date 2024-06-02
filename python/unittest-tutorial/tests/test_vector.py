import sys
import unittest

from vector import Vector


class TestVector(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("Setting up class")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Tearing down class")

    def setUp(self) -> None:
        print("Setting up")

    def tearDown(self) -> None:
        print("Tearing down")

    @unittest.skipIf(sys.platform == "win32", "Skip on Windows")
    def test_add(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        self.assertEqual(v1 + v2, Vector(4, 6))
        with self.assertRaises(AttributeError):
            v1 + 1

        with self.assertRaises(ValueError):
            Vector(1, "2")

    @unittest.skipIf(sys.version_info < (3, 12), "Only support Python 3.12+")
    def test_sub(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        self.assertEqual(v1 - v2, Vector(-2, -2))

    def test_mul(self):
        v1 = Vector(1, 2)
        self.assertEqual(v1 * 3, Vector(3, 6))

    def test_div(self):
        v1 = Vector(1, 2)
        self.assertEqual(v1 / 2, Vector(0.5, 1))

    def test_eq(self):
        v1 = Vector(1, 2)
        v2 = Vector(1, 2)
        self.assertEqual(v1, v2)

    def test_str(self):
        v1 = Vector(1, 2)
        self.assertEqual(str(v1), "(1, 2)")
