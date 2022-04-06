from PIL import Image
from Board import Board

class ImageBoard(Board):
    def __init__(self, board = None):
        super().__init__()
        self.path = 'assets/images/simple/'
        self.generate_empty()
        if board is not None:
            self.board = board
        self.generate_image(self.board)
        
    def generate_empty(self):
        white = Image.open(self.path + 'squares/White.png')
        black = Image.open(self.path + 'squares/Black.png')
        width, height = 72, 72
        board = Image.new('RGB', (576, 576))
        
        for row in range(7):
            coord_square_path = self.path + f'squares/{8 - row}.png'
            coord_square = Image.open(coord_square_path)
            board.paste(coord_square, (0, height * row))
            for column in range(1, 8):
                if self.is_even(row + column):
                    square = white
                else:
                    square = black
                board.paste(square, (width * column, height * row))
                
        letters = 'ABCDEFGH'
        for column in range(8):
            coord_square_path = self.path + f'squares/{letters[column]}.png'
            coord_square = Image.open(coord_square_path)
            board.paste(coord_square, (width * column, height * 7))
        
        board.save(self.path + 'empty.png')
    
    
    def generate_image(self, board):
        show = Image.open(self.path + 'empty.png')
        for key, value in board.items():
            if value != '__':
                piece_path = self.path + f'pieces/{value}.png'
                pos = self.pos_to_tup(key)
                piece = Image.open(piece_path)
                show.paste(piece, pos, piece)
        show.save(self.path + 'board.png')
        
    def pos_to_tup(self, pos):
        letters = 'abcdefgh'
        x = (letters.find(pos[0]))
        y = int(pos[1])
        x = 72*x + 9
        y = 576 - (72*y - 9)
        return (x, y)
    
    def is_odd(self, num):
        return num % 2 == 1 
    def is_even(self, num):
        return num % 2 == 0
    
if __name__ == '__main__':
    img = ImageBoard()
