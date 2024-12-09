# Wesley Tan
# COSC 76
# PA3: Chess AI

import chess
import time
from math import inf

class AlphaBetaAI():
    # Constants for evaluation
    PAWN_VALUE = 1
    KNIGHT_VALUE = 3
    BISHOP_VALUE = 3
    ROOK_VALUE = 5
    QUEEN_VALUE = 9
    KING_VALUE = 99999
    CENTRAL_PAWN_BONUS = 20
    MOBILITY_BONUS = 0.1
    CHECK_PENALTY = 50
    CAPTURE_MOVE_VALUE = 10
    CHECK_MOVE_VALUE = 5

    def __init__(self, depth, time_limit=10):
        self.max_depth = depth
        self.nodes_visited = 0
        self.time_limit = time_limit

    def choose_move(self, board):
        """
        Selects the best move for the current position using alpha-beta pruning.
        
        Args:
            board (chess.Board): Current game state
            
        Returns:
            chess.Move: Best move found within the search parameters
        """

        self.nodes_visited = 0
        start_time = time.time()
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Count the root node
        self.nodes_visited += 1
        
        for move in self.order_moves(board):
            self.nodes_visited += 1
            board.push(move)
            value = self.alpha_beta(board, self.max_depth - 1, alpha, beta, False)
            board.pop()

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, best_value)

        elapsed_time = time.time() - start_time
        print(f"AlphaBeta AI recommending move {best_move}")
        print(f"Nodes visited: {self.nodes_visited}")
        print(f"Time taken: {elapsed_time:.2f} seconds")
        return best_move
  
    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        """
        Implements the alpha-beta pruning algorithm for game tree search.
        
        Args:
            board (chess.Board): Current game state
            depth (int): Remaining depth to search
            alpha (float): Best value found for maximizing player
            beta (float): Best value found for minimizing player
            maximizing_player (bool): True if maximizing, False if minimizing
            
        Returns:
            float: Best evaluation score for the current position
        """

        self.nodes_visited += 1
        
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)
        
        if maximizing_player:
            value = float('-inf')
            for move in self.order_moves(board):
                board.push(move)
                value = max(value, self.alpha_beta(board, depth - 1, alpha, beta, False))
                board.pop()
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Pruning happens here
            return value
        else:
            value = float('inf')
            for move in self.order_moves(board):
                board.push(move)
                value = min(value, self.alpha_beta(board, depth - 1, alpha, beta, True))
                board.pop()
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def evaluate_board(self, board):
        """
        Evaluates the current board position using material count and positional factors.
        
        Args:
            board (chess.Board): Current game state
            
        Returns:
            float: Evaluation score from White's perspective. Positive scores favor White,
                  negative scores favor Black. Larger absolute values indicate stronger positions.
                  
        Features considered:
            - Material count (piece values)
            - Central pawn control
            - Mobility (number of legal moves)
            - King safety (check status)
        """

        if board.is_checkmate():
            return float('-inf') if board.turn == chess.WHITE else float('inf')
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            return 0
        
        piece_values = {
            chess.PAWN: self.PAWN_VALUE, chess.KNIGHT: self.KNIGHT_VALUE, chess.BISHOP: self.BISHOP_VALUE,
            chess.ROOK: self.ROOK_VALUE, chess.QUEEN: self.QUEEN_VALUE, chess.KING: self.KING_VALUE
        }
        
        score = 0
        
        # Material and position evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                    # Bonus for central pawns
                    if piece.piece_type == chess.PAWN and square in [chess.D4, chess.E4, chess.D5, chess.E5]:
                        score += self.CENTRAL_PAWN_BONUS
                else:
                    score -= value
                    if piece.piece_type == chess.PAWN and square in [chess.D5, chess.E5, chess.D4, chess.E4]:
                        score -= self.CENTRAL_PAWN_BONUS
        
        mobility_score = len(list(board.legal_moves))
        score += self.MOBILITY_BONUS * mobility_score  # Small bonus for mobility
        
        # King safety 
        if board.is_check():
            score += -self.CHECK_PENALTY if board.turn == chess.WHITE else self.CHECK_PENALTY
        
        return score if board.turn == chess.WHITE else -score

    def order_moves(self, board):
        """
        Orders moves to improve alpha-beta pruning efficiency.
        """

        def move_value(move):
            if board.is_capture(move):
                return self.CAPTURE_MOVE_VALUE
            elif board.gives_check(move):
                return self.CHECK_MOVE_VALUE
            else:
                return 0

        return sorted(board.legal_moves, key=move_value, reverse=True)
