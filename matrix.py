from sympy import Symbol
from random import randint

scalars = [int,float,Symbol]

class Matrix:
    def __init__(self,arr):
        if not all([len(row)==len(arr[0]) for row in arr]):
            raise TypeError
        self._values = arr
        self.dim = (len(self._values),len(self._values[0]))

    def T(self):
        return Matrix([list(col) for col in zip(*self._values)])
    
    def __add__(self,a):
        if type(a) != Matrix:
            raise Exception
        elif self.dim != a.dim:
            raise Exception
        return Matrix([[a+b for a,b in zip(rowa,rowb)] for rowa,rowb in zip(self._values,a._values)])


    def __sub__(self,a):
        return self+(-1)*a

    def __rmul__(self,a):
        if type(a) not in scalars:
            raise Exception
        return Matrix([[a*element for element in row] for row in self._values])

    def __mul__(self,a):
        if type(a) in scalars:
            return self.__rmul__(a)
        elif type(a) == Matrix:
            i,j = self.dim
            m,n = a.dim
            if not j==m:
                raise Exception
            return Matrix([[sum([a*b for a,b in zip(a_i,b_j)]) for b_j in a.T()._values] for a_i in self._values])            
        else:
            raise Exception

    def __repr__(self):
        return f'Matrix {self.dim}'

    def __str__(self):
        tab = '\t'
        return str('\n'.join([f'[{tab.join([str(n) for n in row])}]' for row in self._values]))

    def __eq__(self,a):
        if type(a) != Matrix:
            return False
        return self._values == a._values



class Dummy():
    def __new__(self,dim:tuple):
        rows,cols = dim
        return Matrix([[randint(-100,100) for j in range(cols)] for i in range(rows)])
