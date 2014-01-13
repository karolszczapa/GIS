import networkx

from Node import Node
from Edge import Edge

from PyQt4.QtGui import QGraphicsScene
from PyQt4.QtGui import QGraphicsItem
from PyQt4.QtCore import pyqtSignal

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class GraphGraphicsScene(QGraphicsScene):

    cursorPositionSignal = pyqtSignal(float, float)
    nodeNumberSignal = pyqtSignal(int)

    def __init__(self, G=None, pos=None, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.G = networkx.Graph()

        if pos is None:
            pos = networkx.spring_layout(self.G)

        self.mode = 'None'
        self.lastSelectedNode = None
        self.lineDuringSelection = None
        self.edges = []
        self.nodes = []
        if G != None:
            self.drawGraph(G, pos)

    def clear(self):
        QGraphicsScene.clear(self)
        self.G.clear()
        del self.nodes[:]
        del self.edges[:]

    def drawGraph(self, G, pos = None):

        self.clear()

        if pos is None:
            pos = networkx.spring_layout(G)

        i = 0
        for n in G.nodes():
            #print str(pos[n][0]) + " " + str(pos[n][1])+ " "+str(n)
            self.addNode(pos[i][0], pos[i][1], n)
            i += 1

        for e in G.edges():
            node1 = self.nodes[e[0]]
            node2 = self.nodes[e[1]]
            self.addEdge(node1, node2)

    def getPos(self):
        points = []
        for node in self.nodes:
            point = [node.centerX(), node.centerY()]
            points.append(point)
        return points

    def setMode(self, mode):
        self.mode = mode

    def mousePressEvent(self, event):
        if self.mode == 'Edge':
            self.mousePressEventEdge(event)

        QGraphicsScene.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.mode == 'Edge':
            self.mouseReleaseEventEdge(event)

        QGraphicsScene.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.mode == 'Edge':
            self.mouseMoveEventEdge(event)
        elif self.mode == 'Node':
            self.mouseMoveEventNode(event)
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.cursorPositionSignal.emit(x, y)
        QGraphicsScene.mouseMoveEvent(self, event)
        item = self.itemAt(event.scenePos())
        if item is not None:
            if isinstance(item, Node):
                self.nodeNumberSignal.emit(item.getNumber())

    def mouseMoveEventNode(self, event):
        item = self.mouseGrabberItem()
        for e in self.edges:
            if e.hasNode(item):
                e.update()

    def mouseMoveEventEdge(self, event):
        if self.lastSelectedNode is not None:
            point1 = self.lastSelectedNode.scenePos()
            point2 = event.scenePos()
            centerX = self.lastSelectedNode.rect().center().x()
            centerY = self.lastSelectedNode.rect().center().y()
            x1 = point1.x() + centerX
            y1 = point1.y() + centerY
            x2 = point2.x()
            y2 = point2.y()
            self.lineDuringSelection.setLine(x1, y1, x2, y2)

    def mousePressEventEdge(self, event):
        item = self.itemAt(event.scenePos())
        if item is not None:
            if isinstance(item, Node):
                item.setSelected(True)
                self.lastSelectedNode = item
                centerX = item.rect().center().x()
                centerY = item.rect().center().y()
                beginPos = item.scenePos()
                x1 = beginPos.x() + centerX
                y1 = beginPos.y() + centerY
                x2 = event.scenePos().x()
                y2 = event.scenePos().y()
                self.lineDuringSelection = self.addLine(x1, y1, x2, y2)

    def mouseReleaseEventEdge(self, event):
        if self.lineDuringSelection is not None:
            self.removeItem(self.lineDuringSelection)

        item = self.itemAt(event.scenePos())
        if item is not None and self.lastSelectedNode is not None:
            if isinstance(item, Node) and item != self.lastSelectedNode:
                self.addEdge(item, self.lastSelectedNode)

        self.lineDuringSelection = None
        self.lastSelectedNode = None

    def addEdge(self, node1, node2):

        for e in self.edges:
            if e.hasNode(node1) and e.hasNode(node2):
                return

        addedEdge = Edge(node1, node2)
        self.edges.append(addedEdge)
        self.addItem(addedEdge)
        self.G.add_edge(node1.getNumber(), node2.getNumber())
        self.changeMode(self.mode)

    def add(self):
        if self.mode == 'Node':
            number = self.nodes[-1].number + 1
            self.addNode(0, 0, number)

    def addNode(self, x, y, number):
        node = Node(x, y, number)
        self.addItem(node)
        self.nodes.append(node)
        self.G.add_node(number)
        self.changeMode(self.mode)

    def deleteNode(self, node):
        self.nodes.remove(node)
        self.G.remove_node(node.getNumber())
        self.removeItem(node)
        self.changeMode(self.mode)

    def deleteEdge(self, edge):
        self.edges.remove(edge)
        self.removeItem(edge)
        self.G.remove_edge(edge.node1.getNumber(), edge.node2.getNumber())
        self.changeMode(self.mode)

    def delete(self):
        items = self.selectedItems()
        for i in items:
            self.deleteItem(i)

    def deleteItem(self, item):
        if isinstance(item, Node):
            toDelete = []
            for e in self.edges:
                if e.hasNode(item):
                    toDelete.append(e)
            for e in toDelete:
                self.deleteEdge(e)
            self.deleteNode(item)

        if isinstance(item, Edge):
            for e in self.edges:
                if e == item:
                    self.deleteEdge(e)

    def changeMode(self, mode):
        self.mode = mode
        if mode == 'Node':
            for n in self.nodes:
                n.setFlag(QGraphicsItem.ItemIsSelectable, True)
                n.setFlag(QGraphicsItem.ItemIsMovable, True)
        else:
            for n in self.nodes:
                n.setFlag(QGraphicsItem.ItemIsSelectable, False)
                n.setFlag(QGraphicsItem.ItemIsMovable, False)

        if mode == 'Edge':
            for e in self.edges:
                e.setFlag(QGraphicsItem.ItemIsSelectable, True)
        else:
            for e in self.edges:
                e.setFlag(QGraphicsItem.ItemIsSelectable, False)

    def setColorForAllEdges(self, color):
        for edge in self.edges:
            edge.setColor(color)

    def setColorForEdge(self, node1, node2, color):
        edgeToChange = None
        for edge in self.edges:
            if edge.hasNodesNum(node1, node2):
                edgeToChange = edge

        if edgeToChange is not None:
            edgeToChange.setColor(color)

    def getMode(self):
        return self.mode

    def getGraph(self):
        return self.G
