import sys

from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication

from crt import Crt, EasyFS
from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.action_Decompile.triggered.connect(self.file_decompile)
        self.actionAdd_file_s.triggered.connect(self.add_file)
        self.actionDelete_file_s.triggered.connect(self.delete_file)
        self.actionUp.triggered.connect(self.up)
        self.actionDown.triggered.connect(self.down)

    def file_decompile(self) -> None:
        file = QFileDialog.getOpenFileName(self, 'Open file', filter="Cart files (*.crt);;All files (*.)")
        if file[0] == '':
            return
        export_path = QFileDialog.getExistingDirectory(self, "Save path")
        if export_path == '':
            return
        with open(file[0], "rb") as f:
            crt = Crt.from_bytes(f.read())
        fs = EasyFS.from_bytes(crt.get_raw())
        fs.export(export_path)
        QMessageBox.information(self, "Decompile", f"Exported:{len(fs.files)} file(s)")

    def add_file(self) -> None:
        pass

    def delete_file(self) -> None:
        pass

    def up(self) -> None:
        pass

    def down(self) -> None:
        pass

    def table_change(self) -> None:
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
