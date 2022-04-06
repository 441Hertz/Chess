from Board import Board
from Piece import *
class Chess():
    """
    Put description of the Chess class here
    """
    def __init__(self, dev_mode = False, console = False):
        self.board = Board()
        self.move_counter = 1
        self.dev_mode = dev_mode
        self.move_log = []
        self.console = console
    def promotion(self, board, to):
        y_pos = int(to[1])
        if board[to].get_name() == 'P' and (y_pos == 8 or y_pos == 1):
            promote = input('Promote pawn to: ').lower()[0]
            while promote not in ['q', 'r', 'b', 'n']:
                print('Invalid piece!')
                promote = input('Promote pawn to: ').lower()
            if promote == 'r':
                board[to] = Rook(board[to].get_col(), to)
            elif promote == 'n':
                board[to] = Knight(board[to].get_col(), to)
            elif promote == 'b':
                board[to] = Bishop(board[to].get_col(), to)
            elif promote == 'q':
                board[to] = Queen(board[to].get_col(), to)
    def whose_move(self):
        if self.move_counter % 2 == 1:
            return ('w', 'white')
        return ('b', 'black')
    def which_move(self):
        return (self.move_counter + 1) // 2
    def correct_turn(self, start):
        if not self.dev_mode:
            return self.board.board[start].get_col() == self.whose_move()[0]
        return True
    def is_piece(self, start):
        return self.board.board[start] != '__'
    def valid_pos(self, *positions):
        # Breaks if y pos is a string + probably more
        # Also only checks for the start pos - not the to pos
        for pos in positions:
            if len(pos) == 2:
                valid_x = pos[0] in 'abcdefgh'
                valid_y = pos[1] in '12345678'
                if not (valid_x and valid_y):
                    return False
            else:
                return False
        return True
    def update_counter(self):
        self.move_counter += 1
        Piece.update_counter(self.move_counter)
    def castle(self, board, start, to):
        rook_pos = board[start].rook_pos(board, start, to)
        castled_rook_pos = board[start].castled_rook_pos(board, start, to)
        self.replace(board, start, to)
        self.replace(board, rook_pos, castled_rook_pos)
    def replace(self, board, start, to):
        # Moves piece from start to to 
        # Places empty space at start location
        # Updates position attribute
        board[to] = board[start]
        board[start] = '__'
        board[to].update_pos(to)
    def error_msg(self):
        pass
    def update_log(self, start, to):
        # TODO
        # ASSUMES THE FIRST MOVE IS MADE BY WHITE
        # BUT IF A CUSTOM BOARD IS LOADED AND BLACK MOVES FIRST GG
        move = self.which_move()
        log = self.move_log

        if self.whose_move()[0] == 'w':
            log.append([move, start + to, ''])
        else:
            log[move - 1][2] = start + to

    def move(self, start, to):
        # TODO : ghost board? -theres some redundancy in updating the logic board and visual board
        # MAYBE ADD IN THE BOARD START TO VARIABLES AS CLASS ATTRIBUTES AND UPDATE THEM HERE WHEN ITS VALID? 
        # THAT WAY WE DONT HAVE TO CONSTANTLY PASS IN VARIABLES FOR METHODS
        """ 
        What an absolute mess
        """
        board = self.board.board
        if self.console:
            self.board.print_board()
            print("---------------------------------------------------------------")
        if self.valid_input(start, to):
            if self.valid_move(board, start, to):
                piece = board[start]

                if piece.get_name() == 'K' and abs(piece.x_diff(start, to)) == 2:
                    self.castle(board, start, to)
                else:
                    self.replace(board, start, to)
                    self.promotion(board, to)
            
                self.update_log(start, to)
                self.update_counter()
                if self.console:
                    self.end_output(piece.__str__() + f' moved from {start} to {to}')

                if board[to].mate(board, to):
                    if self.console:
                        print('Checkmate!')
                    return False
        return True

    def valid_input(self, start, to):
        valid_pos = self.valid_pos(start, to)
        if valid_pos:
            valid_pos = self.is_piece(start)
            if valid_pos:
                valid_turn = self.correct_turn(start)

        # We could have an error msg that contains all the errors with the move
        # but could be redundant
        # error = ''
        if self.console:
            if not valid_pos:
                self.end_output(f"Invalid Move: {start} to {to} \nInvalid position or empty space")
            elif not valid_turn:
                self.end_output(f"Invalid Move: {start} to {to} \nIt's {self.whose_move()[1]}'s turn!")
            
        return valid_pos and valid_turn

    def valid_move(self, board, start, to):
        valid = board[start].is_valid_move(board, start, to)  
        legal = board[start].is_legal(board, start, to)

        if not valid:
            self.end_output(f"Invalid Move: {start} to {to} \nRead the rules!")
        elif not legal:
            self.end_output(f"Invalid Move: {start} to {to} \nMove is not legal!")

        return valid and legal

    def end_output(self, msg):
        print(msg)
        self.board.print_board()
        # print(self.move_log)
        print("---------------------------------------------------------------")
    
        
def translate(position):
    return position

def code_words(code):
    pass
if __name__ == "__main__":
    # TODO
    # PAWN ENPASSANTE FUNCTION IS BROKEN 
    # WHEN LOADING IN A DEFAULT BOARD
    dev_mode = False
    chess = Chess(dev_mode, True)
#     chess.board.custom_board({
# 'a8':'br', 'b8':'wQ', 'c8':'__', 'd8':'__', 'e8':'bK', 'f8':'bR', 'g8':'__', 'h8':'bR',
# 'a7':'bP', 'b7':'__', 'c7':'__', 'd7':'__', 'e7':'__', 'f7':'__', 'g7':'__', 'h7':'__',
# 'a6':'__', 'b6':'__', 'c6':'__', 'd6':'__', 'e6':'__', 'f6':'__', 'g6':'__', 'h6':'__',
# 'a5':'__', 'b5':'wP', 'c5':'__', 'd5':'__', 'e5':'__', 'f5':'__', 'g5':'__', 'h5':'__',
# 'a4':'__', 'b4':'__', 'c4':'__', 'd4':'__', 'e4':'__', 'f4':'__', 'g4':'__', 'h4':'__',
# 'a3':'__', 'b3':'__', 'c3':'__', 'd3':'__', 'e3':'__', 'f3':'__', 'g3':'__', 'h3':'__',
# 'a2':'wP', 'b2':'wP', 'c2':'__', 'd2':'__', 'e2':'__', 'f2':'wP', 'g2':'__', 'h2':'__',
# 'a1':'wR', 'b1':'__', 'c1':'__', 'd1':'__', 'e1':'wK', 'f1':'__', 'g1':'__', 'h1':'wR',
# })

    # chess.move('e1', 'g1')
    # chess.move('e8', 'c8')

    running = True
    while running:
        start = input("From: ")
        if start == 'exit':
            break
        to = input("To: ")
        
        start = translate(start)
        to = translate(to)

        if start == None or to == None:
            continue
        
        running = chess.move(start, to)
        # TODO 
        # If move is invalid, the checkmate function checks the TO position 
        # To see if it can mate
        # But invalid so the move is not made - THEREFORE the TO position is empty and game crash

    # print(chess.move_log)
    chess.board.generate_preset()
    chess.board.save_logs(chess.move_log, filename = 'test')
        