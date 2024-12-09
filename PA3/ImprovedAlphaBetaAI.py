# Wesley Tan
# COSC 76
# PA3: Chess AI

import chess
import time
from math import inf

# Constants for piece values
PAWN_VALUE = 100
KNIGHT_VALUE = 320
BISHOP_VALUE = 330
ROOK_VALUE = 500
QUEEN_VALUE = 900
KING_VALUE = 99999

# Constants for move ordering
CAPTURE_BONUS = 100
PROMOTION_BONUS = 90
CHECK_BONUS = 50
MOBILITY_MULTIPLIER = 10
CHECK_PENALTY = 50

class ImprovedAlphaBetaAI():
    def __init__(self, depth, time_limit=10):
        self.max_depth = depth
        self.nodes_visited = 0
        self.time_limit = time_limit
        self.transposition_table = {}  # Store positions and their evaluations
        self.move_history = {}  # Store move scores from previous iterations
        self.start_time = None

    def choose_move(self, board):
        self.nodes_visited = 0
        self.start_time = time.time()
        best_move = None
        best_value = float('-inf')
        
        # Iterative Deepening
        for current_depth in range(1, self.max_depth + 1):
            alpha = float('-inf')
            beta = float('inf')
            
            # Search at current depth
            for move in self.order_moves(board):
                if time.time() - self.start_time > self.time_limit:
                    break
                    
                board.push(move)
                value = self.alpha_beta(board, current_depth - 1, alpha, beta, False)
                board.pop()
                
                # Update move history with the score
                self.update_move_history(move, value, current_depth)
                
                if value > best_value:
                    best_value = value
                    best_move = move
                    
                alpha = max(alpha, best_value)
            
            print(f"Completed depth {current_depth}")
            if time.time() - self.start_time > self.time_limit:
                break
        
        elapsed_time = time.time() - self.start_time
        print(f"ImprovedAlphaBeta AI recommending move {best_move}")
        print(f"Nodes visited: {self.nodes_visited}")
        print(f"Time taken: {elapsed_time:.2f} seconds")
        return best_move

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        self.nodes_visited += 1
        
        if time.time() - self.start_time > self.time_limit:
            return None
        
        board_key = str(board)
        
        if board_key in self.transposition_table:
            cached_depth, cached_value = self.transposition_table[board_key]
            if cached_depth >= depth:
                return cached_value
        
        if depth == 0 or board.is_game_over():
            value = self.evaluate_board(board)
            self.transposition_table[board_key] = (depth, value)
            return value
        
        moves = self.order_moves(board)
        if maximizing_player:
            value = float('-inf')
            for move in moves:
                board.push(move)
                value = max(value, self.alpha_beta(board, depth - 1, alpha, beta, False))
                board.pop()
                
                if value is None:
                    return None
                    
                alpha = max(alpha, value)
                if beta <= alpha:
                    self.update_move_history(move, value, depth)
                    break
            self.transposition_table[board_key] = (depth, value)
            return value
        else:
            value = float('inf')
            for move in moves:
                board.push(move)
                value = min(value, self.alpha_beta(board, depth - 1, alpha, beta, True))
                board.pop()
                
                if value is None:
                    return None
                    
                beta = min(beta, value)
                if beta <= alpha:
                    self.update_move_history(move, value, depth)
                    break
            self.transposition_table[board_key] = (depth, value)
            return value

    def evaluate_board(self, board):
        if board.is_checkmate():
            return -inf if board.turn else inf
        elif board.is_stalemate():
            return 0
        
        piece_values = {
            chess.PAWN: PAWN_VALUE,
            chess.KNIGHT: KNIGHT_VALUE,
            chess.BISHOP: BISHOP_VALUE,
            chess.ROOK: ROOK_VALUE,
            chess.QUEEN: QUEEN_VALUE,
            chess.KING: KING_VALUE
        }
        
        score = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color == chess.WHITE else -value
        
        # Mobility is the number of legal moves available to the player
        mobility = len(list(board.legal_moves))
        score += mobility * MOBILITY_MULTIPLIER if board.turn == chess.WHITE else -mobility * MOBILITY_MULTIPLIER
        
        # King safety
        if board.is_check():
            score += -CHECK_PENALTY if board.turn == chess.WHITE else CHECK_PENALTY
        
        return score

    def order_moves(self, board):
        def move_value(move):
            score = 0
            
            # Basic move ordering: captures, promotions, checks
            if board.is_capture(move):
                score += CAPTURE_BONUS
            if move.promotion:
                score += PROMOTION_BONUS
            if board.gives_check(move):
                score += CHECK_BONUS
            
            # History heuristic
            move_str = move.uci()
            if move_str in self.move_history:
                score += self.move_history[move_str] / 100
            
            return score
        
        return sorted(board.legal_moves, key=move_value, reverse=True)

    def update_move_history(self, move, value, depth):
        move_str = move.uci()
        if move_str not in self.move_history:
            self.move_history[move_str] = 0
        self.move_history[move_str] += 2 ** depth  # Exponential depth bonus
