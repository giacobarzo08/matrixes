class MatrixDimensionError(Exception): pass

class Matrix:
    def __init__(self,
                  x_dimension: int | None = None,
                  y_dimension: int | None = None) -> None:
        if ((x_dimension is not None) and (not isinstance(x_dimension, int))) or ((y_dimension is not None) and (not isinstance(y_dimension, int))):
            raise ValueError("The dimension of the matrix, if statics, ought to be int numbers")
        
        self._x = x_dimension
        self._y = y_dimension
        self._main_array = []
    
    @property
    def main_array(self):
        return self._main_array
    
    @property
    def y(self):
        return self._y
    
    @property
    def x(self):
        return self._x

    def populate(self, *arrays: list) -> None:
        if not all(len(a) == len(arrays[0]) for a in arrays):
            raise ValueError("A matrix ought to have the same lenght for all the arrays.")
        
        if self.y is not None:
            if len(arrays) != self.y:
                raise ValueError("You have selected a static value for y_dimension, but the arrays you are insered are not compatible")
        else:
            self._y = len(arrays)
        
        if self.x is not None:
            if len(arrays[0]) != self.x:
                raise ValueError("You have selected a static value for x_dimension, but the arrays you are insered are not compatible")
        else:
            self._x = len(arrays[0])
        
        self._main_array = arrays
    
    def transpose(self):
        inverted = []
        for i in range(len(self.main_array[0])):
            row = []
            for j in self.main_array:
                row.append(j[i])
            inverted.append(row)
        
        self._x = None
        self._y = None
        self.populate(*inverted)
    
    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError(f"You need to sum a matrix to an other one, not with {type(other)}")
        if (self.x != other.x) or (self.y != other.y):
            raise MatrixDimensionError(f"You need to 2 matrix with the same dimension to sum them, but you have {self.y}x{self.x} and {other.y}x{other.x}")
        
        new_m = []
        for i, j in zip(self.main_array, other.main_array):
            new_array = []
            for v in range(len(i)):
                new_array.append(i[v] + j[v])
            new_m.append(new_array)

        ret = Matrix()
        ret.populate(*new_m)
        return ret
    
    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError(f"You need to sum a matrix to an other one, not with {type(other)}")
        if self.x != other.y:
            raise MatrixDimensionError(f"You need to 2 matrix that the x-dimension of the first is the same of the y-dimension o fthe second, "\
                                       f"but you have {self.y}x{self.x} and {other.y}x{other.x}")
        
        # AI generated
        result = [[0 for _ in range(other.x)] for _ in range(self.y)]
        for i in range(self.y):
            for j in range(other.x):
                for k in range(self.x):
                    result[i][j] += self.main_array[i][k] * other.main_array[k][j]
        # --

        ret = Matrix()
        ret.populate(*result)
        return ret

    def __repr__(self) -> str:
        ret = f'Matrice {self.y}x{self.x}:\n'
        ret += "\n".join(str(row) for row in self.main_array)
        return ret
    
    def __str__(self) -> str:
        ret = ''
        for array in self.main_array:
            for v in array:
                ret += f'{v}\t'
            ret += '\n'
        return ret
    
    def __pow__(self, other):
        if self.x != self.y:
            raise MatrixDimensionError(f"It is possible di pow only square matrix, not {self.y}x{self.x}")
        act = self
        for i in range(other - 1):
            act*=self
        return act

if __name__=="__main__":
    a = Matrix()
    a.populate([1, 2], [3, 4])
    b = Matrix()
    b.populate([2, 1], [-1, 3], [0, 4])

    print(repr(a**2))