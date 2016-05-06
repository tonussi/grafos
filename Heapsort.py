class Heapsort:

    """
    This is a function to sort the elements
    using a Heap tree logic. Heap sort have
    two main stages. In the first stage, the
    array is transformed into a heap (binary tree).

    Binary Tree Definition:
        1) Each node is greater than each of its children
        2) The tree is completly balanced
        3) All leaves are in the leftmost position available

    In the second stage the heap is continuously reduced
    to a sorted array like this:

        1) While the heap binary tree is not empty
            1.1) Remove the top of the head into an array
            1.2) Fix the heap ('ajuste')

    Heapsort was invented by J. W. J. Williams in 1964 [1]

    [1] Williams, J. W. J. (1964), "Algorithm 232 - Heapsort",
        Communications of the ACM 7 (6): 347–348, doi:10.1145/512274.512284

    MoveDown:
    The movedown method checks and verifies that the structure is a heap.

    @param a: array of elements to be sorted
    @param n: length of the array a
    """
    def heapsort(self, a, n):
        i = 0
        temp = 0
        for i in range(1, n // 2):
            self.ajuste(a, i, n)
        for i in range(1, n - 1):
            temp = a[i + 1]
            a[i + 1] = a[1]
            a[1] = temp
            self.ajuste(a, 1, i)

    """
    This is a method to adjust the elements of
    a partition (subset of A)

    @param a: a partition of the original array of elements
    @param i: the index point of the partition
    @param n: the size of the original array of elements
    """
    def ajuste(self, a, i, n):
        # j = 0
        # aAux = 0

        aAux = a[i]
        j = 2 * i

        while (j <= n):
            if j < n and a[j] < a[j + 1]:
                j = j + 1
            if aAux >= a[j]:
                return
            a[j // 2] = a[j]
            a[j] = aAux
            j = 2 * j
            a[j // 2] = aAux
