# TODO
# Function that converts position to a list of the x and y integers
class Piece():
    """
    Contains basic information about a piece
    Includes functions to whether it can move in certain ways
    Ex. diagonals or lines
    """
    move_counter = 1
    def __init__(self, color, pos, name):
        self.color = color
        self.pos = pos
        self.name = name
        self.letters = 'abcdefgh'

    @classmethod
    def update_counter(cls, counter):
        cls.move_counter = counter
    @classmethod
    def get_counter(cls):
        return cls.move_counter
    def update_pos(self, final):
        self.pos = final
   
    def can_replace(self, board, final):
        """Checks if the target location is either
        different color or empty space
        i.e. NOT the same color

        Args:
            board (dict): dictionary of the board
            final (str): final position in coordinates

        Returns:
            bool: Whether the current piece can move to final position
        """
        if board[final] == None:
            return True
        elif self.color != board[final].color:
            return True
        return False

    def x_diff(self, start, final):
        """Returns the difference between start and end x positions given two position pairs
        
        Args:
            start (str): start position in coordinates
            final (str): final position in coordinates

        Returns:
            int: final - start (Can be negative)
        """
        x1 = self.letters.index(start[0])
        x2 = self.letters.index(final[0])
        return x2 - x1

    def y_diff(self, start, final):
        """Returns the difference between start and end y positions given two position pairs
        
        Args:
            start (str): start position in coordinates
            final (str): final position in coordinates

        Returns:
            int: final - start (Can be negative)
        """
        y1 = int(start[1])
        y2 = int(final[1])
        return y2 - y1
    
    def abs_x_diff(self, start, final):
        return abs(self.x_diff(start, final))
    
    def abs_y_diff(self, start, final):
        return abs(self.y_diff(start, final))
    
    def x_unit(self, start, final):
        """Returns the i unit vector given initial and final positions

        Args:
            start (str): start position in coordinates
            final (str): final position in coordinates
            
        Returns:
            int: unit vector in the x direction
        """
        if self.x_diff(start, final) == 0:
            return 0
        return self.abs_x_diff(start, final) // self.x_diff(start, final)
    
    def y_unit(self, start, final):
        """Returns the j unit vector given initial and final positions

        Args:
            start (str): start position in coordinates
            final (str): final position in coordinates
            
        Returns:
            int: unit vector in the y direction
        """
        if self.y_diff(start, final) == 0:
            return 0
        return self.abs_y_diff(start, final) // self.y_diff(start, final)
    
    def add_vector(self, board, start, i = 0, j = 0):
        """Adds the i and j vectors to the start position

        Args:
            board (dict): board of position and pieces
            start (str): start position in coordinates
            i (int, optional): i vector to be applied. Defaults to 0.
            j (int, optional): j vector to be applied. Defaults to 0.

        Returns:
            str: position coordinate if it exists. Otherwise returns -1 if the coordinate is not in the board
        """
        x = self.letters.index(start[0]) + i
        y = int(start[1]) + j
        pos = self.letters[x] + str(y)
        if pos in board:
            return pos
        return -1
    
    def is_open_line(self, board, start, final):
        """ 
        Returns True if there are no obstructions in a straight line between start and final positions
        """
        i = self.x_unit(start, final)
        j = self.y_unit(start, final)
        
        # Same x column
        if start[0] == final[0]:
            for n in range(int(start[1]) + j, int(final[1]), j):
                if board[start[0] + str(n)] != None:
                    return False
            return True

        # Same y row
        elif start[1] == final[1]:
            for n in range(self.letters.index(start[0]) + i, self.letters.index(final[0]), i):
                if board[self.letters[n] + start[1]] != None:
                    return False
            return True
        return False

    def is_open_diagonal(self, board, start, final):
        """ 
        Returns True if there are no obstructions in a straight diagonal between start and final positions
        """
        if self.abs_x_diff(start, final) == self.abs_y_diff(start, final):
            i = self.x_unit(start, final) 
            j = self.y_unit(start, final)
            x1, y1 = self.letters.index(start[0]) + i, int(start[1]) + j
            x2, y2 = self.letters.index(final[0]), int(final[1])
            for i in range(self.abs_x_diff(start, final) - 1):
                if board[self.letters[x1] + str(y1)] != None:
                    return False   
                x1 += i
                y1 += j
            return True
        return False
   
    def escape(self, board):
        vector =[
                    [-1, 1], [0, 1], [1, 1],
                    [-1, 0],         [1, 0],
                    [-1,-1], [0,-1], [1,-1]
                ]

        ek = self.enemy_king(board)
        for v in vector:
            escape_pos = self.add_vector(board, ek.pos, i = v[0], j = v[1])
            if  escape_pos != -1:
                # valid = ek.is_valid_move(board, ek.pos, escape_pos)
                legal = ek.is_legal(board, ek.pos, escape_pos)
                # return valid and legal
                if legal:
                    return True
        return False
        
    def capture(self, board, final):
        for piece in self.enemy_pieces(board):
            valid = piece.is_valid_move(board, piece.pos, final)
            legal = piece.is_legal(board, piece.pos, final)
            if valid and legal:
                return True
        return False
    
    def block(self, board, final):
        # Find the diagonal / line from checking piece to king
        if board[final].name not in ['N', 'K']:
            king_pos = self.enemy_king(board).pos
            x_diff = self.abs_x_diff(final, king_pos)
            y_diff = self.abs_y_diff(final, king_pos)
            i = self.x_unit(final, king_pos)
            j = self.y_unit(final, king_pos)
            if x_diff > 1 or y_diff > 1:
                block_pos = final
                for n in range(max([x_diff - 1, y_diff - 1])):
                    block_pos = self.add_vector(board, block_pos, i = i, j = j)
                    for piece in self.enemy_pieces(board):
                        if piece.is_valid_move(board, piece.pos, block_pos) and piece.is_legal(board, piece.pos, block_pos):
                            return True
        return False
        
    def mate(self, board, final):
        if board[final].is_valid_move(board, final, self.enemy_king(board).pos):
            can_escape = self.escape(board)
            can_capture = self.capture(board, final)
            can_block = self.block(board, final)
            return not (can_escape or can_capture or can_block)
        return False
    
    def in_check(self, board):
        """ Checks if ally king is in check """
        for piece in self.enemy_pieces(board):
            if piece.is_valid_move(board, piece.pos, self.ally_king(board).pos):
                return True
        return False
    
    def is_legal(self, board, start, final): 
        # Or just copy.deepcopy(board)  
        temp = board[final]
        board[final] = board[start]
        board[start] = None
        board[final].update_pos(final)
        valid = self.in_check(board)
        
        board[start] = board[final]
        board[final] = temp
        board[start].update_pos(start)
        return not valid

    def all_pieces(self, board):
        return [value for value in board.values() if value != None]
    def enemy_pieces(self, board):
        return [value for value in self.all_pieces(board) if value.color != self.color]
    def ally_pieces(self, board):
        return [value for value in self.all_pieces(board) if value.color == self.color]
    def ally_king(self, board):
        return [value for value in self.ally_pieces(board) if value.name == 'K'][0]
    def enemy_king(self, board):
        return [value for value in self.enemy_pieces(board) if value.name == 'K'][0]
    
    def is_white(self):
        if self.color == 'w':
            return True
        return False
    
    def is_empty(self, piece):
        return piece == None 
    
    def __str__(self):
        return self.color + self.name
    
            

