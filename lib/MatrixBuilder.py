
class MatrixBuilder:
    def __init__(self, size) -> None:
        self._max_index = size - 1
        self._row = [None for _ in range(size)]
        self._col = [None for _ in range(size)]
        self._val = [None for _ in range(size)]
        self._index = 0

    def stamp(self, row, column, value):
        self._row[self._index] = row
        self._col[self._index] = column
        self._val[self._index] = value
        self._index += 1
        
    def clear(self, retain_idx = 0):
        self._index = retain_idx

    def to_matrix(self):
        if self._max_index != self._index:
            raise Exception("Solver was not fully utilized. Garbage data remains")
        pass