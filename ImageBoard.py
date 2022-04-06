from PIL import Image
from Board import Board

class ImageBoard(Board):
    def __init__(self, board):
        super().__init__()
        self.path = 'assets/images/simple'
        self.generate_default()
        self.add_pieces(board)
        
    def generate_default(self):
        white = Image.open(f'{self.path}/squares/White.png')
        black = Image.open(f'{self.path}/squares/Black.png')
        width, height = 72, 72
        board = Image.new('RGB', (576, 576))
        
        for row in range(7):
            coord_square_path = f'{self.path}/squares/{8 - row}.png'
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
            coord_square_path = f'{self.path}/squares/{letters[column]}.png'
            coord_square = Image.open(coord_square_path)
            board.paste(coord_square, (width * column, height * 7))
        
        board.save(f'{self.path}/bg.png')
        
    def is_odd(self, num):
        return num % 2 == 1 
    def is_even(self, num):
        return num % 2 == 0
    
    def add_pieces(self, board):
        show = Image.open(f'{self.path}/bg.png')
        for key, value in board.items():
            if value != '__':
                piece_path = f'{self.path}/pieces/{value}.png'
                pos = self.pos_to_tup(key)
                piece = Image.open(piece_path)
                show.paste(piece, pos, piece)
        show.save(f'{self.path}/board.png')
        
    def pos_to_tup(self, pos):
        letters = 'abcdefgh'
        x = (letters.find(pos[0]))
        y = int(pos[1])
        x = 72*x + 9
        y = 576 - (72*y - 9)
        return (x, y)

if __name__ == '__main__':
    img = ImageBoard()
    img.add_pieces(img.board)