class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos, 'R')
        self.moves = 0
        
    def is_valid_move(self, board, start, final):
        return self.is_open_line(board, start, final)

class Knight(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos, 'N')

    def is_valid_move(self, board, start, final):
        """ 
        Checks if the start and end positions are offset by either
        1 in the x direction and 2 in the y direction
        OR 
        2 in the x direction or 1 in the y direction
        """
        return self.abs_x_diff(start, final) * self.abs_y_diff(start, final) == 2

class Bishop(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos, 'B')

    def is_valid_move(self, board, start, final):
        return self.is_open_diagonal(board, start, final)

class Queen(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos, 'Q')

    def is_valid_move(self, board, start, final):
        return self.is_open_line(board, start, final) or self.is_open_diagonal(board, start, final)

class King(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos, 'K')
        self.moves = 0

    def is_valid_move(self, board, start, final):
        x_diff = self.abs_x_diff(start, final)
        y_diff = self.abs_y_diff(start, final)
        if x_diff == 2 and y_diff == 0:
            if board[start].in_check(board) == False:
                if self.can_castle(board, start, final):
                    self.moves += 1
                    return True
        return x_diff < 2 and y_diff < 2
    
    def can_castle(self, board, start, final):
        if self.moves == 0:
            i = self.x_unit(start, final)
            rook_pos = self.rook_pos(board, start, final)
            next_pos = self.next_rook_pos(board, start, final)
            if self.is_valid_rook(board, rook_pos):
                # If castling queenside, need to know that the rook is not obstructed
                if board[rook_pos].is_valid_move(board, rook_pos, next_pos):
                    pos1 = self.add_vector(board, self.pos, i)
                    pos2 = self.add_vector(board, pos1, i)
                    if self.is_empty(board[pos1]) and self.is_empty(board[pos2]):
                        if self.is_legal(board, self.pos, pos1) and self.is_legal(board, self.pos, pos2):
                            return True
        return False
    def rook_pos(self, board, start, final):
        # Returns position of the rook used for castling in the target direction
        i = board[start].x_unit(start, final) 
        if i < 0:
            pos = 'a' + start[1]
        elif i > 0:
            pos = 'h' + start[1]
        return pos

    def next_rook_pos(self, board, start, final):
        # Returns position of the rook used for castling in the target direction BUT SHIFTED ONE UNIT AWAY
        # Ex. b8, g1
        i = board[start].x_unit(start, final) 
        if i < 0:
            pos = 'b' + self.pos[1]
        elif i > 0:
            pos = 'g' + self.pos[1]
        return pos

    def castled_rook_pos(self, board, start, final):
        # Returns position of the rook after castling
        i = board[start].x_unit(start, final)  
        if i > 0:
            pos = 'f' + self.pos[1]
        elif i < 0:
            pos = 'd' + self.pos[1]
        return pos

    def is_valid_rook(self, board, pos):
        if board[pos] != None:
            # Can probably assume that the rook is an ally rook
            # Since is_legal is checked
            # But failsafe
            if board[pos].__str__() == self.color + 'R':
                return board[pos].moves == 0
        return False

