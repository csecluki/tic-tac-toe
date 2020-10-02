def bestscore(board):
    optimal = -100
    x = 0
    y = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minmax(board, 0, False)
                board[i][j] = 0
                if score > optimal:
                    optimal = score
                    x = i
                    y = j
    return x, y


def minmax(board, depth, ismax):
    result = winner(board)
    if result == "cross":
        return -1
    if result == "circle":
        return 1
    if result == "draw":
        return 0

    if ismax:
        optimal = -100
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = minmax(board, depth + 1, False)
                    board[i][j] = 0
                    optimal = max(optimal, score)
        return optimal
    else:
        optimal = 100
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minmax(board, depth + 1, True)
                    board[i][j] = 0
                    optimal = min(optimal, score)
        return optimal


win_combinations = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)],
        ]


def winner(board):
    for i in win_combinations:
        if board[i[0][0]][i[0][1]] == board[i[1][0]][i[1][1]] == board[i[2][0]][i[2][1]] != 0:
            if board[i[0][0]][i[0][1]] == 1:
                return "cross"
            else:
                return "circle"

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return "continue"

    return "draw"
