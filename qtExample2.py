import sys
from PyQt5.QtCore import  Qt, QVariant, QModelIndex, QAbstractListModel
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListView

#################################################################### 
def main(): 
    app = QApplication(sys.argv) 
    w = MyWindow() 
    w.show()
    sys.exit(app.exec_())
    
    #sys.exit(app.exec_()) 

#################################################################### 
class MyWindow(QWidget): 
    def __init__(self, *args): 
        QWidget.__init__(self, *args)
        print("Woot")

        # create table
        list_data = [1,2,3,4]
        lm = MyListModel(list_data, self)
        lv = QListView()
        lv.setModel(lm)
        #lv.setWindowTitle('Woot!')

        # layout
        layout = QVBoxLayout()
        layout.addWidget(lv) 
        self.setLayout(layout)

#################################################################### 
class MyListModel(QAbstractListModel): 
    def __init__(self, datain, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args) 
        self.listdata = datain
 
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else: 
            return QVariant()

####################################################################
if __name__ == "__main__": 
    main()
