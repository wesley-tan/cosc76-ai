# Wesley Tan
# COSC 76
# PA3: Chess AI

import chess
import chess.engine
import math
import time

class QuiescenceAI:
    # Define constants for magic numbers
    CHECKMATE_SCORE = 10000
    STALEMATE_SCORE = 0
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 99999
    }
    CENTRAL_PAWN_BONUS = 20
    MOBILITY_MULTIPLIER = 10
    CHECK_PENALTY = 50
    MOVE_CAPTURE_VALUE = 10
    MOVE_CHECK_VALUE = 5
    MOVE_PROMOTION_VALUE = 4

    def __init__(self, depth=3, time_limit=10):
        self.depth = depth
        self.nodes_visited = 0
        self.time_limit = time_limit
        self.start_time = 0
        self.transposition_table = {}

    def evaluate(self, board):
        if board.is_checkmate():
            return -self.CHECKMATE_SCORE if board.turn else self.CHECKMATE_SCORE
        if board.is_stalemate() or board.is_insufficient_material():
            return self.STALEMATE_SCORE

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.PIECE_VALUES[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                    # Bonus for central pawns
                    if piece.piece_type == chess.PAWN and square in [chess.D4, chess.E4, chess.D5, chess.E5]:
                        score += self.CENTRAL_PAWN_BONUS
                else:
                    score -= value
                    if piece.piece_type == chess.PAWN and square in [chess.D5, chess.E5, chess.D4, chess.E4]:
                        score -= self.CENTRAL_PAWN_BONUS

        # Mobility
        score += self.MOBILITY_MULTIPLIER * (len(list(board.legal_moves)) - len(list(board.generate_legal_moves())))

        if board.is_check():
            score += -self.CHECK_PENALTY if board.turn == chess.WHITE else self.CHECK_PENALTY

        return score if board.turn == chess.WHITE else -score

    def quiescence_search(self, board, alpha, beta, depth=0, max_depth=3):
        self.nodes_visited += 1
        stand_pat = self.evaluate(board)

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        if depth >= max_depth:
            return stand_pat

        for move in self.order_moves(board):
            if board.is_capture(move) or board.gives_check(move) or move.promotion:
                board.push(move)
                score = -self.quiescence_search(board, -beta, -alpha, depth + 1, max_depth)
                board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

        return alpha

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        self.nodes_visited += 1

        # Check time limit
        if time.time() - self.start_time > self.time_limit:
            return None

        # Transposition table lookup
        key = board.fen()
        if key in self.transposition_table and self.transposition_table[key][1] >= depth:
            return self.transposition_table[key][0]

        if depth == 0:
            return self.quiescence_search(board, alpha, beta)

        if maximizing_player:
            max_eval = -math.inf
            for move in self.order_moves(board):
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()

                if eval is None:
                    return None

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = (max_eval, depth)
            return max_eval
        else:
            min_eval = math.inf
            for move in self.order_moves(board):
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()

                if eval is None:
                    return None

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = (min_eval, depth)
            return min_eval

    def order_moves(self, board):
        def move_value(move):
            if board.is_capture(move):
                return self.MOVE_CAPTURE_VALUE
            elif board.gives_check(move):
                return self.MOVE_CHECK_VALUE
            elif move.promotion:
                return self.MOVE_PROMOTION_VALUE
            return 0

        return sorted(board.legal_moves, key=move_value, reverse=True)

    def choose_move(self, board):
        self.start_time = time.time()
        self.nodes_visited = 0
        best_move = None
        best_value = -math.inf

        for depth in range(1, self.depth + 1):
            current_best_move = None
            current_best_value = -math.inf
            alpha = -math.inf
            beta = math.inf

            for move in self.order_moves(board):
                board.push(move)
                value = -self.alpha_beta(board, depth - 1, -beta, -alpha, True)
                board.pop()

                if value is None:
                    print(f"Time limit reached. Stopping at depth {depth-1}")
                    return best_move

                if value > current_best_value:
                    current_best_value = value
                    current_best_move = move

                alpha = max(alpha, current_best_value)

            if current_best_value > best_value:
                best_value = current_best_value
                best_move = current_best_move

            # Print the best move and value after each depth
            print(f"Depth {depth} completed. Best move: {best_move}")

        end_time = time.time()
        print(f"QuiescenceAI recommending move {best_move}")
        print(f"Nodes visited: {self.nodes_visited}")
        print(f"Time taken: {end_time - self.start_time:.2f} seconds")

        return best_move

# board = chess.Board()
# ai = QuiescenceAI(depth=3)

# print("Initial board state:")
# print(board)
# print("\nSearching for best move...")
# move = ai.choose_move(board)
# print(f"\nFinal decision - Best move: {move}")
