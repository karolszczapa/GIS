from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGraphicsView
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QSizePolicy

from PyQt4.QtGui import QTransform
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QSlider
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QIntValidator

from PyQt4.QtCore import QCoreApplication

from GraphGraphicsScene import GraphGraphicsScene
from Euler import Euler
from Generator import Generator
from PyQt4.QtCore import Qt
from GraphFile import GraphFile
from PyQt4.QtGui import QFileDialog


class GraphGui(QWidget):
    def __init__(self, G=None, pos=None, parent=None):
        QWidget.__init__(self, parent)
        self.scene = GraphGraphicsScene(G, pos, self)
        self.view = QGraphicsView(self.scene, self)
        self.button = QPushButton('Quit', self)
        self.nodeButton = QPushButton('Node', self)
        self.edgeButton = QPushButton('Edge', self)
        self.addButton = QPushButton('Add', self)
        self.deleteButton = QPushButton('Delete', self)
        self.printButton = QPushButton('Print', self)
        self.eulerButton = QPushButton('Euler', self)
        self.generateFullButton = QPushButton('Full', self)
        self.generateHalfButton = QPushButton('Half', self)
        self.infoButton = QPushButton('Info', self)
        #self.testButton = QPushButton('Test', self)
        self.nodesInputLabel = QLabel('Nodes', self)
        self.edgesInputLabel = QLabel('Edges', self)
        self.saveButton = QPushButton('Save', self)
        self.loadButton = QPushButton('Load', self)
        self.saveAsButton = QPushButton('SaveAs', self)
        self.bridgeButton = QPushButton('Bridge', self)
        self.stepSlider = QSlider(self)
        self.cursorLabelX = QLabel('X:', self)
        self.cursorLabelY = QLabel('Y:', self)
        self.nodeNumberLabel = QLabel('Nr:', self)
        self.fileLabel = QLabel('File:', self)
        self.nodeInfo = QLabel('N:', self)
        self.edgeInfo = QLabel('E:', self)
        self.eulerInfo = QLabel('None', self)
        #self.fileInput = QLineEdit(self)
        self.fileInput = QLabel('',self)
        self.euler = Euler()
        self.eulerStep = 0
        self.eulerPath =[]

        validator = QIntValidator(0, 10000)

        self.nodesNumberInput = QLineEdit(self)
        self.nodesNumberInput.setValidator(validator)
        self.edgesNumberInput = QLineEdit(self)
        self.edgesNumberInput.setValidator(validator)

        self.cursorLabelX.setMinimumSize(150, 25)
        self.cursorLabelY.setMinimumSize(150, 25)
        self.nodeNumberLabel.setMinimumSize(150, 25)

        self.labelsGroup = QVBoxLayout()
        self.labelsGroup.addWidget(self.cursorLabelX)
        self.labelsGroup.addWidget(self.cursorLabelY)
        self.labelsGroup.addWidget(self.nodeNumberLabel)

        HEIGHT = 50
        WIDTH = 50

        self.nodeButton.setFixedSize(HEIGHT, WIDTH)
        self.edgeButton.setFixedSize(HEIGHT, WIDTH)
        self.addButton.setFixedSize(HEIGHT, WIDTH)
        self.button.setFixedSize(HEIGHT, WIDTH)
        self.deleteButton.setFixedSize(HEIGHT, WIDTH)
        self.printButton.setFixedSize(HEIGHT, WIDTH)
        self.eulerButton.setFixedSize(HEIGHT, WIDTH)
        self.generateFullButton.setFixedSize(HEIGHT, WIDTH)
        self.generateHalfButton.setFixedSize(HEIGHT, WIDTH)
        self.saveButton.setFixedSize(HEIGHT, WIDTH)
        self.loadButton.setFixedSize(HEIGHT, WIDTH)
        self.saveAsButton.setFixedSize(HEIGHT, WIDTH)
        self.infoButton.setFixedSize(HEIGHT, WIDTH)
        self.bridgeButton.setFixedSize(HEIGHT, WIDTH)
        self.nodesNumberInput.setFixedSize(HEIGHT*2, 28)
        self.edgesNumberInput.setFixedSize(HEIGHT*2, 28)
        self.stepSlider.setFixedSize(HEIGHT*2, 28)
        #self.testButton.setFixedSize(HEIGHT, WIDTH)

        self.disableSlider()
        self.stepSlider.setOrientation(Qt.Horizontal)
        horizontal_expanding_spacer1 = QSpacerItem(0,
                                                  0,
                                                  QSizePolicy.Expanding,
                                                  QSizePolicy.Minimum)


        self.fileGroup = QHBoxLayout()
        self.fileGroup.addWidget(self.fileLabel)
        self.fileGroup.addWidget(self.fileInput)
        self.fileGroup.addItem(horizontal_expanding_spacer1)

        self.actionsButtonGroup = QHBoxLayout()
        self.actionsButtonGroup.addWidget(self.addButton)
        self.actionsButtonGroup.addWidget(self.deleteButton)
        self.actionsButtonGroup.addWidget(self.printButton)
        self.actionsButtonGroup.addWidget(self.eulerButton)
        self.actionsButtonGroup.addWidget(self.generateFullButton)
        self.actionsButtonGroup.addWidget(self.generateHalfButton)
        self.actionsButtonGroup.addWidget(self.saveButton)
        self.actionsButtonGroup.addWidget(self.loadButton)
        self.actionsButtonGroup.addWidget(self.saveAsButton)
        self.actionsButtonGroup.addWidget(self.infoButton)
        self.actionsButtonGroup.addWidget(self.bridgeButton)
        #self.actionsButtonGroup.addWidget(self.testButton)
        self.actionsButtonGroup.addWidget(self.button)

        self.topGroup=QVBoxLayout()
        self.topGroup.addItem(self.fileGroup)
        self.topGroup.addItem(self.actionsButtonGroup)

        horizontal_expanding_spacer = QSpacerItem(10,
                                                  10,
                                                  QSizePolicy.Expanding,
                                                  QSizePolicy.Minimum)

        self.actionsButtonGroup.addItem(horizontal_expanding_spacer)
        self.actionsButtonGroup.addItem(self.labelsGroup)

        self.modeButtonGroup = QVBoxLayout()
        self.modeButtonGroup.addWidget(self.nodeButton)
        self.modeButtonGroup.addWidget(self.edgeButton)
        self.modeButtonGroup.addWidget(self.nodesInputLabel)
        self.modeButtonGroup.addWidget(self.nodesNumberInput)
        self.modeButtonGroup.addWidget(self.edgesInputLabel)
        self.modeButtonGroup.addWidget(self.edgesNumberInput)
        self.modeButtonGroup.addWidget(self.stepSlider)

        vertical_expanding_spacer = QSpacerItem(10,
                                                10,
                                                QSizePolicy.Minimum,
                                                QSizePolicy.Expanding)

        self.modeButtonGroup.addItem(vertical_expanding_spacer)

        self.infoGroup = QVBoxLayout()
        self.infoGroup.addWidget(self.edgeInfo)
        self.infoGroup.addWidget(self.nodeInfo)
        self.infoGroup.addWidget(self.eulerInfo)

        self.modeButtonGroup.addItem(self.infoGroup)

        self.button.clicked.connect(QCoreApplication.instance().quit)
        self.addButton.clicked.connect(self.add)
        self.deleteButton.clicked.connect(self.delete)
        self.nodeButton.clicked.connect(self.nodeButtonEvent)
        self.edgeButton.clicked.connect(self.edgeButtonEvent)
        self.printButton.clicked.connect(self.printButtonEvent)
        self.eulerButton.clicked.connect(self.findEulerPath)
        self.generateFullButton.clicked.connect(self.generateFull)
        self.generateHalfButton.clicked.connect(self.generateHalf)
        #self.testButton.clicked.connect(self.scene.changeColor)
        self.saveAsButton.clicked.connect(self.saveAsFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.loadButton.clicked.connect(self.loadFile)
        self.scene.cursorPositionSignal.connect(self.setLabels)
        self.scene.nodeNumberSignal.connect(self.setLabelNumber)
        self.stepSlider.sliderMoved.connect(self.setEulerStep)
        self.bridgeButton.clicked.connect(self.findBridges)
        self.infoButton.clicked.connect(self.setInfo)

        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layoutH = QHBoxLayout()
        layoutH.addWidget(self.view)
        layoutH.addItem(self.modeButtonGroup)

        layoutV = QVBoxLayout()
        layoutV.addItem(self.topGroup)
        layoutV.addItem(layoutH)

        self.setLayout(layoutV)

        self.setWindowTitle('Example')

        self.scene.setSceneRect(0, 0, 1, 1)

        self.view.setMouseTracking(True)

        self.showMaximized()
        self.graphFile = GraphFile("file.txt")
    def findBridges(self):
        bridges = self.euler.find_bridges(self.scene.G)
        print bridges

    def generate(self, h_or_f):
        generator = Generator()
        nodesNumberStr = self.nodesNumberInput.text()
        edgesNumberStr = self.edgesNumberInput.text()

        if nodesNumberStr == "" or edgesNumberStr == "":
            return

        nodeNumber = int(nodesNumberStr)
        edgesNumber = int(edgesNumberStr)

        G = None
        if h_or_f == 'FULL':
            G = generator.generate_full_euler_graph(nodeNumber,edgesNumber)
        elif h_or_f == 'HALF':
            G = generator.generate_half_euler_graph(nodeNumber,edgesNumber)

        if G is not None:
            self.scene.clear()

            self.scene.drawGraph(G)

        self.setInfo()

    def setInfo(self):
        self.edgeInfo.setText("E: "+str(len(self.scene.G.edges())))
        self.nodeInfo.setText("N: "+str(len(self.scene.G.nodes())))

        info, odds = self.euler.checkGraph(self.scene.G)
        self.eulerInfo.setText(info)

    def generateHalf(self):
        self.generate('HALF')

    def generateFull(self):
        self.generate('FULL')

    def add(self):
        self.scene.add()
        self.setInfo()

    def delete(self):
        self.scene.delete()
        self.setInfo()

    def findEulerPath(self):
        eulerPath = self.euler.start(self.scene.getGraph())
        print eulerPath

        if eulerPath is not None and len(eulerPath) > 0:
            self.enableSlider(len(eulerPath))
            self.eulerPath = eulerPath

    def setEulerStep(self, stepNum):

        self.scene.setColorForAllEdges(QColor.fromRgb(0,0,0))
        if stepNum > 0:
            for i in range(stepNum):
                node1 = self.eulerPath[i]
                node2 = self.eulerPath[i + 1]
                self.scene.setColorForEdge(node1, node2, QColor.fromRgb(0, 255, 0))

    def resizeEvent(self, event):
        w = self.view.width() - 10
        h = self.view.height() - 10

        transform = QTransform.fromScale(w, h)

        self.view.setTransform(transform)
        QWidget.resizeEvent(self, event)

    def enableSlider(self, maximum):
        self.stepSlider.setEnabled(True)
        self.stepSlider.setMinimum(0)
        self.stepSlider.setMaximum(maximum - 1)

    def disableSlider(self):
        self.stepSlider.setDisabled(False)

    def setLabels(self, x, y):
        self.cursorLabelX.setText("X:" + str(x))
        self.cursorLabelY.setText("Y:" + str(y))

    def setLabelNumber(self, number):
        self.nodeNumberLabel.setText("Nr:" + str(number))

    def nodeButtonEvent(self):
        if self.scene.getMode() == 'None':
            self.scene.changeMode('Node')
            self.nodeButton.setFlat(True)
        elif self.scene.getMode() == 'Node':
            self.nodeButton.setFlat(False)
            self.scene.changeMode('None')
        elif self.scene.getMode() == 'Edge':
            self.edgeButton.setFlat(False)
            self.scene.changeMode('Node')
            self.nodeButton.setFlat(True)

    def edgeButtonEvent(self):
        if self.scene.getMode() == 'None':
            self.scene.changeMode('Edge')
            self.edgeButton.setFlat(True)
        elif self.scene.getMode() == 'Edge':
            self.scene.changeMode('None')
            self.edgeButton.setFlat(False)
        elif self.scene.getMode() == 'Node':
            self.scene.changeMode('Edge')
            self.nodeButton.setFlat(False)
            self.edgeButton.setFlat(True)

    def printButtonEvent(self):
        print self.scene.G.nodes()
        print self.scene.G.edges()

    def saveFile(self):
        if self.graphFile.path != "":
            self.graphFile.save(self.scene.G, self.scene.getPos())
        else:
            self.saveAsFile()

    def saveAsFile(self):
        path = QFileDialog.getSaveFileName(self, "Open Graph", ".", "Text files (*.txt)")
        self.setFilePath(path)
        self.graphFile.save(self.scene.G, self.scene.getPos())

    def loadFile(self):
        path = QFileDialog.getOpenFileName(self, "Open Graph", ".", "Text files (*.txt)")
        self.setFilePath(path)
        (G, pos,n,n) = self.graphFile.load()
        self.scene.clear()

        self.scene.drawGraph(G, pos)

        self.setInfo()

    def setFilePath(self, path):
        self.graphFile.path = path
        self.fileInput.setText(path)
