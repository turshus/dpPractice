import random
import re
from typing import Sized
import numpy as np

#RETURNS: Boolean
#TAKES: a target string, keywords
def problemOneRecursive(a_targetStr, a_keywords):
    #Base cases
    if(len(a_targetStr) == 0):
        return True
    if len(a_keywords) == 0: 
        return False

    #Break problem down
    isInTargetStr = False
    for i in range(0, len(a_keywords)):
        tempVar = a_keywords[i]
        if not len(a_targetStr) < len(a_keywords[i]): #This prevents checking a case where the target string is smaller than the keyword
            if a_targetStr[0 : len(a_keywords[i])] == a_keywords[i]:
                 isInTargetStr = problemOneRecursive(a_targetStr[len(a_keywords[i]) : len(a_targetStr)], a_keywords)
    
    return isInTargetStr

def problemOneDP(a_targetStr, a_keywords):
    #allocate memory ([a_targetStr][a_keywords]
    dpSolution = [[False] * (len(a_keywords) + 1) for i in range(0, len(a_targetStr) + 1)]

    #fill in the base cases
    for i in range(0, len(a_keywords) + 1):
        dpSolution[0][i] = True

    #loop through the array and fill in each case
    for i in range(0, len(a_keywords)):
        for j in range(0, len(a_keywords)):
            if not len(a_targetStr) < len(a_keywords[j]):
                if a_keywords[j] == a_targetStr[0 : len(a_keywords[j])]:
                    a_targetStr = a_targetStr[len(a_keywords[j]) : len(a_targetStr)]
            if len(a_targetStr) == 0:
                dpSolution[len(a_targetStr)][len(a_keywords)] = True
    return dpSolution[len(a_targetStr)][len(a_keywords)]

#RETURNS: 2d array
#TAKES: moves, current x, y, and z coordinates
g_visitedCubes = [[]]
def problemTwoRecursive(a_moves, a_x, a_y, a_z, a_width, a_height, a_depth):
    xx= 0
    #Base Cases
    if (a_x >= a_width or a_x < 0
        or a_y >= a_height or a_y < 0
        or a_z >= a_depth or a_z < 0):
        return []
    if g_visitedCubes.__contains__((a_x, a_y, a_z)):
        return []
    
    g_visitedCubes.append((a_x, a_y, a_z))

    l_visitedCubes = []
    for i in range(0, len(a_moves)):
        temp = problemTwoRecursive(a_moves, a_x + a_moves[i][0], a_y + a_moves[i][1], a_z + a_moves[i][2], a_width, a_height, a_depth)
        if not temp == []:
            #loop through and add values
            for j in range(0, len(temp)):
                l_visitedCubes.append(temp[j])
        l_visitedCubes.append((a_x, a_y, a_z))
    return l_visitedCubes

def problemTwoDP(a_moves, a_x, a_y, a_z, a_width, a_height, a_depth):
    #set up our dpSolution
    dpSolution = [[[False] * a_depth for i in range(0, a_height)] for j in range(0, a_width)]

    dpSolution[a_x - 1][a_y - 1][a_z - 1] = True

    for z in range(0, a_depth):
        for y in range(0, a_height):
            for x in range(0, a_width):
                for i in range(0, len(a_moves)):
                    if x == a_x + a_moves[i][0] and y == a_y + a_moves[i][1] and z == a_z + a_moves[i][2]:
                        dpSolution[x][y][z] = True
                    
    return dpSolution


#RETURNS: Boolean
#TAKES: Ksize, sizes array (All integers)
def problemThreeRecursive(a_kSize, a_sizes):
    #Base cases
    if a_kSize == 0:
        return True
    if len(a_sizes) < 0:
        return False

    l_val1 = False
    for i in range(0, len(a_sizes)):
        temp = a_sizes[i]
        if a_kSize >= a_sizes[i]:
            l_val1 = problemThreeRecursive(a_kSize - a_sizes[i], a_sizes)
        if l_val1:
            return l_val1

    return l_val1

