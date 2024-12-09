# Wesley Tan
# COSC 76
# PA3: Chess AI

# Iterative Deepening using Minimax

import chess
import time

class IterativeDeepeningAI(): 
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

    def __init__(self, depth):
        self.max_depth = depth
        self.nodes_visited = 0
        self.time_limit = 10  # Default time limit in seconds

    def choose_move(self, board):
        """
        Entry point for selecting the best move using iterative deepening search.
        """
        self.start_time = time.time()
        
        best_move = self.minimax_decision(board)
        self.elapsed_time = time.time() - self.start_time
        print(f"Iterative Deepening AI recommending move {best_move}")
        print(f"Nodes visited: {self.nodes_visited}")
        print(f"Time taken: {self.elapsed_time:.2f} seconds")
        return best_move

    def minimax_decision(self, board):
        """
        Implements iterative deepening search using minimax algorithm.
        Searches progressively deeper until max depth or time limit is reached.
        
        Args:
            board (chess.Board): Current game state
        
        Returns:
            chess.Move: Best move found across all completed depth searches
        """
        overall_best_move = None
        
        # This is the iterative deepening loop
        for depth in range(1, self.max_depth + 1):
            self.nodes_visited = 0
            best_move = None
            best_value = float('-inf')
            
            # Search at current depth
            for move in board.legal_moves:
                board.push(move)
                value = -self.minimax(board, depth - 1, False)
                board.pop()
                
                if value > best_value:
                    best_value = value
                    best_move = move
                    
            if best_move:
                overall_best_move = best_move
                
            print(f"Depth {depth} completed. Best move: {best_move}")

            if time.time() - self.start_time > self.time_limit:
                print(f"Time limit reached. Stopping at depth {depth}")
                break

        return overall_best_move

    def minimax(self, board, depth, maximizing_player):
        """
        Recursive minimax implementation for game tree search.
        
        Args:
            board (chess.Board): Current game state
            depth (int): Remaining depth to search
            maximizing_player (bool): True if maximizing, False if minimizing
        
        Returns:
            float: Best evaluation score for the current position
        """
        self.nodes_visited += 1
        
        if self.cutoff_test(board, depth):
            return self.evaluate(board)

        if maximizing_player:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                value = max(value, self.minimax(board, depth - 1, False))
                board.pop()
            return value
        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self.minimax(board, depth - 1, True))
                board.pop()
            return value

    def cutoff_test(self, board, depth):
        """
        Determines if the search should stop at the current node.
        """
        # Cutoff conditions
        if depth == 0:
            return True
        if board.is_game_over():
            return True
        if time.time() - self.start_time > self.time_limit:
            return True
        return False

    def evaluate(self, board):
        """
        Evaluates the current board position using material count and position factors.
        
        Args:
            board (chess.Board): Current game state
        
        Returns:
            float: Evaluation score from White's perspective. Positive scores favor White,
                  negative scores favor Black. Larger absolute values indicate stronger
                  positions.
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
