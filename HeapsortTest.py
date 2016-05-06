import unittest
from Heapsort import Heapsort

class GraphTest(unittest.TestCase):

    def setUp(self):
        self.heap = Heapsort()

    def tearDown(self):
        del self.heap

    def testSortingWithHeapSort(self):
        pass
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
