from Board import Board
from Piece import *
class Chess():
    """
    Put description of the Chess class here
    """

    def __init__(self, dev_mode = False):
        # replace `pass` with the desired attributes and add any 
        # additional parameters to the function  
        self.board = Board()
        self.board.print_board()
        self.move_counter = 1
        self.dev_mode = dev_mode
    def promotion(self):
        # add any parameters necessary and replace the body with
        # functionality on promoting a Pawn that has reached the 
        # end of the board
        pass
    def whose_move(self):
        if self.move_counter % 2 == 1:
            return ('w', 'white')
        return ('b', 'black')
    def which_move(self):
        return (self.move_counter + 1) // 2
    def correct_turn(self, start):
        if not self.dev_mode:
            return self.board.board[start].get_color() == self.whose_move()[0]
        return True
    def is_piece(self, start):
        return self.board.board[start] != '__'
    def valid_coordinate(self, start):
        # Breaks if y coordinate is a string + probably more
        # Also only checks for the start coordinate - not the to coord
        valid_x = start[0] in 'abcdefgh'
        valid_y = int(start[1]) < 9
        return valid_x and valid_y
    def update_counter(self):
        self.move_counter += 1
        Piece.update_counter(self.move_counter)
    def move(self, start, to):
        # TODO : ghost board? -theres some redundancy in updating the logic board and visual board
        """ 
        What an absolute mess
        """
        board = self.board.board
        print("---------------------------------------------------------------")
        if self.valid_coordinate(start) and self.is_piece(start):
            if self.correct_turn(start):
                valid = board[start].is_valid_move(board, start, to)
                legal = board[start].is_legal(board, start, to)
                if valid: 
                    if legal:
                        print(board[start].__str__() + f' moved from {start} to {to}')
                        board[to] = board[start]
                        board[start] = '__'
                        board[to].update_position(to)
                        self.update_counter()
                        if board[to].mate(board, to):
                            print('Checkmate!')
                    else:
                        print(f"Invalid Move: {start} to {to} \nMove is not legal!")
                else:
                    print(f"Invalid Move: {start} to {to} \nRead the rules!")
            else:
                print(f"Invalid Move: {start} to {to} \nIt's {self.whose_move()[1]}'s turn!")
        else:
            print(f"Invalid Move: {start} to {to} \nInvalid coordinates or empty space")
        self.board.print_board()
        print("---------------------------------------------------------------")
def translate(position):
    return position

if __name__ == "__main__":
    chess = Chess(dev_mode = True)
#     chess.board.custom_board({
# 'a8':'__', 'b8':'wR', 'c8':'__', 'd8':'__', 'e8':'__', 'f8':'__', 'g8':'__', 'h8':'wQ',
# 'a7':'__', 'b7':'__', 'c7':'__', 'd7':'__', 'e7':'__', 'f7':'bP', 'g7':'__', 'h7':'__',
# 'a6':'__', 'b6':'__', 'c6':'__', 'd6':'__', 'e6':'__', 'f6':'__', 'g6':'__', 'h6':'__',
# 'a5':'__', 'b5':'__', 'c5':'bR', 'd5':'__', 'e5':'bB', 'f5':'__', 'g5':'__', 'h5':'__',
# 'a4':'__', 'b4':'bQ', 'c4':'__', 'd4':'__', 'e4':'__', 'f4':'bQ', 'g4':'bP', 'h4':'__',
# 'a3':'bK', 'b3':'bP', 'c3':'wQ', 'd3':'bN', 'e3':'__', 'f3':'__', 'g3':'__', 'h3':'__',
# 'a2':'wP', 'b2':'__', 'c2':'__', 'd2':'__', 'e2':'bQ', 'f2':'wQ', 'g2':'__', 'h2':'wP',
# 'a1':'__', 'b1':'__', 'c1':'__', 'd1':'__', 'e1':'__', 'f1':'__', 'g1':'__', 'h1':'wK',
# })
    chess.board.custom_board({
'a8':'__', 'b8':'__', 'c8':'__', 'd8':'__', 'e8':'__', 'f8':'__', 'g8':'__', 'h8':'bK',
'a7':'__', 'b7':'__', 'c7':'__', 'd7':'__', 'e7':'__', 'f7':'__', 'g7':'__', 'h7':'__',
'a6':'__', 'b6':'__', 'c6':'__', 'd6':'__', 'e6':'__', 'f6':'__', 'g6':'__', 'h6':'__',
'a5':'__', 'b5':'__', 'c5':'__', 'd5':'__', 'e5':'__', 'f5':'__', 'g5':'__', 'h5':'__',
'a4':'__', 'b4':'__', 'c4':'__', 'd4':'__', 'e4':'__', 'f4':'__', 'g4':'__', 'h4':'__',
'a3':'__', 'b3':'__', 'c3':'__', 'd3':'__', 'e3':'__', 'f3':'__', 'g3':'__', 'h3':'__',
'a2':'wP', 'b2':'wP', 'c2':'__', 'd2':'bQ', 'e2':'__', 'f2':'__', 'g2':'__', 'h2':'__',
'a1':'wK', 'b1':'__', 'c1':'__', 'd1':'__', 'e1':'__', 'f1':'__', 'g1':'__', 'h1':'__',
})
    chess.move('d2', 'd1')

    
    # while True:
        # start = input("From: ")
        # to = input("To: ")
        
        # #translate is a helper method to turn the user input into
        # #a representation depending on how the board is represented
        
        # start = translate(start)
        # to = translate(to)

        # if start == None or to == None:
        #     continue

        # chess.move(start, to)

        # # check for promotion pawns
        # i = 0
        # while i < 8:
        #     if not chess.turn and chess.board.board[0][i] != None and \
        #         chess.board.board[0][i].name == 'P':
        #         chess.promotion((0, i))
        #         break
        #     elif chess.turn and chess.board.board[7][i] != None and \
        #         chess.board.board[7][i].name == 'P':
        #         chess.promotion((7, i))
        #         break
        #     i += 1

        # chess.board.print_board()