import unittest

def inc(x):
    return x + 1

class MyTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        self.assertEqual(inc(3), 4)

    def test_answer(self):
        pass

if __name__ == '__main__':
    unittest.main()
