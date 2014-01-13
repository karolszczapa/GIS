from Node import Node

from PyQt4.QtGui import QGraphicsLineItem
from PyQt4.QtCore import QPointF
from PyQt4.QtCore import QLineF
from PyQt4.QtGui import QPen

class Edge(QGraphicsLineItem):

    def __init__(self, node1, node2, parent = None, scene = None):
        self.node1 = node1
        self.node2 = node2

        x1 = node1.centerX()
        y1 = node1.centerY()
        x2 = node2.centerX()
        y2 = node2.centerY()

        QGraphicsLineItem.__init__(
                self,
                x1,
                y1,
                x2,
                y2,
                parent,
                scene
                )

    def hasNode(self, node):
        if self.node1 == node or self.node2 == node:
            return True
        else:
            return False
    def hasNodesNum(self, node1, node2):
        #print self.node1.getNumber()
        #print self.node2.getNumber()
        hasNode1 = self.node1.getNumber() == node1 or self.node1.getNumber() == node2
        hasNode2 = self.node2.getNumber() == node2 or self.node2.getNumber() == node1
        #print hasNode1
        #print hasNode2
        if hasNode1 is True and hasNode2 is True:
            return True
        else:
            return False

    def update(self):
        x1 = self.node1.centerX()
        y1 = self.node1.centerY()
        x2 = self.node2.centerX()
        y2 = self.node2.centerY()

        point1 = QPointF(x1,y1)
        point2 = QPointF(x2,y2)

        line = QLineF(point1, point2)

        QGraphicsLineItem.setLine(self,line)

    def setColor(self, color):
        pen = QPen(color)
        QGraphicsLineItem.setPen(self, pen)

    def resetColor(self):
        pen = QPen(QColor.fromRgb(0,0,0))
        QGraphicsLineItem.setPen(self, pen)
