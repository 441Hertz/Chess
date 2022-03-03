import string
letters = string.ascii_lowercase
class Piece():
    """
    Contains basic information about a piece
    Includes functions to whether it can move in certain ways
    Ex. diagonals or lines
    """
    move_counter = 1
    def __init__(self, color, position, name):
        self.color = color
        self.position = position
        self.name = name

    @classmethod
    def update_counter(cls, counter):
        cls.move_counter = counter
    @classmethod
    def get_counter(cls):
        return cls.move_counter
    def pos(self):
        return self.position
    def update_pos(self, to):
        self.position = to
    def is_valid_move(self):
        return False

    def is_white(self):
        if self.color == 'w':
            return True
        return False

    def __str__(self):
        # replace the body and return a string with how you want your piece
        # to be printed as when `print([A Piece Object])` is called
        return self.color + self.name
    def get_name(self):
        return self.name
    def get_col(self):
        return self.color

    def replaceable(self, board, to):
        """ 
        Checks if the target location is either
        different color or empty space
        i.e. NOT the same color
        """
        
       
        if board[to] == '__':
            return True
        elif self.get_col() != board[to].get_col():
            return True
        return False

    #Could change to static methods
    # Also call it dx?
    def x_diff(self, start, to):
        """
        Returns the difference between start and end x coordinates
        given two coordinate pairs
        Can be negative
        """
        x1 = letters.index(start[0])
        x2 = letters.index(to[0])
        return x2 - x1

    def y_diff(self, start, to):
        """
        Returns the difference between start and end y coordinates
        given two coordinate pairs
        Can be negative
        """
        y1 = int(start[1])
        y2 = int(to[1])
        return y2 - y1

    def unit_vector(self, start, to):
        """
        Returns the i and j unit vectors given 
        initial and final coordinates
        as a dictionary
        """
        # Divide by zero protection
        i, j = 0, 0

        if self.x_diff(start, to) != 0:
            x_ab = abs(self.x_diff(start, to))
            i = x_ab // self.x_diff(start, to)

        if self.y_diff(start, to) != 0:
            y_ab = abs(self.y_diff(start, to))
            j = y_ab // self.y_diff(start, to)

        return {'i':i, 'j':j}

    def line(self, board, start, to):
        """ 
        Returns True if the piece can move to the target location
        in a straight line
        """
        i, j = self.unit_vector(start, to)['i'], self.unit_vector(start, to)['j']
        
        if self.replaceable(board, to):
            if start[0] == to[0]:
                for n in range(int(start[1]) + j, int(to[1]) + j, j):
                    if start[0] + str(n) == to:
                        return True
                    elif board[start[0] + str(n)] != '__':
                        return False

            elif start[1] == to[1]:
                for n in range(letters.index(start[0]) + i, letters.index(to[0]) + i, i):
                    if letters[n] + start[1] == to:
                        return True
                    elif board[letters[n] + start[1]] != '__':
                        return False
        return False

    def diagonal(self, board, start, to):
        """ 
        Returns True if the piece can move to the target location
        in a diagonal
        """
        if self.replaceable(board, to):
            if abs(self.x_diff(start, to)) == abs(self.y_diff(start, to)):
                i, j = self.unit_vector(start, to)['i'], self.unit_vector(start, to)['j']
                x1, y1 = letters.index(start[0]) + i, int(start[1]) + j
                x2, y2 = letters.index(to[0]), int(to[1])
                while True:
                    if x1 == x2 and y1 == y2:
                       return True
                    elif board[letters[x1] + str(y1)] != '__':
                        return False   
                    x1 += i
                    y1 += j
        return False
    def apply_unit_vector(self, board, start, i, j):
        """
        Returns coordinates of the i and j vectors applied to start coordinate
        as a string
        Returns -1 if the resultant coordinate is invalid
        TODO apply this method to other methods
        """
        x = letters.index(start[0]) + i
        y = int(start[1]) + j
        coord = letters[x] + str(y)
        if coord in board:
            return coord
        return -1
    def all_pieces(self, board):
        return [value for value in board.values() if value != '__']
    def enemy_pieces(self, board):
        return [value for value in self.all_pieces(board) if value.get_col() != self.get_col()]
    def ally_pieces(self, board):
        return [value for value in self.all_pieces(board) if value.get_col() == self.get_col()]
    def ally_king(self, board):
        return [value for value in self.ally_pieces(board) if value.get_name() == 'K'][0]
    def enemy_king(self, board):
        return [value for value in self.enemy_pieces(board) if value.get_name() == 'K'][0]
    def escape(self, board):
        vector =[
                    [-1, 1], [0, 1], [1, 1],
                    [-1, 0],         [1, 0],
                    [-1,-1], [0,-1], [1,-1]
                ]

        for v in vector:
            escape_coord = self.apply_unit_vector(board, self.enemy_king(board).pos(), v[0], v[1])
            if  escape_coord != -1:
                valid = self.enemy_king(board).is_valid_move(board, self.enemy_king(board).pos(), escape_coord)
                legal = self.enemy_king(board).is_legal(board, self.enemy_king(board).pos(), escape_coord)
                if valid and legal :
                    return True
        return False
        
    def capture(self, board, to):
        for piece in self.enemy_pieces(board):
            valid = piece.is_valid_move(board, piece.pos(), to)
            legal = piece.is_legal(board, piece.pos(), to)
            if valid and legal:
                return True
        return False
    def block(self, board, to):
        # Find the diagonal / line from checking piece to king
        # Done via 
        if board[to].get_name() not in ['N', 'K']:
            x_diff = self.x_diff(to, self.enemy_king(board).pos())
            y_diff = self.y_diff(to, self.enemy_king(board).pos())
            i, j = self.unit_vector(to, self.enemy_king(board).pos())['i'], self.unit_vector(to, self.enemy_king(board).pos())['j']
            if abs(x_diff) > 1 or abs(y_diff) > 1:
                block_coord = to
                for n in range(max([abs(x_diff) - 1, abs(y_diff) - 1])):
                    block_coord = self.apply_unit_vector(board, block_coord, i, j)
                    for piece in self.enemy_pieces(board):
                        if piece.is_valid_move(board, piece.pos(), block_coord) and piece.is_legal(board, piece.pos(), block_coord):
                            return True
        return False
        #check all enemy pieces to see if they can move to the line of sight
    def mate(self, board, to):
        if board[to].is_valid_move(board, to, self.enemy_king(board).pos()):
            print(self.escape(board), self.capture(board, to), self.block(board, to))
            return not (self.escape(board) or self.capture(board, to) or self.block(board, to))
        return False
    def is_legal(self, board, start, to): 
        # Or just copy.deepcopy(board)  
        temp = board[to]
        board[to] = board[start]
        board[start] = '__'
        board[to].update_pos(to)
        valid = True

        for piece in self.enemy_pieces(board):
            # print(piece, self.ally_king(board).pos(), board[start], board[to])
            if piece.is_valid_move(board, piece.pos(), self.ally_king(board).pos()):
                valid = False

        board[start] = board[to]
        board[to] = temp
        board[start].update_pos(start)
        return valid

            

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, 'R')
        self.moves = 0
    def is_valid_move(self, board, start, to):
        return self.line(board, start, to)

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, 'N')

    def is_valid_move(self, board, start, to):
        """ 
        Checks if the start and end positions are offset by either
        1 in the x direction and 2 in the y direction
        OR 
        2 in the x direction or 1 in the y direction
        """
        if self.replaceable(board, to): 
            return abs(self.x_diff(start, to) * self.y_diff(start, to)) == 2
        return False

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, 'B')

    def is_valid_move(self, board, start, to):
        return self.diagonal(board, start, to)

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, 'Q')

    def is_valid_move(self, board, start, to):
        return self.line(board, start, to) or self.diagonal(board, start, to)

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, 'K')
        self.moves = 0

    def is_valid_move(self, board, start, to):
        if self.replaceable(board, to): 
            if self.can_castle(board, to):
                self.apply_unit_vector(board, self.pos(), self.x_diff(self.pos(), to), 0)
                self.moves += 1
                return True
            return abs(self.x_diff(start, to)) < 2 and abs(self.y_diff(start, to)) < 2
        return False
    
    def can_castle(self, board, to):
        if self.moves == 0:
            i = self.unit_vector(self.pos(), to)['i']
            if i < 0:
                rook_coord = 'a' + self.pos()[1]
                intermediate_coord = 'b' + self.pos()[1]
            elif i > 0:
                rook_coord = 'h' + self.pos()[1]
                intermediate_coord = 'g' + self.pos()[1]
            elif i == 0:
                return False
            if board[rook_coord] != '__':
                if board[rook_coord].__str__() == self.get_col() + 'R':
                    if board[rook_coord].moves == 0:
                        if abs(self.x_diff(self.pos(), to)) == 2 and self.y_diff(self.pos(), to) == 0:
                            if board[rook_coord].is_valid_move(board, rook_coord, intermediate_coord):
                                temp_coord = self.apply_unit_vector(board, self.pos(), i, 0)
                                bandaid = False
                                for n in range(2):
                                    valid = self.is_valid_move(board, self.pos(), temp_coord)
                                    legal = self.is_legal(board, self.pos(), temp_coord)
                                    if valid and legal:

                                        board[temp_coord] = board[self.pos()]
                                        board[self.pos()] = '__'
                                        self.update_pos(temp_coord)
                                        temp_coord = self.apply_unit_vector(board, temp_coord, i, 0)
                                        bandaid = True
                                    else:
                                        bandaid = False
                                        board['e' + self.pos()[1]] = board[self.pos()]
                                        board[self.pos()] == '__'
                                        self.update_pos('e' + self.pos()[1])
                                if bandaid:
                                    castled_rook_coord = self.apply_unit_vector(board, self.pos(), -i, 0)
                                    board[rook_coord].moves += 1
                                    board[castled_rook_coord] = board[rook_coord]
                                    board[castled_rook_coord].update_pos(castled_rook_coord)
                                    board[rook_coord] = '__'
                                    
                                return bandaid
                                        
                                
                            # TODO 
                            # Check if the back row is empty
                            # Check if it is legal
                            # and that it does not "go through checks"
                            # dont have to check for legal moves for the rook
        return False

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, 'P')
        self.moves = 0
        self.last_move = 1
    def is_valid_move(self, board, start, to):
        """ 
        Returns True if the Pawn can occupy it
        Just read the comments - too many conditionals
        """
        j = self.unit_vector(start, to)['j']

        # Checks if white is moving up the board or if black is moving down the board
        correct_direction = False
        if self.get_col() == 'w' and j > 0:
            correct_direction = True
        if self.get_col() == 'b' and j < 0:
            correct_direction = True

        # Only if the move is valid, is the self.move counter updated
        valid = False

        if self.replaceable(board, to) and correct_direction:
            # Checks if target location is one diagonal away
            if abs(self.x_diff(start, to) * self.y_diff(start, to)) == 1:
                # Checks if target location contains an enemy piece
                if board[to] != '__':
                    valid = True
                # EN PASSENTE
                # If target location is empty, checks for an enemy pawn adjacent that just moved two units
                # LOL ITS SO BAD
                else:
                    adj_index = letters.index(start[0]) + self.x_diff(start, to)
                    adj_coord = letters[adj_index] + start[1]
                    adj = board[adj_coord]
                    if adj.get_name() == "P" and adj.get_col() != self.get_col():
                        valid = Piece.get_counter() - self.last_move == 1
                        # I dont like that im removing a piece in this class
                        # wait how am i able to change this board here?
                        if valid == True:
                            board[adj_coord] = '__'
            # Checks if move is forward or backward
            elif abs(self.x_diff(start, to)) == 0:
                # Checks if the target location is empty for 1 unit moves
                if abs(self.y_diff(start, to)) == 1:
                    valid = board[to] == '__'
                # Checks if the target location is empty and path is unobstructed for 2 unit moves
                elif abs(self.y_diff(start, to)) == 2:
                    # OR can just run line() to see if middle square is free
                    middle = int(start[1]) + j
                    if board[to[0] + str(middle)] == '__':
                        valid = self.moves == 0
        if valid:
            self.moves += 1
            self.last_move = Piece.get_counter()
        return valid
