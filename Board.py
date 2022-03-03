from Piece import *
#import pprint
#TO DO
# instead of passing color and name to class, pass as one string
class Board():
    """
    Put description of the Board class here
    """
    def __init__(self):
        self.prefix = 'abcdefgh'
        self.board = {}
        self.default_board()
        
    def default_board(self):
        for i in range(len(self.prefix)):
            for n in range(len(self.prefix)):
                self.board[f'{self.prefix[n]}{8-i}'] = '__'

        for key in self.board.keys():
            if key[1] == '2':
                self.board[key] = Pawn('w', key, 'P')

            elif key[1] == '7':
                self.board[key] = Pawn('b', key, 'P')

            elif key[1] == '1':
                if key[0] == 'a' or key[0] == 'h':
                    self.board[key] = Rook('w', key, 'R')

                elif key[0] == 'b' or key[0] == 'g':
                    self.board[key] = Knight('w', key, 'N')

                elif key[0] == 'c' or key[0] == 'f':
                    self.board[key] = Bishop('w', key, 'B')
                elif key[0] == 'd':
                    self.board[key] = Queen('w', key, 'Q') 

                elif key[0] == 'e':
                    self.board[key] = King('w', key, 'K') 
            
            elif key[1] == '8':
                if key[0] == 'a' or key[0] == 'h':
                    self.board[key] = Rook('b', key, 'R')

                elif key[0] == 'b' or key[0] == 'g':
                    self.board[key] = Knight('b', key, 'N')

                elif key[0] == 'c' or key[0] == 'f':
                    self.board[key] = Bishop('b', key, 'B')

                elif key[0] == 'd':
                    self.board[key] = Queen('b', key, 'Q') 

                elif key[0] == 'e':
                    self.board[key] = King('b', key, 'K') 
    def print_board(self):
        i = 1
        for key, value in self.board.items():
            if (i)%8 != 0:
                print(f'{key}:{value}', end=' ')
                i+=1
            else:
                print(f'{key}:{value}')
                i+=1
        
    def clear_board(self):
        for key in self.board.keys():
            self.board[key] = '__'

    def custom_board(self, preset):
        for key, value in preset.items():
            if value == '__':
                self.board[key] = '__'
            elif value[1] == 'P':
                self.board[key] = Pawn(value[0], key, value[1])
            elif value[1] == 'R':
                self.board[key] = Rook(value[0], key, value[1])
            elif value[1] == 'N':
                self.board[key] = Knight(value[0], key, value[1])
            elif value[1] == 'B':
                self.board[key] = Bishop(value[0], key, value[1])
            elif value[1] == 'Q':
                self.board[key] = Queen(value[0], key, value[1])
            elif value[1] == 'K':
                self.board[key] = King(value[0], key, value[1])
        print('Custom Board Loaded')

    def generate_preset(self):
        i = 1
        for key, value in self.board.items():
            if key == 'a8':
                print('{')
                print(f"'{key}':'{value.__str__()}',", end=' ')
                i+=1
            elif key == 'h1':
                print(f"'{key}':'{value.__str__()}',")
                print('}')
                i+=1
            elif (i)%8 != 0:
                print(f"'{key}':'{value.__str__()}',", end=' ')
                i+=1
            else:
                print(f"'{key}':'{value.__str__()}',")
                i+=1

# TO DO
# Have generate preset save to a file
# Have custom board pull from a file - if not there then pull from current board

