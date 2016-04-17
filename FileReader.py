import os, sys
from blinker._utilities import text

class FileReader(object):

    @staticmethod
    def listGraphsInDirectory(path):
        return [os.path.join(path,fn) for fn in next(os.walk(path))[2]]

    @staticmethod
    def readFile(path):
        """
        <code>with</code> is recommended to open files
        this method open a file to get a edges-dict inside it
        """
        edges = {}
        try:
            with open(path, 'r') as inf:
                edges = eval(inf.read())
        except IOError:
            raise Exception("it was impossible to open the given file")
            sys.exit()
        inf.close()
        return edges

    @staticmethod
    def writef(fileName='dat' + os.path.sep + 'result.dat', results=''):
        try:
            file = open(fileName, 'w')
        except IOError:
            raise Exception('Erro ao tentar escrever no arquivo(s) em: {}'.format(fileName))
            sys.exit()

        file.write(str(results))
        file.close()
