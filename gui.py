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
import ctypes
import cv2
import matplotlib.pyplot as plt
import math
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

        self.setWindowIcon(QIcon('images/Chess-icon.png'))

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
        self.txtKnights.setText('0')

        self.ShowImage()

        self.foundSolution = False

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
        numKnights = int(self.txtKnights.text())

        # before loop seed generator
        #random.seed(454)

        if numIterations == 0:
            numIterations = 1000
            countIter = 0
            guesses = -1
            piecesNumbers = {'queen': numQueens, 'rook':numRooks, 'bishop':numBishops, 'knight':numKnights}
            numberOfPieces = numQueens+numRooks+numBishops+numKnights
            #self.n = self.GetHValue(numQueens,numRooks,numBishops,numKnights) #start with 1x1 board
            self.n = math.ceil(float(numQueens)*1.01+float(numRooks)*1.0+float(numBishops)*.4+float(numKnights)*.2)
            boardMaxIncrease = numberOfPieces - self.n
            pl=[]
            piecesPlaced = -1
            self.boardObject.changeSize(self.n)
            print('Checking size: ',self.n)
            for pc in piecesNumbers:
                for _ in range(piecesNumbers[pc]):
                    piecesPlaced+=1
                    row = int(piecesPlaced / self.n)
                    col = int(piecesPlaced % self.n)
                    pl.append((pc,row,col))
            for iter in range(numIterations):
                countIter += 1
                # run the solver for one iteration                
                pl, solFound = minConflicts(pl, self.n)
                # if a solution is found, alert the user
                if solFound:
                    break
            if solFound: #Board is too big
                for boardsize in range(1,numberOfPieces):
                    guesses += 1
                    lastSuccess = pl.copy()
                    print('Checking size: ',self.n-boardsize)
                    pl=[]
                    piecesPlaced = -1
                    self.boardObject.changeSize(self.n-boardsize)
                    for pc in piecesNumbers:
                        for _ in range(piecesNumbers[pc]):
                            piecesPlaced+=1
                            row = int(piecesPlaced / (self.n-boardsize))
                            col = int(piecesPlaced % (self.n-boardsize))
                            pl.append((pc,row,col))
                    for iter in range(numIterations):                        
                        # run the solver for one iteration
                        countIter+=1
                        pl, solFound = minConflicts(pl, self.n-boardsize)
                        if solFound:
                            break
                    if not solFound: #Found minimum size
                        self.boardObject.changeSize(self.n-boardsize+1)
                        self.boardObject.fillBoard(lastSuccess)
                        self.ShowImage(False)
                        QMessageBox.about(self, "Success", "Found a solution for the problem in %d iterations. Heuristic was off by %s"%(countIter,guesses))
                        return
            else: #Board is too small                
                for boardsize in range(1,boardMaxIncrease+1):
                    guesses += 1
                    print('Checking size: ',boardsize+self.n)
                    pl=[]
                    piecesPlaced = -1
                    self.boardObject.changeSize(self.n+boardsize)
                    for pc in piecesNumbers:
                        for _ in range(piecesNumbers[pc]):
                            piecesPlaced+=1
                            row = int(piecesPlaced / self.n)
                            col = int(piecesPlaced % self.n)
                            pl.append((pc,row,col))
                    for iter in range(numIterations):                        
                        # run the solver for one iteration
                        countIter+=1
                        pl, solFound = minConflicts(pl, self.n+boardsize)  
                        # if a solution is found, alert the user
                        if solFound:
                            self.boardObject.fillBoard(pl)
                            self.ShowImage(False)
                            QMessageBox.about(self, "Success", "Found a solution for the problem in %d iterations. Heuristic was off by %s"%(countIter,guesses))
                            return
                   
        elif desiredN > 0:
            self.n = desiredN
            self.boardObject.changeSize(desiredN)
            # make a dictionary of chess pieces we are potentially going to use
            piecesNumbers = {'queen': numQueens, 'rook':numRooks, 'bishop':numBishops, 'knight':numKnights}


            pl = [] # pieces list that is actually used for the solver
            totalPieces=-1

            # add the pieces to the list
            for pc in piecesNumbers:
                for _ in range(piecesNumbers[pc]):
                    totalPieces+=1
                    row = int(totalPieces / self.n)
                    col = int(totalPieces % self.n)

                    pl.append((pc,row,col))


            # run solver for designated number of iterations until we find a solution or bust
            for iter in range(numIterations):
                
                # run the solver for one iteration
                pl, solFound = minConflicts(pl, self.n)

                # if a solution is found, alert the user
                if solFound:
                    self.boardObject.fillBoard(pl)
                    self.ShowImage(False)
                    QMessageBox.about(self, "Success", "Found a solution for the problem in %d iterations"%(iter+1))
                    break

                if iter % 50 == 0:
                    self.boardObject.fillBoard(pl)
                    self.ShowImage(False)


            if iter == numIterations-1:
                QMessageBox.about(self, "Bummer", "No solution found!")
        elif desiredN ==0:
            piecesNumbers = {'queen': numQueens, 'rook':numRooks, 'bishop':numBishops, 'knight':numKnights}
            numberOfPieces = numQueens+numRooks+numBishops+numKnights
            self.n = 1 #start with 1x1 board
            while self.n*self.n < numberOfPieces: #increase size until all pieces can fit
                self.n += 1
            boardMaxIncrease = numberOfPieces - self.n
            found=False
            for boardsize in range(boardMaxIncrease+1):
                print('Checking size: ',boardsize+self.n)
                pl=[]
                piecesPlaced = -1
                self.boardObject.changeSize(self.n+boardsize)
                for pc in piecesNumbers:
                    for _ in range(piecesNumbers[pc]):
                        piecesPlaced+=1
                        row = int(piecesPlaced / self.n)
                        col = int(piecesPlaced % self.n)

                        pl.append((pc,row,col))
                for iter in range(numIterations):
                    
                    # run the solver for one iteration
                    pl, solFound = minConflicts(pl, self.n+boardsize)
                    
                    
                    # if a solution is found, alert the user
                    if solFound:
                        self.boardObject.fillBoard(pl)
                        self.ShowImage(False)
                        QMessageBox.about(self, "Success", "Found a solution for the problem in %d iterations"%((numIterations*boardsize)+iter+1))
                        return
                        

                    #if iter % 50 == 0:
                        #self.boardObject.fillBoard(pl)
                        #self.ShowImage(False)
                
        else:
            QMessageBox.about(self, "Error", "Sorry, this beta version does not support those parameters.")
            return

        



# playing board class
class playingBoard():


    def __init__(self, square, n):

        self.piecesNames = ['queen', 'rook', 'bishop','knight']
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
        if n%2==0:
            self.board = np.kron([[1, 0] * halfDim, [0, 1] * halfDim] * halfDim, np.full((step, step), 255))
        else:
            first = [1,0]*halfDim
            first.append(1)
            second = [0,1]*halfDim
            second.append(0)
            third = [first,second]*halfDim
            third.append(first)
            self.board = np.kron(third, np.full((step, step), 255))
            #[first, second] * (halfDim+1)

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


    myappid = 'CSI535.ChessSolver.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    window = SPApp()
    window.show()
    sys.exit(app.exec_())
