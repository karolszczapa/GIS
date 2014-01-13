#import networkx
import sys
import os
import os.path
from Generator import Generator
from GraphFile import GraphFile
import networkx
import timeit

#import matplotlib.pyplot as plt
#from matplotlib.backend_bases import NavigationToolbar2
from GraphGui import GraphGui
from PyQt4.QtGui import QApplication
from Euler import Euler


def visualize_graph(G=None, pos=None):
    app = QApplication(sys.argv)
    window = GraphGui(G, pos)
    window.show()
    sys.exit(app.exec_())


def visualize_graph_():
    app = QApplication(sys.argv)
    window = GraphGui()
    window.show()
    sys.exit(app.exec_())


def mainVisual():
    visualize_graph()
def avg(table):
    return sum(times[0:])/len(times)

if __name__ == "__main__":
    #main()
    for s in sys.argv:

        if s == "-g":
            visualize_graph()

        elif s == "-c":
            countIndex =  sys.argv.index("-c")
            graphCount = int(sys.argv[countIndex+1])

            dIndex = sys.argv.index("-d")
            directory = sys.argv[dIndex+1]

            nodeIndex = sys.argv.index("-n")
            nodeCount = int(sys.argv[nodeIndex + 1])

            edgeIndex = sys.argv.index("-e")
            edgeCount = int(sys.argv[edgeIndex + 1])

            if os.path.exists(directory) is False:
                os.mkdir(directory)

            generator = Generator()
            graphFile = GraphFile()
            for i in range(graphCount):
                path = directory + "/graph" + str(i) + ".txt"
                graphFile.setPath(path)
                G = Generator().generate_half_euler_graph(5,6)
                graphFile.save(G)

        elif s == "-t":
            countIndex =  sys.argv.index("-t")
            graphCount = int(sys.argv[countIndex+1])

            dIndex = sys.argv.index("-d")
            directory = sys.argv[dIndex+1]

            nodeIndex = sys.argv.index("-n")
            nodeCount = sys.argv[nodeIndex + 1]

            edgeIndex = sys.argv.index("-e")
            edgeCount = sys.argv[edgeIndex + 1]

            t = timeit.Timer("Generator().generate_half_euler_graph("+nodeCount+","+edgeCount+")",
                            "from Generator import Generator")
            times = t.repeat(5,10)
            print avg(times)

        elif s == "-i":
            dFile = sys.argv.index("-i")
            fileTemp = sys.argv[dFile+1]
            graphFile = GraphFile(fileTemp)
            (G, pos, nodesNumber, edgesNumber) = graphFile.load()
            euler = Euler()
            (info,odds) = euler.checkGraph(G)
            print info
            print "Edges: "+str(nodesNumber)
            print "Nodes: "+str(edgesNumber)

        elif s == "-e":
            dFile = sys.argv.index("-e")
            fileTemp = sys.argv[dFile+1]
            graphFile = GraphFile(fileTemp)
            (G, pos, nodesNumber, edgesNumber) = graphFile.load()
            euler = Euler()
            path = euler.start(G)
            print path

        elif s == "-et":
            t = timeit.Timer("euler.start(G)",
            "from GraphFile import GraphFile\n"+
            "from Euler import Euler\n"+
            "import sys\n"+
            "dFile = sys.argv.index(\"-et\")\n"+
            "fileTemp = sys.argv[dFile+1]\n"+
            "graphFile = GraphFile(fileTemp)\n"+
            "(G, pos, nodesNumber, edgesNumber) = graphFile.load()\n"+
            "euler = Euler()\n"
            )
            times = t.repeat(100,10)
            print avg(times)


        elif s == "-if":
            dFile = sys.argv.index("-if")
            fileTemp = sys.argv[dFile+1]
            graphFile = GraphFile(fileTemp)
            (G, pos, nodesNumber, edgesNumber) = graphFile.load()
            euler = Euler()
            (info,odds) = euler.checkGraph(G)
            print info
            print "Edges: "+str(nodesNumber)
            print G.edges()
            print "Nodes: "+str(edgesNumber)
            print G.nodes()
