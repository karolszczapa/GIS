from PyQt4.QtGui import QGraphicsEllipseItem

class Node(QGraphicsEllipseItem):

    RADIUS = 0.01

    def __init__(self, x, y, number = 0, radius = RADIUS,
                 parent = None, scene = None):
        QGraphicsEllipseItem.__init__(
                self,
                x-radius/2,
                y-radius/2,
                2*radius,
                2*radius,
                parent,
                scene,
                )
        self.number = number

    def centerX(self):
        return self.sceneBoundingRect().center().x()
    def centerY(self):
        return self.sceneBoundingRect().center().y()
    def getNumber(self):
        return self.number
