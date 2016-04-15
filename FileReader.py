import os
from blinker._utilities import text

class FileReader(object):

    @staticmethod
    def listGraphsInDirectory(path):
        return [os.path.join(path,fn) for fn in next(os.walk(path))[2]]

    @staticmethod
    def readFile(path):
        results = dict()
        try:
            file = open(path)
            text = file.read()
            exec text
            results = arestas
        except IOError:
            raise Exception('Excessao na hora da leitura')
            sys.exit()
        file.close()
        return results

    @staticmethod
    def writef(fileName, results):
        try:
            file = open(fileName, 'w')
        except IOError:
            raise Exception('Erro ao tentar escrever no arquivo(s) em: {}'.format(fileName))
            sys.exit()

        file.write(str(results))
        file.close()
