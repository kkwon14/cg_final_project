"""Three functions to perform global alignment.

All functions take two strings, x, y, and a cost function as parameters and
output the alignment for x and y and the score.

Three types:
    DP learned in class
    Hirschberg s Algorithm
    Method of Three Russians

"""
import itertools
from itertools import product
import numpy as np
from numpy import zeros
import pathlib

def get_cost(xc, yc):
    """Cost function - 0 for a match, 1 for a mismatch, 2 for an gap."""
    if xc == yc:
        return 0 # match
    if xc == '-' or yc == '-':
        return 2 # gap
    return 1 # mismatch

def dp(x, y, s):
    """DP from class."""
    # first part of code taken from lecture notes
    D = zeros((len(x)+1, len(y)+1), dtype=int)
    for j in range(1, len(y)+1):
        D[0, j] = D[0, j-1] + s('-', y[j-1])
    for i in range(1, len(x)+1):
        D[i, 0] = D[i-1, 0] + s(x[i-1], '-')
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            D[i, j] = min(D[i-1, j-1] + s(x[i-1], y[j-1]), # diagonal
                          D[i-1, j  ] + s(x[i-1], '-'),    # vertical
                          D[i  , j-1] + s('-',    y[j-1])) # horizontal

    score = D[len(x), len(y)]

    # Traceback
    xa = ''
    ya = ''

    i = len(x)
    j = len(y)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i, j] == D[i-1, j-1] + s(x[i-1], y[j-1]):
            # diagonal
            i -= 1
            j -= 1
            xa = x[i] + xa
            ya = y[j] + ya
        elif i > 0 and D[i, j] == D[i-1, j] + s(x[i-1], '-'):
            # vertical
            i -= 1
            xa = x[i] + xa
            ya = '-' + ya
        else: # j > 0 and D[i, j] == D[i, j-1] + s('-', y[j-1])
            # horizontal
            j -= 1
            xa = '-' + xa
            ya = y[j-1] + ya
    return xa, ya, score

def hirschberg_split(x, y, s):
    """Finds the last row of the dp matrix using linear space."""
    # initialize first row in the same way as normal dp
    prev_row = [0] * (len(y) + 1)
    for j in range(1, len(y)+1):
        prev_row[j] = prev_row[j-1] + s('-', y[j-1])

    for i in range(1, len(x)+1):
        curr_row = [0] * (len(y) + 1)
        for j in range(len(y)+1):
            if j == 0:
                # only choice is vertical
                curr_row[j] = prev_row[j] + s(x[i-1], '-')
            else:
                curr_row[j] = min(prev_row[j-1] + s(x[i-1], y[j-1]), # diagonal
                                  prev_row[j  ] + s(x[i-1], '-'),    # vertical
                                  curr_row[j-1] + s('-',    y[j-1])) # horizontal
        prev_row = curr_row
    return curr_row

def hirschberg(x, y, s):
    # setting the shorter string as x
    if (len(y) > len(x)):
        x, y = y, x

    # base case:
    if len(x) <= 1 or len(y) <= 1:
        return dp(x, y, s)
    # split
    split = len(x) // 2

    top = hirschberg_split(x[:split], y, s)
    bot = hirschberg_split(x[split:][::-1], y[::-1], s)
    bot.reverse()

    # find the min index
    sum = [top[i] + bot[i] for i in range(len(top))]
    max_index = sum.index(min(sum))
    
    # recurse on the relevant sections - that is, split the matrix into 4
    # sections using split to separate top from bottom and max_index to
    # separate left and right, then take the top left and bottom right.
    top_left = hirschberg(x[:split], y[:max_index], s)
    bot_right = hirschberg(x[split:], y[max_index:], s)

    # sum up results from the top left and bottom right and return
    return [top_left[i] + bot_right[i] for i in range(len(top_left))]



#Takes an input block size, and stores the output to all possible row and column offset vectors of size t
#Offset vectors store elements {-1,0,1}, which represent D(i,j) - D(i-1,j) or D(i,j) - D(i,j-1)
def preprocessing(t):
    """ Input block size t.
        Returns dictionary.
        Keys: all possible genome strings of length t, offset vectors of length t
        Values: the offset vectors corresponding to the bottom row and rightmost column of the tblock."""
    F = {}
    possibleOffsets = generateOffsets(t)
    strings = []
    for value in generate_strings(t):
        strings.append(value)
    
    #print(strings)
    #loop through all possible string pairings and offset vectors
    for s1 in strings:
        for s2 in strings:
            for i in range(len(possibleOffsets)):
                for j in range(len(possibleOffsets)):
                    newKey = (tuple(possibleOffsets[i]), tuple(possibleOffsets[j]), s1, s2)
                    
                    #Compute block edit distance
                    tblockfull =  edDistOffset(possibleOffsets[i], possibleOffsets[j], s1, s2)
                    
                    rowOffset, colOffset = tBlockToOffset(tblockfull)
                    
                    
                    newValue = (tuple(rowOffset), tuple(colOffset))
                    
                    F[newKey] = newValue
                    
    return F
                    

def generateOffsets(t):
    output = list(product(range(-1, 2), repeat=t))
    for i in range(len(output)):
        output[i] = list(output[i])
        #output[i].insert(0,0)
    return output;

def generate_strings(length):
    chars = "ACTG"
    for item in itertools.product(chars, repeat=length):
        yield "".join(item)
        
