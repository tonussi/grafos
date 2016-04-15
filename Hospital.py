import Floyd, Graph

class Hospital(Graph, FloydWarshall):
    """<h1>Simple Graph Class Impl of the Medical Center's problem</h1>
    <p>This class implement a Graph for the Medical Center's problem
    Its structured with basic functions and extends FloydWarshall actions.</p>"""

    def __init__(self, arg={}, name='', location=[]):
        super(Graph, self).__init__()
        self.graph = arg
        self.name = name
        self.location = location

    def name(self, name):
        self.name = name

    def location(self, name):
        pass