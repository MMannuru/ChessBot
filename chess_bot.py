import chess
import chess.engine

#installed stockfish with 'brew install stockfish' (this is for mac)
stockfish_path = "/opt/homebrew/bin/stockfish"

#prints the board
#originally didn't have row and column numbers which made it a bit confusing so i went back and added those
def print_board(board): #argument is an instance of chess.Board
    #str(board) converts board into string representation. each row of chessboard is represented as a line of text
    #.split("\n") splits this string into a list where each row is represented as a string
    board_string = str(board).split("\n")
    #columns of chess board
    columns = "  a b c d e f g h"
    #we first print our columns
    print(columns)
    #now for the board
    #to get numbers on each side we start with 8 and subtract that with the index to get the row number
    #put this on both sides, and in the middle we print the actual row
    for i, row in enumerate(board_string):
        print(f"{8 - i} {row} {8 - i}")
    #print columns again
    print(columns)
    #now the board representation has all the rows along with columns and row #

def display_moves(board):
    #board.legal_moves allows us to iterate over all the legal moves
    legal_moves = list(board.legal_moves)
    print("\nPossible Moves:")
    #displaying all legal moves
    for move in legal_moves:
        print(f"{str(move)}")
    print()

def get_player_move(board):
    while True:
        #getting input from the player
        #.strip() is important here bc it gets rid of any spaces user leaves
        move = input("White's move (or type 'help' for options): ").strip()
        if move == "help":
            print("Commands:")
            print("  'resign' - forfeit the game")
            print("  'legal' - to show all legal moves")
            print("  'superpower' - get help from a friend")
            continue

        if move == "resign":
            print("You gave up :( You lose")
            return None

        if move == "legal":
            display_moves(board)
            continue

        #using this in main function to call the engine
        if move == "use engine":
            return "engine"

        try:
            uci_move = chess.Move.from_uci(move) #converting user move into chess.Move object
            if uci_move in board.legal_moves:
                return uci_move
            else:
                print("Illegal move. Refer to the help guide.")
        except:
            print("Invalid format. Refer to the help guide.")

def main():
    #initializing chessboard object
    board = chess.Board()

    #starting the stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    print("Welcome to my unbeatable ChessBot!")
    print("You're playing as Black. Enter your moves by typing the move (e.g. type e2e4).")
    #displaying the board
    print_board(board)

    game_over = board.is_game_over()

    while not game_over:
        player_move = get_player_move(board)
        #if player quits break loop
        if player_move is None:
            break
        #if player decides to get some help...
        elif player_move == "engine":
            print("Generating move:")
            #giving engine a 1 second time limit
            result = engine.play(board, chess.engine.Limit(time=1.0))
            #applying the generated move
            board.push(result.move)
            print(f"Generated move: {result.move}")
        else:
            #if engine isn't used we update board with users move
            board.push(player_move)

        #printing updated board
        print_board(board)

        #break loop if game is over after white move
        if game_over:
            break

        #now for black players logic 
        move = input("Black's move (or type 'help' for options): ").strip()
        if move == "engine":
            print("Generating move:")
            #giving engine a 1 second time limit
            result = engine.play(board, chess.engine.Limit(time=1.0))
            #applying the generated move
            board.push(result.move)
            print(f"Generated move: {result.move}")
        else: 
            try:
                uci_move = chess.Move.from_uci(move)
                if uci_move in board.legal_moves:
                    board.push(uci_move)
                else:
                    print("Illegal move. Refer to the help guide.")
                    continue
            except:
                print("Invalid format. Refer to the help guide.")
                continue

        print_board(board)

    result = board.result()
    print(f"Game over! Result: {result} (1-0 is a win for white, 0-1 is a win for black)")

    engine.quit()

if __name__ == "__main__":
    main()
