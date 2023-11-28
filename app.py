import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from crt import Crt, EasyFS
from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.action_Decompile.triggered.connect(self.file_decompile)

    def file_decompile(self) -> None:
        file = QFileDialog.getOpenFileName(self, 'Open file', filter="Cart files (*.crt);;All files (*.)")
        if file[0] == '':
            return
        dir = QFileDialog.getExistingDirectory(self, "Save path")
        if dir == '':
            return
        with open(file[0], "rb") as f:
            crt = Crt.from_bytes(f.read())
        fs = EasyFS.from_bytes(crt.get_raw())
        fs.export(dir)
        QMessageBox.information(self,"Decompile",f"Exported:{len(fs.files)} file(s)")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
