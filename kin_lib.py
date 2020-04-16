import math

""" 
    _.Matrix(list): Create matrix
    _.Matrix(int):  Create identity matrix
    add:            Add matrices
    sub:            Sub matrices
    mulElem:        Elementwise matrix multiplication
    mulFactor:      Multiply matrix by factor
    mul:            Multiply matrices
    invert:         Invert matrix
    solve:          Solve matrix
    print:          Print matrix
    printSize:      Print size of matrix
    inverse:        Find inverse of matrix

-    det:            Find determinant
-    eigVal:         Find eigen value
-    eigVec:         Find eigen vector
 """

class Error:
    @staticmethod
    def colRowError():
        return print("col/row error")

    @staticmethod
    def checkColRow(a, b):
        if(a.row != b.row or a.column != b.column):
            return 1
        return 0

    @staticmethod
    def intError():
        return print("must multiply by integer")

    @staticmethod
    def checkInteger(num):
        if(not isinstance(num, int)):
            return 1
        return 0

class Matrix:
    def __init__(self, _elem):
        if(isinstance(_elem, list)):
            self.row = len(_elem)
            self.column = len(_elem[0])
            self.mat = _elem
        elif(isinstance(_elem, int)):
            self.row = _elem
            self.column = _elem
            count = 0
            self.mat = []
            for m in range(_elem):
                temp_list = []
                for n in range(_elem):
                    if(n == count):
                        temp_list.append(1)
                    else:
                        temp_list.append(0)
                count += 1
                self.mat.append(temp_list)

    def invert(self):
        temp_mat = list()
        for col in range(self.column):
            temp_row = list()
            for row in range(self.row):
                elem = self.mat[row][col]
                
                temp_row.append(elem)
            temp_mat.append(temp_row)
        self.mat = temp_mat
        self.row, self.column = self.column, self.row

    def det(self):

        return

    def inverse(self):
        _mat = Matrix(self.row)
        self.__rowEch(_mat)
        for i in range(self.row - 1):
            for n in range(self.row-i-1):
                index = self.row-i-n-2
                pivot = self.mat[self.row-i-1][self.row-i-1]
                comp_num = self.mat[index][self.row-i-1]
                if(comp_num != 0):
                    factor = abs(comp_num / pivot)
                    if((pivot > 0 and comp_num < 0) or (pivot < 0 and comp_num > 0)):
                        factor *= -1
                    self.__reduceRow(index, self.row-i-1, factor)
                    _mat.__reduceRow(index, self.row-i-1, factor)
        for i in range(self.row):
            for j in range(self.row):
                divider = self.mat[i][i]
                _mat.mat[i][j] /= divider
        self.mat = _mat.mat

    def solve(self, _mat):
        if(_mat.column > 1):
            return print("can only solve for vector not matrix")
        self.__rowEch(_mat)
        for x in range(self.row):
            if(x > 0):
                sum = 0
                for n in range(x):
                    s_num = self.mat[self.row-x-1][self.column-n-1]
                    m_num = _mat.mat[_mat.row-n-1][0]
                    sum += s_num * m_num
                _mat.mat[_mat.row-x-1][0] -= sum
            _mat.mat[_mat.row-x-1][0] /= self.mat[self.row-x-1][self.row-x-1]

    def __rowEch(self, _mat):
        for i in range(self.row - 1):
            self.__checkFlip(_mat, i)
            for n in range(self.row-i-1):
                index = i+n+1
                num = self.mat[i][i]
                comp_num = self.mat[index][i]
                if(comp_num != 0):
                    factor = abs(comp_num / num)
                    if((num > 0 and comp_num < 0) or (num < 0 and comp_num > 0)):
                        factor *= -1
                    self.__reduceRow(index, i, factor)
                    _mat.__reduceRow(index, i, factor)

    def __reduceRow(self, n_row, row, factor):
        for i in range(self.column):
            self.mat[n_row][i] -= factor * self.mat[row][i]

    def __checkFlip(self, _mat, n):
        max_index = n
        n_val = self.mat[n][n]
        for x in range(self.row-n-1):
            index = x+n+1
            comp_val = self.mat[index][n]
            if(abs(comp_val) > abs(n_val)):
                max_index = index
                n_val = comp_val
        if(n != max_index):
            self.__flip(n, max_index)
            _mat.__flip(n, max_index)

    def __flip(self, n, _max):
        self.mat[n], self.mat[_max] = self.mat[_max], self.mat[n]

    def add(self, _mat):
        if(Error.checkColRow(self, _mat)):
            return Error.colRowError()

        for row in range(self.row):
            for col in range(self.column):
                self.mat[row][col] += _mat.mat[row][col]

    def sub(self, _mat):
        if(Error.checkColRow(self, _mat)):
            return Error.colRowError()

        for row in range(self.row):
            for col in range(self.column):
                self.mat[row][col] -= _mat.mat[row][col]

    def mulElem(self, _mat):
        if(Error.checkColRow(self, _mat)):
            return Error.colRowError()

        for row in range(self.row):
            for col in range(self.column):
                self.mat[row][col] *= _mat.mat[row][col]

    def mulFactor(self, num):
        if(Error.checkInteger(num)):
            return Error.intError()

        for row in range(self.row):
            for col in range(self.column):
                self.mat[row][col] *= num

    def mul(self, _mat):
        #check for error
        
        temp_mat = []
        for n in range(self.row):
            temp_line = []
            for m in range(_mat.column):
                temp_num = 0
                for x in range(_mat.row):
                    temp_num += self.mat[n][x] * _mat.mat[x][m]
                temp_line.append(temp_num)
            temp_mat.append(temp_line)
        self.mat = temp_mat
        self.column = _mat.column

    def printSize(self):
        print(self.row, self.column)

    def print(self, decimals = 0):
        #Get length of longest number in matrix
        len = 0
        for row in range(self.row):
            for col in range(self.column):
                n = self.mat[row][col]
                if n > 0:
                    digits = int(math.log10(n))+1
                elif n == 0:
                    digits = 1
                else:
                    digits = int(math.log10(-n)) + 2
                if(digits > len):
                    len = digits

        for row in range(self.row):
            for col in range(self.column):
                element = self.mat[row][col]
                print('% *.*f' % (len+decimals+2, decimals, element) + "  ", end='')
            print(end='\n\n')
