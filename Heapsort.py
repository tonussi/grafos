class Heapsort:

    """
    This is a function to sort the elements
    using a Heap tree logic

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
