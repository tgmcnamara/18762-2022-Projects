from scipy.sparse import csc_matrix

class MatrixBuilder:
    def __init__(self) -> None:
        self._row = []
        self._col = []
        self._val = []
        self._index = 0
        self._max_index = 0

    def stamp(self, row, column, value):
        if self._index == self._max_index:
            self._row.append(row)
            self._col.append(column)
            self._val.append(value)
            self._index += 1
            self._max_index += 1
            return

        self._row[self._index] = row
        self._col[self._index] = column
        self._val[self._index] = value
        self._index += 1
        
    def clear(self, retain_idx = 0):
        self._index = retain_idx

    def to_matrix(self):
        if self._max_index != self._index:
            raise Exception("Solver was not fully utilized. Garbage data remains")

        return csc_matrix((self._val, (self._row, self._col)))

    def get_usage(self):
        return self._index