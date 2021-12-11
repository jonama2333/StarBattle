from math import *

class Board():

    #To simplify the code, we assume user will pass the dimension of board (m rows and n cols), and number of total shapes (k shapes)
    def __init__(self, instance_str,m,n,k,star):
        self.row = m
        self.col = n
        self.shape = k
        self.star = star
        
        self.shapes = {i+1:[] for i in range(k)}
        a = [[] for i in range(k)]
        for i in range(m):
            substring = ''
            for j in range(n):
                substring += instance_str[i*n+j]
                index = self.str_to_int(instance_str[i*n+j])
                a[index-1].append((i,j))
            print(f'{substring}')
        a.sort(key=lambda x: len(x))
        for i in self.shapes:
            self.shapes[i] = a[i-1]
        print(self.shapes)
        return

    def str_to_int(self, letter):
        if letter.isdigit():
            return int(letter)
        else:
            return 10+(ord(letter)-ord('A'))

class Decision():
    
    def __init__(self, board: Board):
        self.decisions = []
        self.row_count = [0] * board.row
        self.col_count = [0] * board.col
        #self.shape_count = {}      looks like we don't need this now
        
    def move(self, i, j):
        self.decisions.append((i,j))
        self.row_count[i] += 1
        self.col_count[j] += 1

    def score(self):
        return len(self.decisions), self.decisions
    
    def valid_point(self, board: Board):
        star = board.star
        shape = len(self.decisions) // star + 1
        #print(f'{shape}  {self.decisions}')
        #possible = board.shapes[shape]
        possible = board.shapes.get(shape,[])
        result = [] 
        
        for i,j in possible:
            valid = True
            if self.row_count[i] >= star or self.col_count[j] >= star:
                continue
            for x,y in self.decisions:
                # if repeated, TODO: could be simplified
                if abs(i-x)==0 and abs(j-y)==0:
                    valid = False
                    break

                elif abs(i-x)==1 and abs(j-y)==1:
                    valid = False
                    break
                elif abs(i-x) + abs(j-y) == 1:
                    valid = False
                    break
            if valid:
                result.append((i,j))
        
        return result
            