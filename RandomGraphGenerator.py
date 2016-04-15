import os, random, time
from collections import defaultdict
from Graph import Graph
from Chronometer import timeit

class RandomGraphGenerator(object):
    
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        else:
            random.seed('8has&Has%5sa654')

    def random_regular_graph(self, d, n, seed=None):
        """Returns a random `d`-regular graph on `n` nodes.
    
        The resulting graph has no self-loops or parallel edges.
    
        Parameters
        ----------
        d : int
          The degree of each node.
        n : integer
          The number of nodes. The value of :math:`n * d` must be even.
        seed : hashable object
            The seed for random number generator.
    
        Notes
        -----
        The nodes are numbered from `0` to `n - 1`.
    
        Kim and Vu's paper [2]_ shows that this algorithm samples in an
        asymptotically uniform way from the space of random graphs when
        `d = O(n^{1 / 3 - \epsilon})`.
    
        Raises
        ------
    
        Warning:
            If :math:`n * d` is odd or `d` is greater than or equal to `n`.
    
        References
        ----------
        .. [1] A. Steger and N. Wormald,
           Generating random regular graphs quickly,
           Probability and Computing 8 (1999), 377-396, 1999.
           http://citeseer.ist.psu.edu/steger99generating.html
    
        .. [2] Jeong Han Kim and Van H. Vu,
           Generating random regular graphs,
           Proceedings of the thirty-fifth ACM symposium on Theory of computing,
           San Diego, CA, USA, pp 213--222, 2003.
           http://portal.acm.org/citation.cfm?id=780542.780576
        """
        if (n * d) % 2 != 0:
            raise Warning("n * d must be even")

        if not 0 <= d < n:
            raise Warning("the 0 <= d < n inequality must be satisfied")

        if d == 0:
            return

        def _suitable(edges, potential_edges):
        # Helper subroutine to check if there are suitable edges remaining
        # If False, the generation of the graph has failed
            if not potential_edges:
                return True
            for s1 in potential_edges:
                for s2 in potential_edges:
                    # Two iterators on the same dictionary are guaranteed
                    # to visit it in the same order if there are no
                    # intervening modifications.
                    if s1 == s2:
                        # Only need to consider s1-s2 pair one time
                        break
                    if s1 > s2:
                        s1, s2 = s2, s1
                    if (s1, s2) not in edges:
                        return True
            return False
    
        def _try_creation():
            # Attempt to create an edge set
    
            edges = set()
            stubs = list(range(n)) * d
    
            while stubs:
                potential_edges = defaultdict(lambda: 0)
                random.shuffle(stubs)
                stubiter = iter(stubs)
                for s1, s2, s3 in zip(stubiter, stubiter, stubiter):
                    if s1 > s2:
                        s1, s2 = s2, s1
                    if s1 != s2 and ((s1, s2, s3) not in edges):

                        # adiciona um vertice com custo aleatorio
                        edges.add((s1, s2, s3 << random.randint(7, 11)))

                    else:
                        potential_edges[s1] += 1
                        potential_edges[s2] += 1
    
                if not _suitable(edges, potential_edges):
                    return None # failed to find suitable edge set
    
                stubs = [node for node, potential in potential_edges.items()
                         for _ in range(potential)]
            return edges

        # Even though a suitable edge set exists,
        # the generation of such a set is not guaranteed.
        # Try repeatedly to find one.
        edges = _try_creation()
        while edges is None:
            edges = _try_creation()
        return edges

    @timeit
    def convertSetToDict(self, set):
        temp = {}
        for i in range(len(set)):
            v1, v2, cost = set.pop()
            temp['v{}'.format(i)] = [v1, v2, cost]
        return temp