class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos, 'P')
        self.moves = 0
        self.last_move = 1
    def is_valid_move(self, board, start, final):
        """ 
        Returns True if the Pawn can occupy it
        Just read the comments - too many conditionals
        """
        i = self.x_unit(start, final)
        j = self.y_unit(start, final)

        # Only if the move is valid, is the self.move counter updated
        valid = False

        if self.correct_direction(start, final):
            if self.is_diagonal(start, final):
                # Checks if target location contains an enemy piece
                if not self.is_empty(board[final]):
                    valid = True
                # EN PASSENTE
                # If target location is empty, checks for an enemy pawn adjacent that just moved two units
                # LOL ITS SO BAD
                else:
                    adj_pos = self.add_vector(board, start, i)
                    adj = board[adj_pos]
                    if adj.name == "P" and adj.color != self.color:
                        # If the Pawn moved in the last move, replace the pawn with an empty space
                        valid = Piece.get_counter() - adj.last_move == 1
                        if valid:
                            board[adj_pos] = None
            # Checks that the move does not move in the horizontal direction at all
            elif self.abs_x_diff(start, final) == 0:
                # Checks if the target location is empty for 1 unit moves
                if self.abs_y_diff(start, final) == 1:
                    valid = self.is_empty(board[final])
                # Checks if the target location is empty and path is unobstructed for 2 unit moves
                elif self.abs_y_diff(start, final) == 2:
                    # OR can just run line() final see if middle square is free
                    middle = self.add_vector(board, start, j = j)
                    if self.is_empty(board[middle]):
                        valid = self.moves == 0
        if valid:
            self.moves += 1
            self.last_move = Piece.get_counter()
        return valid
    
    def correct_direction(self, start, final):
        # Checks if white/black is moving up/down the board
        j = self.y_unit(start, final)
        if j > 0:
            return self.color == 'w'
        if j < 0:
            return self.color == 'b' 
        return False
    def is_diagonal(self, start, final):
        # Checks if target location is one diagonal away
        return self.abs_x_diff(start, final) * self.abs_y_diff(start, final) == 1


