from dataclasses import dataclass

TABLE_EN = [
    ["@", "-", "_", "/", "1"],
    ["a", "b", "c", "A", "B", "C", "2"],
    ["d", "e", "f", "D", "E", "F", "3"],
    ["g", "h", "i", "G", "H", "I", "4"],
    ["j", "k", "l", "J", "K", "L", "5"],
    ["m", "n", "o", "M", "N", "O", "6"],
    ["p", "q", "r", "s", "P", "Q", "R", "S", "7"],
    ["t", "u", "v", "T", "U", "V", "8"],
    ["w", "x", "y", "z", "W", "X", "Y", "Z", "9"],
    ["■"],
    ["'", '"', ":", ";"],
    [".", ",", "?", "!"],
]

TABLE_JP = [
    ["あ", "い", "う", "え", "お", "ぁ", "ぃ", "ぅ", "ぇ", "ぉ", "ゔ"],
    ["か", "き", "く", "け", "こ", "が", "ぎ", "ぐ", "げ", "ご"],
    ["さ", "し", "す", "せ", "そ", "ざ", "じ", "ず", "ぜ", "ぞ"],
    ["た", "ち", "つ", "て", "と", "っ", "だ", "ぢ", "づ", "で", "ど"],
    ["な", "に", "ぬ", "ね", "の"],
    [
        "は",
        "ひ",
        "ふ",
        "へ",
        "ほ",
        "ば",
        "び",
        "ぶ",
        "べ",
        "ぼ",
        "ぱ",
        "ぴ",
        "ぷ",
        "ぺ",
        "ぽ",
    ],
    ["ま", "み", "む", "め", "も"],
    ["や", "ゆ", "よ", "ゃ", "ゅ", "ょ"],
    ["ら", "り", "る", "れ", "ろ"],
    ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    ["わ", "を", "ん", "ー"],
    ["、", "。", ".", "？", "！"],
]


@dataclass
class InputTable:
    table: list[list[str]]

    def char(self, row: int, col: int):
        if len(self.table) <= row or len(self.table[row]) <= col:
            raise IndexError("no character")
        return self.table[row][col]

    def __init__(self, table):
        self.table = table
        self.rows = len(table)
        self.cols = tuple(len(t) for t in table)


@dataclass
class InputTableGroup:
    tables: list[InputTable]

    def char(self, mode: int, row: int, col: int):
        if len(self.tables) <= mode:
            raise IndexError("no mode")
        return self.tables[mode].char(row, col)

    def table(self, mode: int):
        if len(self.tables) <= mode:
            raise IndexError("no mode")
        return self.tables[mode]
