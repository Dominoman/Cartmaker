from os import path
from typing import List, Any


class Chip:
    def __init__(self) -> None:
        self.signature = 'CHIP'
        self.total_length = 0x10
        self.type = 0
        self.bank_number = 0
        self.start_address = 0
        self.rom_size = 0
        self.data = bytes()


class Crt:
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
    def __init__(self):
        self.name = ""
        self.type = 0x1f
        self.bank = 0
        self.offset = 0
        self.size = 0
        self.data = bytes()

    def __repr__(self):
        e = self.offset + self.size
        return f"{self.name}[{self.bank}:{hex(self.offset)}-{self.bank + e // 0x4000}:{hex(e % 0x4000)}=>{self.bank * 0x4000 + self.offset}]"


class EasyFS:
    files: list[EasyFile]

    def __init__(self) -> None:
        self.boot = bytes()
        self.easyapi = bytes()
        self.startup = bytes()
        self.files = []

    @staticmethod
    def from_bytes(data: bytes) -> 'EasyFS':
        fs = EasyFS()
        fs.boot = data[:0x2000]
        fs.easyapi = data[0x2000 + 0x1800:0x2000 + 0x1b00]
        fs.startup = data[0x2000 + 0x1b00:0x2000 + 0x2000]
        fs.files = []
        for i in range(255):
            p = 0x2000 + i * 24
            file = EasyFile()
            file.type = data[p + 16]
            if file.type in [0x1f, 0xff]:
                break

            file.name = data[p:p + 16].decode('ASCII').rstrip(' \0x00')
            file.bank = data[p + 17]
            file.offset = int.from_bytes(data[p + 19:p + 21], "little")
            file.size = int.from_bytes(data[p + 21:p + 24], "little")
            file_start = file.bank * 0x4000 + file.offset
            file.data = data[file_start:file_start + file.size]
            fs.files.append(file)
        return fs

    def export(self, export_path: str) -> None:
        with open(path.join(export_path, "boot.prg"), "wb") as fo:
            fo.write(0x8000.to_bytes(2, "little"))
            fo.write(self.boot)

        with open(path.join(export_path, "easyapi.prg"), "wb") as fo:
            fo.write(0xb800.to_bytes(2, "little"))
            fo.write(self.easyapi)

        with open(path.join(export_path, "startup.prg"), "wb") as fo:
            fo.write(0xbb00.to_bytes(2, "little"))
            fo.write(self.startup)

        for file in self.files:
            with open(path.join(export_path, f"{file.name}.prg"), "wb") as fo:
                fo.write(file.data)
