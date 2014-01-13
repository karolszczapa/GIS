import networkx


class GraphFile:
    def __init__(self, path = ""):
        self.path = path

    def save(self, G, pos = None):
        file_ = open(self.path, 'w')
        file_.write(str(len(G.nodes()))+"\n")

        i=0

        for node in G.nodes():
            file_.write(str(node))
            file_.write(" ")
            if pos != None:
                file_.write(str(pos[i][0]))
                file_.write(" ")
                file_.write(str(pos[i][1]))
                i+=1
            file_.write("\n")

        file_.write(str(len(G.edges()))+"\n")

        for edge in G.edges():
            file_.write(str(edge[0]))
            file_.write(" ")
            file_.write(str(edge[1]))
            file_.write("\n")
        file_.close()

    def load(self):
        file_ = open(self.path, 'r')
        nodesNumberStr = file_.readline()
        nodesNumber = int(nodesNumberStr)
        G = networkx.Graph()
        pos = []
        for n in range(nodesNumber):
            line = file_.readline()
            lineStr = str(line)
            lineStr = lineStr.replace("\n", "")
            words = lineStr.split(" ")
            nodeNumber = int(words[0])

            if len(words) == 3:
                posX = float(words[1])
                posY = float(words[2])
                pos.append([posX, posY])

            G.add_node(nodeNumber)

        edgesNumberStr = file_.readline()
        edgesNumber = int(edgesNumberStr)
        for n in range(edgesNumber):
            line = file_.readline()
            lineStr = str(line)
            lineStr = lineStr.replace("\n", "")
            words = lineStr.split(" ")
            node1 = int(words[0])
            node2 = int(words[1])
            G.add_edge(node1, node2)
        return (G, pos, nodesNumber, edgesNumber)

    def setPath(self, path):
        self.path = path

    def getPath(self):
        return self.path
