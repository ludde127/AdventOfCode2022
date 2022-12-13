import unittest
from day13.main import compare_pair,run_over_data,top_level_compare
from utils import readfile


class Day13(unittest.TestCase):
    def test_run_example(self):
        example = readfile("input.txt")
        expected = [True, True, False, True, False, True, False, False]
        self.assertEqual(expected, list(run_over_data(example)))

    def test_custom(self):
        self.assertFalse(top_level_compare(str(17), str(9)))
        self.assertTrue(top_level_compare(str(17), str(98)))
        self.assertTrue(top_level_compare(str(17), str([98])))
        self.assertTrue(top_level_compare(str([17]), str([98])))
        self.assertTrue(top_level_compare(str([2, 3, 4]), str([4])))
        self.assertTrue(top_level_compare(str([2, 3, 5]), str([4])))
        self.assertFalse(top_level_compare(str([5, 3, 5]), str([4])))
        self.assertTrue(top_level_compare("5", "5"))
        self.assertTrue(top_level_compare("[[4,4],4,4]", "[[4,4],4,4,4]"))
        self.assertFalse(top_level_compare("[7,7,7,7]", "[7,7,7]"))

    def test_hugo_bs(self):
        self.assertTrue(top_level_compare("[[4,[],7],[]]", "[[[4,5],[[5,1],4,[],0,[9,9]],2,7,3]]"))

    def test_hugo2(self):
        self.assertTrue(top_level_compare("[[],[9,4]]", "[[],[[5,4,1],7],[[],4],[],[3,1,[[1],3,4,2]]]"))

if __name__ == '__main__':
    unittest.main()
