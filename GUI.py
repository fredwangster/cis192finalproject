    # use PyQT's QTableView and QAbstractTableModel
    # to present tabular data
    # allow sorting by clicking on the header title
    # tested with Python 3.1.1 and PyQT 4.5.2
    # ene
import operator
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time

class MyWindow(QWidget):
    def __init__(self, data_list, header, *args):
        QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 200, 420, 250)
        self.setWindowTitle("Exploring PyQT's QTableView")
        table_model = MyTableModel(self, data_list, header)
        table_view = QTableView()
        table_view.setModel(table_model)
        # enable sorting
        table_view.setSortingEnabled(True)
        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        self.setLayout(layout)
        
class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
            return QVariant(self.mylist[index.row()][index.column()])
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
            return QVariant()
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))
        
header = ['First Name', 'Last Name', 'Age', 'Weight']
# a list of (name, age, weight) tuples
data_list = [
('Heidi', 'Kalumpa', '36', '127'),
('Frank', 'Maruco', '27', '234'),
('Larry', 'Pestraus', '19', '315'),
('Serge', 'Romanowski', '59', '147'),
('Carolus', 'Arm', '94', '102'),
('Michel', 'Sargnagel', '21', '175')
]
app = QApplication([])
splash_pix = QPixmap('splash_loading.png')
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
splash.setMask(splash_pix.mask())
splash.show()
time.sleep(5)
win = MyWindow(data_list, header)
win.show()
splash.finish(win)
app.exec_()

