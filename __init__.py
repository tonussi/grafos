# encoding:utf-8

from Graph import Graph
from FileReader import FileReader
from Hospital import Hospital
from RandomGraphGenerator import RandomGraphGenerator
from FloydWarshall import FloydWarshall

import sys
import getopt
import os
import threading
import random

"""
You can choose -e or --export to build the dat directory
this will populate the dat directory with graphs
You also can start the calculation of a graph at time
just input in your terminal the following line:
python __init__.py -i dat/<name_of_file>
and them fo to the /results directory at the root of this
software package to pick up your results.
note: this program already build regular graphs with random
costs, and this program also makes use of an good algorithm to
to build random regular graphs, see RandomGraphGenerator.py for
more information. Another thing to account is that the program
divide the efforts to find the best path into to running threads.
each thread called Samu Slave will calculate the best path for the
ambulance to arrive at his Medical Center. What I mean is that a
ambulance A is related to medical center A and not to medical center B
wich is related to ambulance B.\n"
"""


class SamuSlave(threading.Thread):

    def __init__(self, hospital, threadID, name, routes):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.routes = routes
        self.hospital = hospital

    def run(self):
        threadLock.acquire()
        self.hospital.findBestWayToMedicalCenterRoute()
        threadLock.release()

threadLock = threading.Lock()
threads = []


def exportnewRegularGraphsToDat(edgesArray=[10, 20, 50, 100, 500]):
    """
    This function exports to files 5 or more regular graph without crossing edges
    or also parallel edges.

    There will be files in dat directory with at least the number of nodes passed
    as parameter divided by 2 in edges.
    """
    graph_generator = RandomGraphGenerator()

    for i in edgesArray:
        set_of_edges = graph_generator.random_regular_graph(1, i)
        dict_of_edges = graph_generator.convertSetToOrderedDict(set_of_edges)
        FileReader.writef(
            'dat' +
            os.path.sep +
            'results_' +
            str(i) +
            '_nodes' +
            '.dat',
            'edges=' +
            str(dict_of_edges))

def getDatDirectory():
    return FileReader.listGraphsInDirectory('dat')


def startThreadings():
    hospitalA = Hospital()
    hospitalB = Hospital()

    # Create new threads
    thread1 = SamuSlave(hospitalA, 0x1, "Operador Samu 1", [1, 2, 3])
    thread2 = SamuSlave(hospitalB, 0x2, "Operador Samu 2", [3, 2, 1])

    # Start new Threads
    thread1.start()
    thread2.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)

    # Wait for all threads to complete
    for t in threads:
        t.join()


def main(argv):
    edges = {}

    try:
        opts, args = getopt.getopt(argv, "h|i|e")
    except getopt.GetoptError:
        print("(1) python __init__.py -i <DAT_FILE_INPUT> (find best path)")
        print("(2) python __init__.py -e (export)")
        print("(3) python __init__.py -h (help)")
        raise Warning("warning: did you forget parameters?")
    for opt, arg in opts:
        if opt == '-help':
            print(
                "(1) python __init__.py -i <DAT_FILE_INPUT> (find best path)")
            print("(2) python __init__.py -e (export)")
            print("(3) python __init__.py -h (help)")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            print(args)
            if os.path.exists(args[0]):
                edges = FileReader.readFile(args[0])
                print(edges)
        elif opt in ("-e", "--export"):
            if not os.path.exists('dat'):
                try:
                    os.makedirs('dat')
                except IOError:
                    raise Exception("it was impossible to create the given directory name")

            exportnewRegularGraphsToDat()
            print('visit dat directory to see your graphs')

            if not os.path.exists('results'):
                try:
                    os.makedirs('results')
                except IOError:
                    raise Exception("it was impossible to create the given directory name")

if __name__ == '__main__':
    main(sys.argv[1:])
