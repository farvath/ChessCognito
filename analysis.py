import chess
import chess.pgn
import chess.engine
from tabulate import tabulate

# Path to Stockfish executable
STOCKFISH_PATH = 'F:/final/stockfish/stockfish-windows-x86-64-avx2.exe'

# Path to PGN file
PGN_FILE = "C:/Users/Farvath/OneDrive/Desktop/chess_game.pgn"

def move_remarks(evaluation):
    if evaluation is None:
        return "No evaluation available"
    elif evaluation >= 100:
        return "Excellent move!"
    elif evaluation >= 50:
        return "Good move"
    elif evaluation >= 20:
        return "Decent move"
    elif evaluation >= -20:
        return "Okay move"
    elif evaluation >= -50:
        return "Not the best choice"
    elif evaluation >= -100:
        return "Mistake"
    else:
        return "Blunder"

def analyze_game(pgn_file, stockfish_path, player_side):
    headers = ["Move", "Evaluation", "Remarks", "Suggested Move", "Check"]
    table_data = []
    check_status = False

    with open(pgn_file) as pgn:
        game = chess.pgn.read_game(pgn)
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        board = game.board()

        for move in game.mainline_moves():
            board.push(move)
            info = engine.analyse(board, chess.engine.Limit(time=0.1))

            if player_side == 'white':
                evaluation = info["score"].white().score() if info["score"].white() else None
            else:
                evaluation = info["score"].black().score() if info["score"].black() else None

            suggested_move = None
            if evaluation is not None and abs(evaluation) > 100:
                suggested_moves_info = engine.analyse(board, chess.engine.Limit(time=0.5)).get("pv", [])
                if suggested_moves_info:
                    suggested_move = str(suggested_moves_info[0])

            # Check if the move results in a check
            if board.is_check():
                check_status = True
            else:
                check_status = False

            table_data.append([move, evaluation, move_remarks(evaluation), suggested_move, "Yes" if check_status else "No"])

        engine.quit()

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Determine the result of the game
    result = game.headers["Result"]
    if result == "1-0":
        winner = "White"
    elif result == "0-1":
        winner = "Black"
    else:
        winner = "Draw"

    # Summary of the match
    print("\nMatch Summary:")
    print("Total moves:", len(table_data))
    print("Winner:", winner)
    print("Result:", result)

# Ask the user which side they played
player_side = input("Did you play as white or black? Enter 'white' or 'black': ").lower()

# Analyze the game
analyze_game(PGN_FILE, STOCKFISH_PATH, player_side)