#****This is the most beautiful code I've ever written****
def problemThreeDP(a_kSize, a_sizes):
    #allocate memory
    dpSolution = [-1] * (a_kSize + 1)

    #base cases
    dpSolution[0] = True

    for l_currKSize in range(1, a_kSize + 1):
        for i in range(0, len(a_sizes)):
            if l_currKSize >= a_sizes[i]: #if the size we're looking at is larger than ksize, don't bother and move on
                if l_currKSize % a_sizes[i] == 0: #if ksize % size is 0, we know we get a true
                    dpSolution[l_currKSize] = True
                    break
                else: #no match :/
                    #loop through and check if this value subtract any others is true
                    #the idea is that our knapsack minus any valid value should result in a valid look up of a previous solution
                    for j in range(0, len(a_sizes)):
                        if l_currKSize - a_sizes[j] >= 0:
                            if dpSolution[l_currKSize - a_sizes[j]] == True:
                                dpSolution[l_currKSize] = dpSolution[l_currKSize - a_sizes[j]]
                                break

        if dpSolution[l_currKSize] == -1:
            dpSolution[l_currKSize] = False
            
    
    return dpSolution[a_kSize]

#RETURNS: double
#TAKES: currRow, currCol
def problemFourRecursive(a_currRow, a_currCol, a_values):
    #base cases
    if len(a_values) < 1 or len(a_values[0]) < 1:
        return 0.0
    if (len(a_values[0]) - 1) - a_currCol == 0:
        return a_values[a_currRow][a_currCol]
    
    l_upVal = 0
    l_downVal = 0
    #go up if possible
    if a_currRow > 0 and (len(a_values[0]) - 1) - a_currCol > 0:
        l_upVal += problemFourRecursive(a_currRow - 1, a_currCol + 1, a_values)
    #now go down if possible
    if (len(a_values) - 1) - a_currRow > 0 and (len(a_values[0]) - 1) - a_currCol > 0:
        l_downVal += problemFourRecursive(a_currRow + 1, a_currCol + 1, a_values)
    return max(l_upVal, l_downVal) + a_values[a_currRow][a_currCol]

def problemFourDP(a_values):
    #allocate array [rows][columns]
    dpSolution = [[0] * len(a_values[0]) for i in range(0, len(a_values))]
    l_rows = len(a_values)
    l_columns = len(a_values[0])

    #fill the base cases
    for i in range(0, l_rows):
        dpSolution[i][0] = a_values[i][0]
    
    for i in range(1, l_columns):
        for j in range(0, l_rows):
            #check looking down
            l_downVal = 0
            if not j + 1 > l_rows - 1:
                l_downVal = dpSolution[j + 1][i - 1]
            l_downVal += a_values[j][i]

            #check looking up
            l_upVal = 0
            if (l_rows - 1) + j > (l_rows - 1):
                l_upVal = dpSolution[j - 1][i - 1]
            l_upVal += a_values[j][i]

            dpSolution[j][i] = max(l_upVal, l_downVal)
    #return the max of the last column
    l_maxVal = 0
    for i in range(0, l_rows):
        if dpSolution[i][l_columns - 1] > l_maxVal:
            l_maxVal = dpSolution[i][l_columns - 1] 

    return l_maxVal

#RETURNS: int
#TAKES: list of coin values
def problemFiveRecursive(a_coins):
    #base cases
    if len(a_coins) < 2:
        return 0
    if len(a_coins) == 2:
        return max(a_coins)
    
    #we are p1, naturally
    p1Front_p2Front = 0
    p1Back_p2Back = 0
    p1Front_p2Back = 0
    p1Back_p2Front = 0

    #take from the list
    p1Front_p2Front = problemFiveRecursive(a_coins[2:]) + a_coins[0]
    offBothEnds = problemFiveRecursive(a_coins[1 : len(a_coins) - 1])
    p1Back_p2Back = problemFiveRecursive(a_coins[0 : len(a_coins) - 2]) + a_coins[len(a_coins) - 1]

    p1Front_p2Back = offBothEnds + a_coins[0]
    p1Back_p2Front = offBothEnds + a_coins[len(a_coins) - 1]

    return max(p1Front_p2Front, p1Back_p2Back, p1Front_p2Back, p1Back_p2Front)
    
