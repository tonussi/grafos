import Chronometer

class FloydWarshall(object):
    '''
    This class implements the function to extract the matrices
    of Routes and matrices of Adjacency from a given matrix that
    represents a Graph
    '''

    def __init__(self, MatrixGraph):
        '''
        Use @timeit in a method to get the time
        '''
        self.MatrixGraph = MatrixGraph
