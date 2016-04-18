from FloydWarshall import FloydWarshall
from Graph import Graph

class Hospital(Graph, FloydWarshall):
    """<h1>Simple Graph Class Impl of the Medical Center's problem</h1>
    <p>This class implement a Graph for the Medical Center's problem
    Its structured with basic functions and extends FloydWarshall actions.</p>"""

    def __init__(self, arg={}, name='', location=[]):
        self.graph = arg
        self.name = name
        self.location = location
        self.rotas = 1

    def name(self, name):
        self.name = name

    def location(self, name):
        pass

    def rotas(self):
        return self.rotas
