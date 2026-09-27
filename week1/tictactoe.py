"""
Tic-Tac-Toe AI Lab Program
--------------------------
Demonstrates the Minimax algorithm (with alpha-beta pruning) for an
unbeatable AI player in Tic-Tac-Toe.

Human  = 'X' (moves first)
AI     = 'O' (uses minimax to find optimal move)

Concepts demonstrated:
  - Game tree representation
  - Minimax search (MIN and MAX levels)
  - Alpha-beta pruning for search-space reduction
  - Terminal state / utility evaluation
"""

import math

print("SCRIPT STARTED")
def print_board(board):
    print()
    for i in range(0, 9, 3):
        row = board[i:i + 3]
        print(" | ".join(row))
        if i < 6:
            print("---------")
    print()


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == ' ']


def check_winner(board, player):
    win_combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6)               # diagonals
    ]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_combos)


def is_full(board):
    return ' ' not in board


def is_terminal(board):
    return check_winner(board, 'X') or check_winner(board, 'O') or is_full(board)


# ---------------------------------------------------------------------
# Minimax with Alpha-Beta Pruning
# ---------------------------------------------------------------------
# AI = 'O' is the MAXIMIZING player, Human = 'X' is the MINIMIZING player.

def evaluate(board, depth):
    if check_winner(board, 'O'):
        return 10 - depth      # prefer faster wins
    if check_winner(board, 'X'):
        return depth - 10      # prefer slower losses
    return 0                   # draw / non-terminal


def minimax(board, depth, alpha, beta, is_maximizing):
    if is_terminal(board):
        return evaluate(board, depth)

    if is_maximizing:  # AI's turn ('O')
        best = -math.inf
        for move in available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth + 1, alpha, beta, False)
            board[move] = ' '
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # beta cutoff
        return best
    else:  # Human's turn ('X')
        best = math.inf
        for move in available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth + 1, alpha, beta, True)
            board[move] = ' '
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break  # alpha cutoff
        return best


def best_move(board):
    best_score = -math.inf
    move = -1
    for candidate in available_moves(board):
        board[candidate] = 'O'
        score = minimax(board, 0, -math.inf, math.inf, False)
        board[candidate] = ' '
        if score > best_score:
            best_score = score
            move = candidate
    return move


# ---------------------------------------------------------------------
# Game loop
# ---------------------------------------------------------------------

def play_game():
    board = [' '] * 9
    print("Tic-Tac-Toe: You are 'X', AI is 'O'.")
    print("Board positions are numbered 0-8, left to right, top to bottom:")
    print_board([str(i) for i in range(9)])

    current_player = 'X'  # human moves first

    while True:
        print_board(board)

        if is_terminal(board):
            break

        if current_player == 'X':
            move = -1
            while move not in available_moves(board):
                try:
                    move = int(input("Enter your move (0-8): "))
                except ValueError:
                    continue
            board[move] = 'X'
            current_player = 'O'
        else:
            print("AI is thinking...")
            move = best_move(board)
            board[move] = 'O'
            print(f"AI plays position {move}")
            current_player = 'X'

    print_board(board)
    if check_winner(board, 'X'):
        print("You win! (This shouldn't happen against a perfect AI \U0001F609)")
    elif check_winner(board, 'O'):
        print("AI wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    play_game()