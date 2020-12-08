"""Three functions to perform global alignment.

All functions take two strings, x, y, and a cost function as parameters and
output the alignment for x and y and the score.

Three types:
    DP learned in class
    Hirschberg s Algorithm
    Method of Three Russians

"""
from numpy import zeros

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