#here for comparison with edDistOffset. Shamelessly borrowed from Dr. Ben Langmead's Comp Genomics course.         
def edDistDp(x, y):
    """ Calculate edit distance between sequences x and y using
        matrix dynamic programming.  Return matrix. """
    D = zeros((len(x)+1, len(y)+1), dtype=int)
    D[0, 1:] = range(1, len(y)+1)
    D[1:, 0] = range(1, len(x)+1)
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            delt = 1 if x[i-1] != y[j-1] else 0
            D[i, j] = min(D[i-1, j-1]+delt, D[i-1, j]+1, D[i, j-1]+1)
    return D[len(x), len(y)]

#at any random t block with a 10 * 20 dp matrix
# D(5,10) = 
def edDistOffset(rowOffsets, colOffsets, s1, s2): #note does not calculate output in O(t) time, but in O(t^2) time
    """ Calculate edit distance with offset vectors {-1,0,1}.
        Given two strings (s1,s2) and precomputed offsets.
        len(s1) = len(s2) = len(rowOffsets) = len(colOffsets)
        Return edit distance matrix. """
    #print("len s1 %d len s2 %d len row %d len col %d" %(len(s1), len(s2), len(rowOffsets), len(colOffsets)))
    assert len(s1) == len(s2) == len(rowOffsets) == len(colOffsets)
    D = zeros((len(s1)+1, len(s2)+1), dtype=int)
    rowEditDist = [0] * len(rowOffsets)
    colEditDist = [0] * len(colOffsets)
    for k in range(1, len(rowOffsets)):
        rowEditDist[k] = rowOffsets[k] + rowEditDist[k-1]
        colEditDist[k] = colOffsets[k] + colEditDist[k-1]
    D[0, 1:] = rowEditDist
    D[1:, 0] = colEditDist
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            delt = 1 if s1[i-1] != s2[j-1] else 0
            D[i, j] = min(D[i-1, j-1]+delt, D[i-1, j]+1, D[i, j-1]+1)
    return D

def tBlockToOffset(D):
    """ Calculate offset vectors. 
        Given an DP edit distance 2D array.
        Return bottom row and rightmost column as offsets.
        D is a square matrix.
        from a tblock with edit distances. """
    N = len(D)
    M = len(D[0])
    
    row = D[N-1, 1:]
    col = D[1:, M-1]
    
    newRow = np.copy(row)
    newCol = np.copy(col)
    # 4 5 6 7 8
    # 0 1 1 1 1
    
    # 4 4 5 5 6 7
    # 0 0 1 0 1 1
    
    for k in range(1, len(row)):
        newRow[k] = row[k] - row[k-1]
        newCol[k] = col[k] - col[k-1]
        
        
    newRow[0] = 0
    newCol[0] = 0

    return newRow, newCol

def create_preprocess_file(t):
    base_path = pathlib.Path(__file__).parent
    filename = f't_{str(t)}_preprocessed.json'
    filepath = (base_path / 'four_russians_preprocessed' / filename).resolve()

    preprocessed = preprocessing(t)

    with open(filepath, 'w+') as fout:
        fout.write(str(preprocessed))

def read_preprocess_file(t):
    base_path = pathlib.Path(__file__).parent
    filename = f't_{str(t)}_preprocessed.json'
    filepath = (base_path / 'four_russians_preprocessed' / filename).resolve()
    if not filepath.is_file():
        raise ValueError('Preprocess file does not exist - must run preprocessing first')

    with open(filepath, 'r') as fin:
        preprocessed_string = fin.read()
    preprocessed = eval(preprocessed_string)
    return preprocessed

def four_russians(s1, s2, t):
    if(t == 1):
        return -1;
    n = len(s1)
    m = len(s2)
    D = zeros((m+1,n+1))
    F = read_preprocess_file(t)
    
    D[0,1:] = range(1, n+1)
    D[1:,0] = range(1, m+1)
    result = runFour(s1, s2, t, D, F)
    return result;

def runFour(s1, s2, t, D, F):
    n = len(s1)
    m = len(s2)
    
    i = 0
    j = 0
    while i + t <= n:
        while j + t <= m:
            if(i == 0 and j == 0):
                for k in range(1, t):
                    for l in range(1, t):
                        delt = 1 if s1[k-1] != s2[l-1] else 0
                        D[k, l] = min(D[k-1, l-1]+delt, D[k-1, l]+1, D[k, l-1]+1)
                j = j + t - 1
                continue;
            
            Aoffset, Boffset = LookUpF(i, j, t, D, s1, s2, F) #returns offset vector

            for k in range(1, len(Aoffset)):
                D[i+t, j+k] = D[i+t, j+k-1] + Aoffset[k]
            for k in range(1, len(Boffset)):
                D[i+k, j + t] = D[i+k-1, j + t] + Boffset[k]
            j = j + t - 1 #overlap
        i = i + t - 1 #overlap
    
    squareEditDist = D[n,m]
    
    s1LeftOver = ""
    s2LeftOver = ""
    
    if not i >= n-1:
        s1LeftOver = s1[i+1:n]
            
    if not j >= j-1:
        s2LeftOver = s2[j+1:m]
        
    return edDistDp(s1LeftOver, s2LeftOver) + squareEditDist
        
def LookUpF(i, j, t, D, s1, s2, F):
    A = D[i, j:j + t]
    B = D[i:i + t, j]
    
    A_copy = np.copy(A)
    B_copy = np.copy(B)
    for k in range(1, len(A)):
        A_copy[k] = A[k] - A[k-1]
        B_copy[k] = B[k] - B[k-1]
    
    A_copy[0] = 0
    B_copy[0] = 0
    C = s1[i: i + t]
    E = s2[j: j + t]
    print(F)
    result = F[(tuple(np.array(A_copy.astype(int))), tuple(np.array(B_copy.astype(int))), C, E)] # result = (Aprime, Bprime)
    
    Bprime = result[0] #row
    Aprime = result[1] #col
    return Aprime, Bprime
