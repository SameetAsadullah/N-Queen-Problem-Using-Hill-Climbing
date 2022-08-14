import random
import math
import numpy as np

board = None  # to store chess board
N = -1  # to store size of the board


# function to generate board
def generate():
    global board
    board = np.zeros([N, N], dtype=int)
    rows = [*range(N)]
    # initialising queens in all different columns
    for i in range(N):
        board[random.choice(tuple(rows))][i] = 1

    # initialising queens randomly
    # for i in range(N):
    #    cols = [*range(N)]
    #    board[random.choice(tuple(rows))][random.choice(tuple(cols)] = 1


# function to arrange queens in all different columns
def arrangeBoard():
    # forward fixing
    for i in range(N):
        check = False
        for j in range(N):
            if board[j][i] == 1 and check and i != N - 1:
                board[j][i] = 0
                for k in range(N):
                    if board[k][i + 1] == 0:
                        board[k][i + 1] = 1
                        break
            if board[j][i] == 1 and not check:
                check = True

    # backward fixing
    for i in reversed(range(N)):
        check = False
        for j in range(N):
            if board[j][i] == 1 and check and i != 0:
                board[j][i] = 0
                for k in range(N):
                    if board[k][i - 1] == 0:
                        board[k][i - 1] = 1
                        break
            if board[j][i] == 1 and not check:
                check = True


# function to calculate objective i.e. how many queens are attacking each other
def objectiveFunc(temp_board):
    count = 0
    for i in range(N):
        for j in range(N):
            if temp_board[i][j] == 1:
                # checking other queens in the same row
                col = 0
                while col != N:
                    if col != j and temp_board[i][col] == 1:
                        count += 1
                    col += 1

                # checking queens in the same column
                row = 0
                while row != N:
                    if row != i and temp_board[row][j] == 1:
                        count += 1
                    row += 1

                # checking queens in the area above main diagonal
                row = i - 1
                col = j - 1
                while row != -1 and col != -1:
                    if temp_board[row][col] == 1:
                        count += 1
                    row -= 1
                    col -= 1

                # checking queens in the area below main diagonal
                row = i + 1
                col = j + 1
                while row != N and col != N:
                    if temp_board[row][col] == 1:
                        count += 1
                    row += 1
                    col += 1

                # checking queens in the area above reverse diagonal
                row = i - 1
                col = j + 1
                while row != -1 and col != N:
                    if temp_board[row][col] == 1:
                        count += 1
                    row -= 1
                    col += 1

                # checking queens in the area below reverse diagonal
                row = i + 1
                col = j - 1
                while row != N and col != -1:
                    if temp_board[row][col] == 1:
                        count += 1
                    row += 1
                    col -= 1
    return count // 2


# function to check neighbour when applying hill climbing and move
# if there's a better neighbour otherwise stay at the same position
def checkNeighboursHC(row, col):
    global board
    temp_board = np.copy(board)

    # if queen is in the first row who's neighbours are being checked
    if row == 0:
        temp_board[row][col] = 0
        temp_board[row + 1][col] = 1
        if objectiveFunc(temp_board) <= objectiveFunc(board):
            board = np.copy(temp_board)

    # if queen is in the last row who's neighbours are being checked
    elif row == N - 1:
        temp_board[row][col] = 0
        temp_board[row - 1][col] = 1
        if objectiveFunc(temp_board) <= objectiveFunc(board):
            board = np.copy(temp_board)

    # if in between first and last row
    else:
        temp_board1 = np.copy(board)
        temp_board[row][col] = 0
        temp_board[row - 1][col] = 1
        temp_board1[row][col] = 0
        temp_board1[row + 1][col] = 1

        # randomly choose if the objective function of neighbours are same
        if (objectiveFunc(temp_board) == objectiveFunc(temp_board1)) \
                and (objectiveFunc(temp_board) <= objectiveFunc(board)):
            check = random.randrange(0, 2)
            if check == 0:
                board = np.copy(temp_board)
            elif check == 1:
                board = np.copy(temp_board1)

        # choose the neighbour who has less objective value
        elif (objectiveFunc(temp_board) < objectiveFunc(temp_board1)) \
                and (objectiveFunc(temp_board) < objectiveFunc(board)):
            board = np.copy(temp_board)

        # choose the neighbour who has less objective value
        elif (objectiveFunc(temp_board1) < objectiveFunc(temp_board)) \
                and (objectiveFunc(temp_board1) < objectiveFunc(board)):
            board = np.copy(temp_board1)
    return objectiveFunc(board)  # return objective function of updated board


