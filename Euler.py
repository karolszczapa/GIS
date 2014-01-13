import networkx
import sys


class Euler:
    NON_COMPACT = 'NOT_COMPACT'
    FULL = 'FULL'
    HALF = 'HALF'
    NONE = 'NONE'

    def start(self, G):
        (parity, odds) = self.checkGraph(G)

        if parity != self.HALF and parity != self.FULL:
            return

        H = G.copy()

        euler_path = []
        start_node = None

        if parity == self.HALF:
            start_node = odds[0]
        elif parity == self.FULL:
            start_node = H.nodes()[0]

        euler_path.append(start_node)

        neighbors = networkx.all_neighbors(H, start_node)
        last_node = start_node
        i = 1000

        while H.number_of_edges() > 0 and i > 0:
            bridges = self.find_bridges(H)
            chosenNode = None
            neighbors = networkx.all_neighbors(H, last_node)
            wasNonBridge = False

            for node in neighbors:
                isBridge = self.isBridge(last_node, node, bridges)
                if isBridge is False:
                    chosenNode = node
                    wasNonBridge = True
                    break

            if wasNonBridge is False:
                neighbors = networkx.all_neighbors(H, last_node)
                first = None
                for node in neighbors:
                    first = node
                    break
                chosenNode = first

            euler_path.append(chosenNode)
            H.remove_edge(last_node, chosenNode)

            if H.degree(last_node) == 0:
                H.remove_node(last_node)

            last_node = chosenNode
            i -= 1
        return euler_path

    def checkGraph(self, G):
        odds = None
        compact = self.isCompact(G)
        if compact is False:
            return self.NON_COMPACT

        parity, odds = self.checkParity(G)
        return (parity, odds)

    def isBridge(self, node1, node2, bridges):
        retValue = False

        if bridges is not None and len(bridges) > 0:
            for bridge in bridges:
                if (bridge[0] == node1 and bridge[1] == node2) or \
                (bridge[1] == node1 and bridge[0] == node2):
                    retValue = True

        return retValue

    def checkParity(self, G):
        degreeList = networkx.degree(G)
        oddNumber = 0
        odds = []
        for i, degree in degreeList.iteritems():
            if degree % 2 != 0:
                oddNumber += 1
                odds.append(i)

        retValue = self.NONE
        if oddNumber == 0:
            retValue = self.FULL
        elif oddNumber == 2:
            retValue = self.HALF

        return retValue, odds

    def isCompact(self, G):
        if G is None:
            return False
        if len(G.nodes()) == 0:
            return False
        H = G.copy()
        for node in H.nodes_iter(data=True):
            node[1]['visited'] = False
        start_node = H.nodes(data=True)[0]
        nodesVisited =[]
        nodeList = self.dfsCompact(H, start_node, nodesVisited )
        retValue = False
        if len(nodeList) == len(G.nodes()):
            retValue = True
        return retValue

    def dfsCompact(self, G, actual, nodesVisited):
        actual[1]['visited'] = True
        nodesVisited.append(actual)
        for neighbor_num in networkx.all_neighbors(G, actual[0]):
            neighbor = G.nodes(data=True)[G.nodes().index(neighbor_num)]
            if neighbor[1]['visited'] is False:
                    nodesVisited = self.dfsCompact(G, neighbor, nodesVisited)
        return nodesVisited

    def find_bridges(self, G):
        new_G = G.copy()
        for node in new_G.nodes_iter(data=True):
            node[1]['visited'] = False
            node[1]['d'] = sys.maxint
            node[1]['low'] = sys.maxint
        bridges = []
        start_node = new_G.nodes(data=True)[0][0]
        (bridges, counter, new_G) = self.__DFS_bridges(new_G, start_node, None, 0, bridges)
        return bridges

    def __DFS_bridges(self, G, actual, father, counter, bridges):
        G.node[actual]['visited'] = True
        counter += 1
        G.node[actual]['d'] = counter
        G.node[actual]['low'] = counter

        for neighbor in networkx.all_neighbors(G, actual):

            if father is None or neighbor != father:
                if G.node[neighbor]['visited'] is False:
                    (bridges, counter, G) = self.__DFS_bridges(G, neighbor, actual, counter, bridges)
                    G.node[actual]['low'] = min(G.node[actual]['low'], G.node[neighbor]['low'])
                else:
                    G.node[actual]['low'] = min(G.node[actual]['low'], G.node[neighbor]['d'])

        if G.node[actual]['low'] == G.node[actual]['d'] and father is not None:
            bridges.append([actual, father])

        return (bridges, counter, G)

    def __DFS_bridges_(self, G, actual, father, counter, bridges):
        actual[1]['visited'] = True
        counter += 1
        actual[1]['d'] = counter
        actual[1]['low'] = counter

        for neighbor_num in networkx.all_neighbors(G, actual[0]):
            neighbor = G.nodes(data=True)[G.nodes().index(neighbor_num)]

            if father is None or neighbor[0] != father[0]:
                if neighbor[1]['visited'] is False:
                    (bridges, counter, G, neighbor) = self.__DFS_bridges(G, neighbor, actual, counter, bridges)
                    actual[1]['low'] = min(actual[1]['low'], neighbor[1]['low'])
                else:
                    actual[1]['low'] = min(actual[1]['low'], neighbor[1]['d'])

        if actual[1]['low'] == actual[1]['d'] and father is not None:
            bridges.append([actual[0], father[0]])

        return (bridges, counter, G)
