#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Ethan Webster
#
# Created:     12/05/2018
# Copyright:   (c) Ethan Webster 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import numpy as np
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFileDialog, QMessageBox, QSystemTrayIcon
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from backend import minConflicts


fileTypes = "JPEG (*.jpg);;PNG (*.png);;TIFF (*.tif);;BMP (*.bmp);;GIF (*.gif);;All Files (*)"

qtCreatorFile = "guiLayout.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class FormatException:
    pass


class SPApp(QMainWindow, Ui_MainWindow):

    # imglbl_height = 512
    # imglbl_width = 512
    boardDim = 680
    n = 8

    def __init__(self):

        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.boardObject = playingBoard(self.boardDim,self.n)

        self.setupUi(self)
        self.btnSolve.clicked.connect(self.findSolution)
        self.btnReset.clicked.connect(self.ResetBoard)
        self.btnSave.clicked.connect(self.SaveImage)

        self.txtIterations.setText('1000')
        self.txtBoardSize.setText('8')
        self.txtQueens.setText('8')
        self.txtRooks.setText('0')
        self.txtBishops.setText('0')
        self.txtUnicorns.setText('0')

        self.ShowImage()

        #self.lblImg.resize(self.imglbl_width, self.imglbl_height)
        #self.lblImg.setAlignment(QtCore.Qt.AlignCenter)

    def to_rgb(self, im):
        return np.dstack([im.astype(np.uint8)] * 3).copy(order='C')

    def ShowImage(self,reset=True):


        # if self.image is None:
        #     QMessageBox.about(self, "Error", "Please select an image file first.")
        #     return

        # if self.image.ndim != 3:
        #dispImg = color.gray2rgb(self.image)
        # else:
        #     dispImg = self.image
        if reset:
            pb = self.boardObject.getOrigBoard()
        else:
            pb = self.boardObject.getBoard()

        height, width = pb.shape

        # plt.imshow(pb)
        # plt.show()

        dispImg = self.to_rgb(pb)

        #dispImg = np.require(dispImg, np.uint8, 'C')

        qtImg = QImage(dispImg.data, width, height, dispImg.strides[0], QImage.Format_RGB888)

        pix = QPixmap(qtImg)

        #self.scene.addPixmap(pix)

        #pixmap = QPixmap('image.jpeg')

        # newWidth = round(self.imglbl_height/height*width)

        #pixmap = pix.scaled(newWidth, self.imglbl_height)

        pixmap = pix.scaled(self.boardDim,self.boardDim)

        self.lblImg.setPixmap(pixmap)

        #self.lblImg.resize(512, 250)

        # Optional, resize window to image size
        #self.resize(pix.width(),pix.height())


    # resets the board
    def ResetBoard(self):
        self.ShowImage()


    # def ConvertToGray(self):

    #     if self.image.ndim == 3:
    #         self.image = (color.rgb2gray(self.image)*255).astype(np.uint8)
    #         self.ShowImage()




    def SaveImage(self):

        savePath,_ = QFileDialog.getSaveFileName(self, 'Save Image As', "", fileTypes)

        try:
            if savePath:
                cv2.imwrite(savePath, self.boardObject.getBoard())

        except:
            QMessageBox.about(self, "Error", "Cannot save file. Please try again.")


    # calls backend until solution is found
    def findSolution(self):
        
        numIterations = int(self.txtIterations.text())
        desiredN = int(self.txtBoardSize.text())
        numQueens = int(self.txtQueens.text())
        numRooks = int(self.txtRooks.text())
        numBishops = int(self.txtBishops.text())
        numUnicorns = int(self.txtUnicorns.text())

        # before loop seed generator
        #random.seed(454)

        if desiredN > 0 and desiredN % 2 == 0 and desiredN != self.n:
            self.n = desiredN
            self.boardObject.changeSize(desiredN)

        conflictsList = [1]*self.n

        pl = []
        qind = -1
        for i in range(self.n):
            for j in range(self.n):
                qind+=1
                if qind < numQueens:
                    pl.append(('queen',i,j))


        for iter in range(numIterations):
            
            pl, conflictsList, solFound = minConflicts(pl, self.n, conflictsList)

            if solFound:
                QMessageBox.about(self, "Success", "Found a solution for the problem in %d iterations"%(iter+1))
                self.boardObject.fillBoard(pl)
                self.ShowImage(False)
                break

            if iter % 10 == 0:
                self.boardObject.fillBoard(pl)
                self.ShowImage(False)
                #print(conflictList)



# playing board class
class playingBoard():


    def __init__(self, square, n):

        self.piecesNames = ['queen', 'rook', 'bishop','knight','unicorn']
        self.pieces = {}
        self.square = square
        self.n = n
        self.workingBoard = None
        self.board = None

        self.obtainPieces()
        self.makeBoard()

    def getBoard(self):
        return self.workingBoard

    def getOrigBoard(self):
        return self.board

    def changeSize(self, n):
        self.n = n
        self.obtainPieces()
        self.makeBoard()


    def obtainPieces(self):

        ss = int(self.square/self.n*(2/3))

        # Load in the images
        for name in self.piecesNames:

            img = cv2.imread('images/{0}.png'.format(name),0)

            scaledImg = cv2.resize(img, (ss, ss), interpolation=cv2.INTER_CUBIC)

            self.pieces[name] = scaledImg


    def makeBoard(self):

        n = self.n
        step = int(self.square/n)
        halfDim = int(n/2)

        self.board = np.kron([[1, 0] * halfDim, [0, 1] * halfDim] * halfDim, np.full((step, step), 255))


    def placePiece(self, name, x, y):

        step = int(self.square/self.n)
        ss = int(step*(2/3))
        sp = int(step*(1/6))

        pieceImg = self.pieces[name]

        origX = step*x + sp
        origY = step*y + sp
        xlim = ss+origX
        ylim = ss+origY

        self.workingBoard[origX:xlim, origY:ylim] = pieceImg


    def fillBoard(self, piecesList):

        self.workingBoard = np.copy(self.board)

        for (pieceName, x, y) in piecesList:
            self.placePiece(pieceName, x, y)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SPApp()
    window.show()
    sys.exit(app.exec_())
