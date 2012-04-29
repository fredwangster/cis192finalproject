# use PyQT's QTableView and QAbstractTableModel
# to present tabular data (with column sort option)
# tested with Python 3.1 and PyQT 4.5

import operator
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
from analyzer import Analyzer
from scanner import scanner

class MyWindow(QWidget):
    def __init__(self, element_list, header, *args):
        QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 200, 900, 300)
        self.setWindowTitle("Sorting PyQT's QTableView")
        self.button = QPushButton("Start")
        self.button.clicked.connect(self.start_analyzing)
        #self.button.disa
        self.header = header
        self.mydata = element_list
        # create table
        self.tmodel = MyTableModel(self, self.mydata, self.header)
        table = self.createTable()

        # use vbox layout
        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def createTable(self):
        # create table view
        tview = QTableView()
        # set table model
        #tmodel = MyTableModel(self, self.mydata, self.header)
        tview.setModel(self.tmodel)
        
        # set minimum size of table
        tview.setMinimumSize(450, 300)
        # hide grid
        tview.setShowGrid(False)
        # set font
        font = QFont("Courier New", 8)
        tview.setFont(font)
        # hide vertical header
        vh = tview.verticalHeader()
        vh.setVisible(False)
        # set horizontal header properties
        hh = tview.horizontalHeader()
        hh.setStretchLastSection(True)
        # set column width to fit contents
        tview.resizeColumnsToContents()
        # set all row heights
        nrows = len(self.mydata)
        for row in range(nrows):
            tview.setRowHeight(row, 18)
        # enable sorting
        tview.setSortingEnabled(True)
        return tview
        
    def start_analyzing(self):
        self.threads = []
        downloader_caller =DownloadCaller(self.tmodel)
        self.threads.append(downloader_caller)
        downloader_caller.start()
        
        
class DownloadThread(QThread):
    def __init__(self, url, model):
        QThread.__init__(self)
        self.url = url
        self.model = model

    def run(self):
        #info = urllib2.urlopen(self.url).info()
        html_name,url_name = scanner([self.url],"000")
        a = Analyzer(html_name, url_name)
        
        print self.url
        self.model.mydata = self.model.mydata + [(self.url,a.getAds()[1],a.getAds()[0],a.getUniqueVisitors(),"0")]
        
        self.model.emit(SIGNAL("layoutChanged()"))
        

class DownloadCaller(QThread):
    def __init__(self, model):
        QThread.__init__(self)
        f = open("top_sites.txt",'r')
        self.urls = f.readlines()
        f.close()
        self.model = model
        

    def run(self):
        self.threads = []
        for url in self.urls:
            downloader = DownloadThread(url, self.model)
            self.threads.append(downloader)
            downloader.start()
            time.sleep(1)
        
class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mydata, header, *args):
        """
        mydata is list of tuples
        header is list of strings
        tuple length has to match header length
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.mydata = mydata
        self.header = header

    def rowCount(self, parent):
        return len(self.mydata)

    def columnCount(self, parent):
        if len(self.mydata) > 0:
            return len(self.mydata[0])
        else:
            return 0
    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.mydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()

    def sort(self, col, order):
        
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mydata = sorted(self.mydata,
            key=operator.itemgetter(col))
        if order != Qt.DescendingOrder:
            self.mydata.reverse()
           
        self.emit(SIGNAL("layoutChanged()"))





if __name__ == "__main__":
    header = ['URL', 'Total Line in Source', 'Ads in Source', 'Unique Visitors', 'Rank']
    # a list of (name, age, weight) tuples
    data_list =[]

    #data_list= data_list+ [('Michel', 'Sargnagel', '21', '175')]
    app = QApplication([])
    splash_pix = QPixmap('loading.jpg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    time.sleep(5)
    win = MyWindow(data_list, header)
    win.show()
    splash.finish(win)
    app.exec_()

