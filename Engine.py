from Board import Board
from Piece import *
class Chess():
    def __init__(self, dev_mode = False, console = False):
        self.board = Board()
        self.move_counter = 1
        self.dev_mode = dev_mode
        self.move_log = []
        self.console = console
        
        self.msg = ''
        self.error = ''
        self.moved = False
        self.finished = False
        
        if self.console:
            self.start_console()
            
    def move(self, start, to):
        # TODO : ghost board? -theres some redundancy in updating the logic board and visual board
        # MAYBE ADD IN THE BOARD START TO VARIABLES AS CLASS ATTRIBUTES AND UPDATE THEM HERE WHEN ITS VALID? 
        # THAT WAY WE DONT HAVE TO CONSTANTLY PASS IN VARIABLES FOR METHODS
        self.moved = False
        board = self.board.board
            
        if self.valid_input(start, to):
            piece = board[start]
            if piece.can_replace(board, to):
                if self.valid_move(board, start, to):

                    if piece.name == 'K' and abs(piece.x_diff(start, to)) == 2:
                        self.castle(board, start, to)
                    else:
                        self.replace(board, start, to)
                        self.promotion(board, to)
                
                    self.update_log(start, to)
                    self.update_counter()
                        
                    self.msg = board[to].__str__() + f' moved from {start} to {to}'
                    self.moved = True
                    
                    if board[to].mate(board, to):
                        self.finished = True
                        return False
                
        if self.console:
            self.output_console(board, start, to)
            
        return True
    
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
    
    def valid_input(self, start, to):
        valid_pos = self.valid_pos(start, to)
        if valid_pos:
            valid_pos = self.is_piece(start)
            if valid_pos:
                valid_turn = self.correct_turn(start)

        if not valid_pos:
            self.error = f"Invalid Move: {start} to {to} \nInvalid position or empty space"
        elif not valid_turn:
            self.error = f"Invalid Move: {start} to {to} \nIt's {self.whose_move()[1]}'s turn!"
            
        return valid_pos and valid_turn

    def valid_move(self, board, start, to):
        valid = board[start].is_valid_move(board, start, to)  
        legal = board[start].is_legal(board, start, to)

        if not valid:
            self.error = f"Invalid Move: {start} to {to} \nRead the rules!"
        elif not legal:
            self.error = f"Invalid Move: {start} to {to} \nMove is not legal!"

        return valid and legal
            
    def promotion(self, board, to):
        y_pos = int(to[1])
        if board[to].name == 'P' and (y_pos == 8 or y_pos == 1):
            promote = input('Promote pawn to: ').lower()[0]
            while promote not in ['q', 'r', 'b', 'n']:
                print('Invalid piece!')
                promote = input('Promote pawn to: ').lower()
            if promote == 'r':
                board[to] = Rook(board[to].color, to)
                board[to].moves = 1
            elif promote == 'n':
                board[to] = Knight(board[to].color, to)
            elif promote == 'b':
                board[to] = Bishop(board[to].color, to)
            elif promote == 'q':
                board[to] = Queen(board[to].color, to)
                
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
        board[start] = None
        board[to].update_pos(to)
    
    def start_console(self):
        # TODO
        # Will always display default board regardless if custom board is passed
        self.board.print_board()
        print("---------------------------------------------------------------")
        
    def output_console(self, board, start, to):
        print("---------------------------------------------------------------")
        # If it did not move, then there should be a self.msg
        if self.moved:
            msg = self.msg
        else:
            msg = self.error
        print(msg)
        
        self.board.print_board()
        # print(self.move_log)
        print("---------------------------------------------------------------")
        if self.finished:
            print('Checkmate!')
            
    def whose_move(self):
        if self.move_counter % 2 == 1:
            return ('w', 'white')
        return ('b', 'black')
    
    def which_move(self):
        return (self.move_counter + 1) // 2
    
    def correct_turn(self, start):
        if not self.dev_mode:
            return self.board.board[start].color == self.whose_move()[0]
        return True
    
    def is_piece(self, start):
        return self.board.board[start] != None

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
            
    def update_counter(self):
        self.move_counter += 1
        Piece.update_counter(self.move_counter)
        
if __name__ == "__main__":
    # TODO
    # PAWN ENPASSANTE FUNCTION IS BROKEN 
    # WHEN LOADING IN A DEFAULT BOARD
    dev_mode = False
    chess = Chess(dev_mode, True)
#     chess.board.custom_board({
# 'a8':'br', 'b8':'wQ', 'c8':None, 'd8':None, 'e8':'bK', 'f8':'bR', 'g8':None, 'h8':'bR',
# 'a7':'bP', 'b7':None, 'c7':None, 'd7':None, 'e7':None, 'f7':None, 'g7':None, 'h7':None,
# 'a6':None, 'b6':None, 'c6':None, 'd6':None, 'e6':None, 'f6':None, 'g6':None, 'h6':None,
# 'a5':None, 'b5':'wP', 'c5':None, 'd5':None, 'e5':None, 'f5':None, 'g5':None, 'h5':None,
# 'a4':None, 'b4':None, 'c4':None, 'd4':None, 'e4':None, 'f4':None, 'g4':None, 'h4':None,
# 'a3':None, 'b3':None, 'c3':None, 'd3':None, 'e3':None, 'f3':None, 'g3':None, 'h3':None,
# 'a2':'wP', 'b2':'wP', 'c2':None, 'd2':None, 'e2':None, 'f2':'wP', 'g2':None, 'h2':None,
# 'a1':'wR', 'b1':None, 'c1':None, 'd1':None, 'e1':'wK', 'f1':None, 'g1':None, 'h1':'wR',
# })

    chess.board.custom_board({
'a8':'bR', 'b8':'bN', 'c8':'bB', 'd8':'None', 'e8':'bK', 'f8':'bB', 'g8':'bN', 'h8':'bR',
'a7':'bP', 'b7':'bP', 'c7':'bP', 'd7':'bP', 'e7':'None', 'f7':'bP', 'g7':'bP', 'h7':'bP',
'a6':'None', 'b6':'None', 'c6':'None', 'd6':'None', 'e6':'None', 'f6':'bQ', 'g6':'None', 'h6':'None',
'a5':'None', 'b5':'None', 'c5':'None', 'd5':'None', 'e5':'bP', 'f5':'None', 'g5':'None', 'h5':'None',
'a4':'None', 'b4':'None', 'c4':'None', 'd4':'None', 'e4':'wP', 'f4':'None', 'g4':'None', 'h4':'None',
'a3':'None', 'b3':'None', 'c3':'None', 'd3':'None', 'e3':'None', 'f3':'wQ', 'g3':'None', 'h3':'None',
'a2':'wP', 'b2':'wP', 'c2':'wP', 'd2':'wP', 'e2':'None', 'f2':'wP', 'g2':'wP', 'h2':'wP',
'a1':'wR', 'b1':'wN', 'c1':'wB', 'd1':'None', 'e1':'wK', 'f1':'wB', 'g1':'wN', 'h1':'wR',
})
    running = True
    while running:
        start = input("From: ")
        if start == 'exit':
            break
        if start =='print':
            chess.board.generate_preset()
        to = input("To: ")

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
        