# hill climbing algorithm
def hillClimbing():
    count = objectiveFunc(board)
    while count != 0:  # loop until the solution is found i.e. no queen is attacking any other queen
        check = np.copy(board)
        # traversing through the board
        for i in range(N):
            if count == 0:
                return not None
            for j in range(N):
                if count == 0:
                    return not None
                if board[i][j] == 1:
                    count = checkNeighboursHC(i, j)
        if np.array_equal(check, board):  # if no better neighbours were found then return
            return None


# function to check neighbour when applying simulated annealing and move
# if there's a better neighbour otherwise stay at the same position
def checkNeighboursSA(row, col, T):
    global board
    temp_board = np.copy(board)

    # if queen is in the first row who's neighbours are being checked
    if row == 0:
        temp_board[row][col] = 0
        temp_board[row + 1][col] = 1
        if (objectiveFunc(board) - objectiveFunc(temp_board)) > 0:  # if it's a better move
            board = np.copy(temp_board)
        else:  # otherwise randomly choose the neighbour
            exp = (objectiveFunc(board) - objectiveFunc(temp_board)) / T
            exp = math.exp(exp)
            check = random.uniform(0, 1)
            if check < exp:
                board = np.copy(temp_board)

    # if queen is in the last row who's neighbours are being checked
    elif row == N - 1:
        temp_board[row][col] = 0
        temp_board[row - 1][col] = 1
        if (objectiveFunc(board) - objectiveFunc(temp_board)) > 0:  # if it's a better move
            board = np.copy(temp_board)
        else:  # otherwise randomly choose the neighbour if probability is less than exp
            exp = (objectiveFunc(board) - objectiveFunc(temp_board)) / T
            exp = math.exp(exp)
            check = random.uniform(0, 1)
            if check < exp:
                board = np.copy(temp_board)

    # if in between first and last row
    else:
        check = random.randrange(0, 2)  # randomly choose any neighbour
        if check == 1:
            temp_board[row][col] = 0
            temp_board[row - 1][col] = 1
        else:
            temp_board[row][col] = 0
            temp_board[row + 1][col] = 1

        if (objectiveFunc(board) - objectiveFunc(temp_board)) > 0:  # if it's a better move
            board = np.copy(temp_board)
        else:  # otherwise randomly choose the neighbour if probability is less than exp
            exp = (objectiveFunc(board) - objectiveFunc(temp_board)) / T
            exp = math.exp(exp)
            check = random.uniform(0, 1)
            if check < exp:
                board = np.copy(temp_board)
    return objectiveFunc(board)


# simulated annealing algorithm
def simulatedAnnealing(T, decFactor):
    count = objectiveFunc(board)
    while count != 0 and T > 1:  # loop until the solution is found or value of T becomes less than 1
        # traversing through the board
        for i in range(N):
            if count == 0 or T <= 1:
                break;
            for j in range(N):
                if count == 0 or T <= 1:
                    break;
                if board[i][j] == 1:
                    count = checkNeighboursSA(i, j, T)
                    T *= decFactor  # decrease value of T everytime
    if T <= 1 and count != 0:
        print("No solution found using Simulated Annealing.\n")
        return None
    return not None


if __name__ == "__main__":
    N = int(input("Enter N: "))
    generate()
    arrangeBoard()    # use this function to arrange queens in all different columns if generated randomly before
    print("Initial Board:\n", board)
    board_cpy = np.copy(board)

    if hillClimbing() is None:
        print("\nNo solution found using Hill Climbing.\n")
    else:
        print("\nFinal board using Hill Climbing:\n", board)

    board = np.copy(board_cpy)
    if simulatedAnnealing(10000, 0.99) is not None:
        print("Final board using Simulated Annealing:\n", board)
