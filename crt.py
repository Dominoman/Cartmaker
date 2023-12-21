import os
import petscii_codecs
from os import path

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import QMessageBox


class Chip:
    TYPE = {0: "ROM", 1: "RAM", 2: "Flash ROM"}

    def __init__(self) -> None:
        self.signature = 'CHIP'
        self.total_length = 0x10
        self.type = 0
        self.bank_number = 0
        self.start_address = 0
        self.rom_size = 0
        self.data = bytes()

    def __str__(self):
        return f"<{self.signature}:{self.TYPE[self.type] if self.type in self.TYPE else self.type}:B{self.bank_number}:{hex(self.start_address)}:{hex(self.rom_size)}>"


class Crt:
    TYPE = {0: "Normal cartridge", 1: "Action Replay", 2: "KCS Power Cartridge", 3: "Final Cartridge III",
            4: "Simons Basic",
            5: "Ocean type", 6: "Expert Cartridge", 7: "Fun Play, Power Play", 8: "Super Games", 9: "Atomic Power",
            10: "Epyx Fastload", 11: "Westermann Learning", 12: "Rex Utility", 13: "Final Cartridge I",
            14: "Magic Formel",
            15: "C64 Game System, System 3", 16: "WarpSpeed", 17: "Dinamic", 18: "Zaxxon, Super Zaxxon (SEGA)",
            19: "Magic Desk, Domark, HES Australia", 20: "Super Snapshot 5", 21: "Comal-80", 22: "Structured Basic",
            23: "Ross", 24: "Dela EP64", 25: "Dela EP7x8", 26: "Dela EP256", 27: "Rex EP256", 32: "EasyFlash"}
    chips: list[Chip]

    def __init__(self):
        self.signature = 'C64 CARTRIDGE'
        self.header_length = 64
        self.version_hi = 1
        self.version_low = 0
        self.type = 32
        self.extrom = True
        self.game = False
        self.name = 'EasyFlash'
        self.chips = []

    def __str__(self):
        return f"<{self.signature}:{self.version_hi}.{self.version_low}:{self.TYPE[self.type] if self.type in self.TYPE else self.type}:{'EXROM' if self.extrom else ''}{'GAME' if self.game else ''}:{self.name}>"

    @staticmethod
    def from_bytes(data: bytes) -> 'Crt':
        crt = Crt()
        crt.signature = data[:0x10].decode('ASCII').rstrip(' \x00')
        crt.header_length = int.from_bytes(data[0x10:0x14], "big")
        crt.version_hi = data[0x14]
        crt.version_low = data[0x15]
        crt.type = int.from_bytes(data[0x16:0x18], "big")
        crt.exrom = data[0x18] == 1
        crt.game = data[0x19] == 1
        crt.name = data[0x20:0x40].decode('ASCII').rstrip(' \x00')
        i = 0x40
        while i < len(data):
            chip = Chip()
            chip.signature = data[i:i + 0x04].decode('ASCII')
            chip.total_length = int.from_bytes(data[i + 0x04:i + 0x08], "big")
            chip.type = int.from_bytes(data[i + 0x8:i + 0x0a], "big")
            chip.bank_number = int.from_bytes(data[i + 0xa:i + 0xc], "big")
            chip.start_address = int.from_bytes(data[i + 0xc:i + 0xe], "big")
            chip.rom_size = int.from_bytes(data[i + 0xe:i + 0x10], "big")
            chip.data = data[i + 0x10:i + 0x10 + chip.rom_size]
            crt.chips.append(chip)
            i += chip.total_length
        return crt

    def get_raw(self) -> bytes:
        result = bytes()
        for chip in self.chips:
            result += chip.data
        return result


class EasyFile:
    def __init__(self, file_name: str = ""):
        self.file_path = file_name
        self.name = os.path.splitext(os.path.basename(file_name))[0]
        self.type = 0x1f
        self.bank = 0
        self.offset = 0

        if not file_name:
            self.data = bytes()
            self.size = 0
        else:
            with open(file_name, "rb") as f:
                self.data = f.read()
                self.size = len(self.data)

    def __repr__(self):
        e = self.offset + self.size
        return f"{self.name}[{self.bank}:{hex(self.offset)}-{self.bank + e // 0x4000}:{hex(e % 0x4000)}=>{self.bank * 0x4000 + self.offset}]"


class EasyFS(QAbstractTableModel):
    files: list[EasyFile]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.boot = bytes()
        self.easyapi = bytes()
        self.startup = bytes()
        self.files = []
        self.modified = False

    def clear(self) -> None:
        self.boot = bytes()
        self.easyapi = bytes()
        self.startup = bytes()
        self.files = []
        self.modified = False

    def add_file(self, file: EasyFile) -> None:
        self.files.append(file)
        self.layoutChanged.emit()

    def from_bytes(self, data: bytes) -> None:
        self.boot = data[:0x2000]
        self.easyapi = data[0x2000 + 0x1800:0x2000 + 0x1b00]
        self.startup = data[0x2000 + 0x1b00:0x2000 + 0x2000]
        self.files = []
        for i in range(255):
            p = 0x2000 + i * 24
            file = EasyFile()
            file.type = data[p + 16]
            if file.type & 0x1f == 0x1f:
                break

            file.name = data[p:p + 16].rstrip(b'\0x00').decode('petscii_c64en_lc')
            file.bank = data[p + 17]
            file.offset = int.from_bytes(data[p + 19:p + 21], "little")
            file.size = int.from_bytes(data[p + 21:p + 24], "little")
            file_start = file.bank * 0x4000 + file.offset
            file.data = data[file_start:file_start + file.size]
            self.files.append(file)
        self.modified = False
        self.layoutChanged.emit()

    def export(self, export_path: str) -> None:
        with open(path.join(export_path, "boot.prg"), "wb") as fo:
            fo.write(0x8000.to_bytes(2, "little"))
            fo.write(self.boot)

        with open(path.join(export_path, "easyapi.prg"), "wb") as fo:
            fo.write(0xb800.to_bytes(2, "little"))
            fo.write(self.easyapi)

        with open(path.join(export_path, "startup.prg"), "wb") as fo:
            fo.write(0xfb00.to_bytes(2, "little"))
            fo.write(self.startup)

        for file in self.files:
            with open(path.join(export_path, f"{file.name}.prg"), "wb") as fo:
                fo.write(file.data)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            file = self.files[index.row()]
            if index.column() == 0:
                return file.name
            if index.column() == 1:
                return file.size
            if index.column() == 2:
                return "PRG"
        if role == Qt.ItemDataRole.TextAlignmentRole and index.column() == 1:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None

    def setData(self, index: QModelIndex, value, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.EditRole:
            if value == "":
                QMessageBox.warning(self.parent(), "Error", "Empty filename!")
                return False
            if len(value) > 16:
                QMessageBox.warning(self.parent(), "Error", "Too long filename!")
                return False
            self.files[index.row()].name = value
            self.modified = True
            return True
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if index.column() == 0:
            return super().flags(index) | Qt.ItemFlag.ItemIsEditable
        return super().flags(index)

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return "File name"
            if section == 1:
                return "File size"
            if section == 2:
                return "File type"
        return None

    def columnCount(self, parent=QModelIndex()) -> int:
        return 3

    def rowCount(self, parent=QModelIndex) -> int:
        return len(self.files)
