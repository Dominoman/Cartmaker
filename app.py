import sys

from PySide6.QtCore import QItemSelection, QPersistentModelIndex
from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication

from crt import Crt, EasyFS, EasyFile
from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.action_Open_crt.triggered.connect(self.file_open_crt)
        self.actionAdd_file_s.triggered.connect(self.add_file)
        self.actionDelete_file_s.triggered.connect(self.delete_file)
        self.actionUp.triggered.connect(self.up)
        self.actionDown.triggered.connect(self.down)
        self.model = EasyFS()
        self.tableView.setModel(self.model)
        self.tableView.selectionModel().selectionChanged.connect(self.table_change)

    def file_open_crt(self) -> None:
        file = QFileDialog.getOpenFileName(self, 'Open file', filter="Cart files (*.crt);;All files (*.*)")
        if file[0] == '':
            return
        with open(file[0], "rb") as f:
            crt = Crt.from_bytes(f.read())
        self.model.from_bytes(crt.get_raw())

    def add_file(self) -> None:
        files = QFileDialog.getOpenFileNames(self, "Add file(s)", filter="PRG files (*.prg);;All files(*.*)")
        if len(files[0]) == 0:
            return
        for file in files[0]:
            self.model.add_file(EasyFile(file))

    def delete_file(self) -> None:
        index_list = []
        indexes = self.tableView.selectionModel().selectedRows()
        for model_index in indexes:
            index = QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.model.removeRow(index.row())
            self.model.layoutChanged.emit()

    def up(self) -> None:
        pass

    def down(self) -> None:
        pass

    def table_change(self, modelindex: QItemSelection) -> None:
        b = modelindex.count() > 0
        self.actionDelete_file_s.setEnabled(b)
        self.actionUp.setEnabled(b)
        self.actionDown.setEnabled(b)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
