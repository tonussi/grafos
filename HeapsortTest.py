import unittest, random
from HeapSort import HeapSort

class GraphTest(unittest.TestCase):

    def setUp(self):
        self.oddarray = [8, 99, 12, 839, 12, 32, 89, 11, 99, 4, 12, 2, 13]
        self.evenarray = [8, 99, 12, 839, 12, 32, 89, 11, 99, 4, 2, 13]

    def tearDown(self):
        del self.oddarray
        del self.evenarray

    """
    Testing against 13 random elements is passing (odd index)
    """
    def testSortingWithHeapSortOddIndex(self):
        HeapSort.heapsort(self.oddarray, len(self.oddarray))
        for i in range(1, len(self.oddarray) - 1):
            self.assertTrue(self.oddarray[i] <= self.oddarray[i + 1], 'oddarray[{}] should be leq than oddarray[{}]'.format(i, i + 1))

    """
    Testing against 12 random elements is passing (odd index)
    """
    def testSortingWithHeapSortEvenIndex(self):
        HeapSort.heapsort(self.evenarray, len(self.evenarray))
        for i in range(1, len(self.evenarray) - 1):
            self.assertTrue(self.evenarray[i] <= self.evenarray[i + 1], 'oddarray[{}] should be leq than oddarray[{}]'.format(i, i + 1))

    """
    Testing against 2kk random elements is passing
    """
    def testAgainstBigArray(self):
        bigarray = [random.random() for _ in range(2000000)]
        HeapSort.heapsort(bigarray, len(bigarray))
        for i in range(1, len(bigarray) - 1):
            self.assertTrue(bigarray[i] <= bigarray[i + 1], 'bigarray[{}]={} should be leq than bigarray[{}]={}'.format(i, bigarray[i], i + 1, bigarray[i + 1]))
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
