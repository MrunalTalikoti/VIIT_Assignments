import math

# Function to print the board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

# Check for winner
def evaluate(board):
    # Rows
    for row in board:
        if row.count(row[0]) == 3 and row[0] != "_":
            return 10 if row[0] == "O" else -10

    # Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "_":
            return 10 if board[0][col] == "O" else -10

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != "_":
        return 10 if board[0][0] == "O" else -10
    if board[0][2] == board[1][1] == board[2][0] != "_":
        return 10 if board[0][2] == "O" else -10

    return 0

# Check if moves are left
def moves_left(board):
    for row in board:
        if "_" in row:
            return True
    return False

# Minimax Algorithm
def minimax(board, depth, is_max):
    score = evaluate(board)

    # Terminal states
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not moves_left(board):
        return 0

    if is_max:  # Maximizer (AI)
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "O"
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = "_"
        return best
    else:  # Minimizer (Human)
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "X"
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = "_"
        return best

# AI Move
def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = "O"
                move_val = minimax(board, 0, False)
                board[i][j] = "_"

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

# ------------------- Game -------------------
def play_game():
    board = [["_"] * 3 for _ in range(3)]
    print("Tic Tac Toe - You are X, AI is O")

    while True:
        print_board(board)

        # Human move
        x, y = map(int, input("Enter your move (row col): ").split())
        if board[x][y] != "_":
            print("Invalid move, try again.")
            continue
        board[x][y] = "X"

        if evaluate(board) == -10:
            print_board(board)
            print("You win!")
            break
        if not moves_left(board):
            print_board(board)
            print("It's a draw!")
            break

        # AI move
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = "O"

        if evaluate(board) == 10:
            print_board(board)
            print("AI wins!")
            break
        if not moves_left(board):
            print_board(board)
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()
