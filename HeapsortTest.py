import unittest
from HeapSort import HeapSort

class GraphTest(unittest.TestCase):

    def setUp(self):
        self.heap = HeapSort()
        self.array = [8, 99, 12, 839, 12, 32, 89, 11, 99, 4, 12, 2, 13]

    def tearDown(self):
        del self.heap

    def testSortingWithHeapSort(self):
        self.heap.heapsort(self.array, len(self.array))
        print(self.array)
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