def problemFiveDP(a_coins):
    #n x n array
    dpSolution = np.zeros(shape = (len(a_coins), len(a_coins)))

    #base cases
    for i in range(0, len(a_coins)):
        for j in range(0, i):
            dpSolution[i, j] = 0
    
    for p in range(len(a_coins)):
        i = 0
        j = p
        for q in range(p, len(a_coins)):
            a = 0
            b = 0
            c = 0

            if i < len(a_coins) - 1 and j > 0:
                a = dpSolution[i + 1][j - 1]
            if i < len(a_coins) - 2:
                b = dpSolution[i + 2][j]
            if j > 1:
                c = dpSolution[i][j - 2]

            dpSolution[i][j] = max(a_coins[i] + min(a, b), a_coins[j] + min(a, c))
            i += 1
            j += 1
    return dpSolution[0][len(a_coins) - 1]          

    
#Main Program
if __name__ == "__main__":
    print('\n-- Starting Program --\n')

    while(True):
        #Get the user input for what problem they want to run
        print("\nType the number of the corresponding problem you would like to run or type 'q' to exit")
        problemChoice = input("('1', '2', '3', '4', '5', or 'q'): ").lower()
        
        if(problemChoice == '1'):
            print('\n -- Starting Problem 1 --\n')

            while True:
                print('Enter one of the following options...\n( P ) : Predictable Answer\n( R ) : Random\n( Q ) : Quit')
                p5Choice = input('Your choice: ').lower()

                if p5Choice == 'p':
                    #Custom Case
                    l_keywords = ['ar', 'gt', 'pee', 'zu', 'he', 'ck', 'ral', 'st', 'reeeeee']
                    print(f'Keywords: {l_keywords}')
                    print('Word: starheck')
                    print('Recursive: ', problemOneRecursive('starheck', l_keywords))
                    print(f'DP: {problemOneDP("starheck", l_keywords)}\n')

                elif p5Choice == 'r':
                    #random cases

                    #make the keywords list
                    l_keywords = []
                    for i in range(0, random.randint(10, 100)):
                        #make the keyword
                        l_keyword = "" 
                        for j in range(1, random.randint(2, 5)):
                            l_keyword += chr(random.randint(33, 126))
                        l_keywords.append(l_keyword)
                    
                    #make the target string
                    l_targetStr = ""
                    for i in range(1, random.randint(2, 10)):
                        l_targetStr += chr(random.randint(33, 126))
                    
                    print(f'Keywords: {l_keywords}')
                    print(f'Target String: {l_targetStr}')
                    print(f'Recursive: {problemOneRecursive(l_targetStr, l_keywords)}')
                    print(f'DP: {problemOneDP(l_targetStr, l_keywords)}\n')
                elif p5Choice == 'q':
                    break
                else:
                    print("\n Sorry, that didn't make sense.  Enter either a 'p', 'r', or 'q'\n")

        elif(problemChoice == '2'):
            print('\n -- Starting Problem 2 --\n')
            print('\nPay special attention to the outputs.  The Recursive solution returns all visited values and literally displays them.   The recursive solution displays every possible cube and places a True where it was visited, thus the Recursive Solution may return a [] and the DP solution returns a huge list of falses')
            while True:
                g_visitedCubes = []
                print('Enter one of the following options...\n( P ) : Predictable Answer\n( R ) : Random\n( Q ) : Quit')
                p5Choice = input('Your choice: ').lower()

                if p5Choice == 'p':
                    #Custom Case
                    l_width = 3
                    l_height = 4
                    l_depth = 5
                    l_startX = 0
                    l_startY = 0
                    l_startZ = 0
                    l_moves = [[0, 1, 2], [0, 3, 1], [1, 1, 2], [1, 2, 2]]
                    print(f'Starting coordinates: {l_startX}, {l_startY}, {l_startZ}')
                    print(f'Cube dimensions: {l_width} x {l_height} x {l_depth}')
                    print(f'Moves: {l_moves}')
                    print(f'Recursive: {problemTwoRecursive(l_moves, l_startX, l_startY, l_startZ, l_width, l_height, l_depth)}')
                    print(f'\nDP: {problemTwoDP(l_moves, l_startX, l_startY, l_startZ, l_width, l_height, l_depth)}\n')

                elif p5Choice == 'r':
                    #random cases
                    l_width = random.randint(2, 10)
                    l_height = random.randint(2, 10)
                    l_depth = random.randint(2, 10)
                    l_startX = random.randint(0, l_width)
                    l_startY = random.randint(0, l_height)
                    l_startZ = random.randint(0, l_depth)

                    #generate moves
                    l_moves = []
                    for i in range(0, random.randint(3, 10)):
                        deltaX = random.randint(0, 9)
                        deltaY = random.randint(0, 9)
                        deltaZ = random.randint(0, 9)

                        if deltaX == 0 and deltaY == 0 and deltaZ == 0:
                            deltaX += 1
                        l_moves.append((deltaX, deltaY, deltaZ))
                    
                    print(f'Starting coordinates: {l_startX}, {l_startY}, {l_startZ}')
                    print(f'Cube dimensions: {l_width} x {l_height} x {l_depth}')
                    print(f'Moves: {l_moves}')
                    print(f'Recursive: {problemTwoRecursive(l_moves, l_startX, l_startY, l_startZ, l_width, l_height, l_depth)}')
                    print(f'\nDP: {problemTwoDP(l_moves, l_startX, l_startY, l_startZ, l_width, l_height, l_depth)}\n')
                elif p5Choice == 'q':
                    break
                else:
                    print("\n Sorry, that didn't make sense.  Enter either a 'p', 'r', or 'q'\n")

            #custom problem
            

        elif(problemChoice == '3'):
            print('\n -- Starting Problem 3 --\n')
            print('!!  This DP algorithm is beautiful !!\n')

            while True:
                print('Enter one of the following options...\n( P ) : Predictable Answer\n( R ) : Random\n( Q ) : Quit')
                p5Choice = input('Your choice: ').lower()

                if p5Choice == 'p':
                    #Custom Case
                    l_k1Size = 12
                    l_k2Size = 25
                    l_sizes = [4, 7, 16, 3]
                    print(f'\nk1Size: {l_k1Size}  |  k2Size = {l_k2Size}\nvalues: {l_sizes}')
                    print('Recursive: ', (problemThreeRecursive(l_k1Size, l_sizes) and problemThreeRecursive(l_k2Size, l_sizes)))
                    print(f'DP: {problemThreeDP(l_k1Size, l_sizes) and problemThreeDP(l_k2Size, l_sizes)}\n')
                    
                elif p5Choice == 'r':
                    #random cases
                    l_k1Size = random.randint(0, 100)
                    l_k2Size = random.randint(0, 100)
                    
                    #generate the sizes
                    l_sizes = []
                    for i in range(0, random.randint(0, 100)):
                        l_sizes.append(random.randint(1, 100))
                    print(f'\nk1Size: {l_k1Size}  |  k2Size = {l_k2Size}\nvalues: {l_sizes}')
                    print('Recursive: ', (problemThreeRecursive(l_k1Size, l_sizes) and problemThreeRecursive(l_k2Size, l_sizes)))
                    print(f'DP: {problemThreeDP(l_k1Size, l_sizes) and problemThreeDP(l_k2Size, l_sizes)}\n')
                elif p5Choice == 'q':
                    break
                else:
                    print("\n Sorry, that didn't make sense.  Enter either a 'p', 'r', or 'q'\n")

            l_k1Size = 12
            l_k2Size = 25
            l_sizes = [4, 7, 16, 3]
            print(f'k1Size: {l_k1Size}  |  k2Size = {l_k2Size}\nvalues: {l_sizes}')
            print('Recursive: ', (problemThreeRecursive(l_k1Size, l_sizes) and problemThreeRecursive(l_k2Size, l_sizes)))
            print(f'DP: {problemThreeDP(7, [3, 6, 5, 9])}')

        elif(problemChoice == '4'):
            print('\n -- Starting Problem 4 --\n')
            print('!! Fair Warning, the answer sometimes comes slowly, but it does come.  Recursion takes a while')

            while True:
                print('Enter one of the following options...\n( P ) : Predictable Answer\n( R ) : Random\n( Q ) : Quit')
                p5Choice = input('Your choice: ').lower()

                if p5Choice == 'p':
                    #Custom Case
                    l_col = 7
                    l_row = 4
                    l_values = [[10, 3,  20, 4,  19, 20, 13], 
                                [3,  6,  7,  44, 22, 7,  6], 
                                [6,  13, 4,  16, 11, 5,  20], 
                                [23, 9,  7,  33, 15, 1,  31]]
                    l_maxValues = []
                    for i in range(0, len(l_values)):
                        l_maxValues.append(problemFourRecursive(i, 0, l_values))
                    print(f'Recursive: ${max(l_maxValues)}')
                    print(f'DP: ${problemFourDP(l_values)}\n')
                elif p5Choice == 'r':
                    #Random cases
                    l_col = random.randint(1, 30)
                    l_row = random.randint(1, 30)
                    l_values = [[0] * (l_col + 1) for i in range(0, l_row)]  #allocate memory for array
                    for i in range(l_row):
                        for j in range(l_col):
                            l_values[i][j] = random.randint(1, 100)
                    l_maxValues = []
                    for i in range(0, len(l_values)):
                        l_maxValues.append(problemFourRecursive(i, 0, l_values))
                    print(f'Recursive: ${max(l_maxValues)}')
                    print(f"DP: ${problemFourDP(l_values)}\n") 
                elif p5Choice == 'q':
                    break
                else:
                    print("\n Sorry, that didn't make sense.  Enter either a 'p', 'r', or 'q'\n")

            

            #Random cases
            l_col = random.randint(1, 30)
            l_row = random.randint(1, 30)
            l_values = [[0] * l_col for i in range(0, l_row)]  #allocate memory for array
            for i in range(l_row):
                for j in range(l_col):
                    l_values[i][j] = round(random.uniform(1.0, 100.0), 2)
            print(f"Recursive: ${problemFourRecursive(random.randint(0, l_row - 1), 0, l_values)}")          
        
        elif(problemChoice == '5'):
            print('\n -- Starting Problem 5 --\n')
            print("!! This problem can be interpretted two ways.  I made it so the Recursive Function returns the maximum value possible as stated in the problem, and the DP returns the solution as if the computer was playing a 'smart' game too.\n")

            while True:
                print('Enter one of the following options...\n( P ) : Predictable Answer\n( R ) : Random Coin Values\n( Q ) : Quit')
                p5Choice = input('Your choice: ').lower()

                if p5Choice == 'p':
                    l_coins = [5, 10, 4, 4]
                    print(f'\nCoins: {l_coins}')
                    print(f'\nMaximum Value Possible (Recursive): {problemFiveRecursive(l_coins)}')
                    print(f'Realistic Value Possible (DP):      {problemFiveDP(l_coins)}\n')
                elif p5Choice == 'r':
                    l_coins = []
                    for i in range(0, random.randint(1, 10) * 2):
                        l_coins.append(random.randint(1, 9))
                    print(f'\nCoins: {l_coins}')
                    print(f'\nMaximum Value Possible (Recursive): {problemFiveRecursive(l_coins)}')
                    print(f'Realistic Value Possible (DP):      {problemFiveDP(l_coins)}\n')
                    pass
                elif p5Choice == 'q':
                    break
                else:
                    print("\n Sorry, that didn't make sense.  Enter either a 'p', 'r', or 'q'\n")

        elif(problemChoice == 'q'):
            print('\n\n -- EXITING -- \n')
            break
        else:
            print('\n !! That was not a valid choice. !!  Pick a number between 1 and 5 or q to quit\n')
        
        print("\n -- FINISHED --\n")