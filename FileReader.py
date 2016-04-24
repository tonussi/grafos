import os, sys
from blinker._utilities import text

class FileReader(object):

    @staticmethod
    def listFilesInDirectory(path):
        return [os.path.join(path,fn) for fn in next(os.walk(path))[2]]

    @staticmethod
    def readFile(path):
        """
        <code>with</code> is recommended to open files
        this method open a file to get a edges-dict inside it
        """
        arestas = []
        try:
            with open(path, 'r') as inf:
                exec inf
        except IOError:
            raise Exception("it was impossible to open the given file")
            sys.exit()
        inf.close()
        return arestas

    @staticmethod
    def readFiles(path='dat'):
        """
        this method open a file to get data inside it
        """
        files = []
        for file in FileReader.listFilesInDirectory(path):
            files.append(FileReader.readFile(file))
        return len(files), files

    @staticmethod
    def writef(fileName, results):
        try:
            file = open(fileName, 'w')
        except IOError:
            raise Exception('Erro ao tentar escrever no arquivo(s) em: {}'.format(fileName))
            sys.exit()

        file.write(results)
        file.close()
