import chess
import chess.engine
import math
import time
import random

class EnhancedQAI:
    # Piece values
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 99999
    }
    
    # Evaluation constants
    CHECKMATE_SCORE = 10000
    STALEMATE_SCORE = 0
    CENTRAL_PAWN_BONUS = 30
    MOBILITY_MULTIPLIER = 10
    CHECK_PENALTY = 50
    
    # Move ordering constants
    CAPTURE_BONUS = 100
    PROMOTION_BONUS = 90
    CHECK_BONUS = 50
    KILLER_MOVE_BONUS = [80, 70]  # First and second killer move bonuses
    
    # Position tables
    PAWN_POSITION_BONUS = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]
    
    KNIGHT_POSITION_BONUS = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]
    
    BISHOP_POSITION_BONUS = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]
    
    ROOK_POSITION_BONUS = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ]
    
    # Opening book with weighted moves
    OPENING_BOOK = {
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": [
            (chess.Move.from_uci("e2e4"), 40),  # King's Pawn
            (chess.Move.from_uci("d2d4"), 40),  # Queen's Pawn
            (chess.Move.from_uci("c2c4"), 20)   # English Opening
        ],
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": [
            (chess.Move.from_uci("e7e5"), 40),  # Open Game
            (chess.Move.from_uci("c7c5"), 30),  # Sicilian
            (chess.Move.from_uci("e7e6"), 30)   # French
        ]
    }

    def __init__(self, depth=3, time_limit=10):
        self.depth = depth
        self.nodes_visited = 0
        self.time_limit = time_limit
        self.start_time = 0
        self.transposition_table = {}
        self.move_history = {}
        self.killer_moves = [[None] * 100 for _ in range(2)]

    def get_piece_position_bonus(self, piece, square, is_white):
        position_tables = {
            chess.PAWN: self.PAWN_POSITION_BONUS,
            chess.KNIGHT: self.KNIGHT_POSITION_BONUS,
            chess.BISHOP: self.BISHOP_POSITION_BONUS,
            chess.ROOK: self.ROOK_POSITION_BONUS
        }
        
        if piece.piece_type in position_tables:
            bonus = position_tables[piece.piece_type][square if is_white else chess.square_mirror(square)]
            return bonus if is_white else -bonus
        return 0

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
                position_bonus = self.get_piece_position_bonus(piece, square, piece.color == chess.WHITE)
                
                if piece.color == chess.WHITE:
                    score += value + position_bonus
                else:
                    score -= value + position_bonus

        # Mobility evaluation
        mobility = len(list(board.legal_moves))
        score += self.MOBILITY_MULTIPLIER * mobility if board.turn == chess.WHITE else -self.MOBILITY_MULTIPLIER * mobility

        # King safety
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

        for move in self.order_moves(board, depth):
            if board.is_capture(move) or board.gives_check(move) or move.promotion:
                board.push(move)
                score = -self.quiescence_search(board, -beta, -alpha, depth + 1, max_depth)
                board.pop()

                if score >= beta:
                    self.update_killer_moves(move, depth)
                    return beta
                if score > alpha:
                    alpha = score

        return alpha

    def update_killer_moves(self, move, depth):
        if not self.killer_moves[0][depth]:
            self.killer_moves[0][depth] = move
        elif move != self.killer_moves[0][depth]:
            self.killer_moves[1][depth] = self.killer_moves[0][depth]
            self.killer_moves[0][depth] = move

    def order_moves(self, board, depth=0):
        def move_value(move):
            score = 0
            
            # Basic move ordering: captures, promotions, checks
            if board.is_capture(move):
                score += self.CAPTURE_BONUS
            if move.promotion:
                score += self.PROMOTION_BONUS
            if board.gives_check(move):
                score += self.CHECK_BONUS
            
            # Killer move bonus (only if depth is provided)
            if depth > 0:
                if self.killer_moves[0][depth] == move:
                    score += self.KILLER_MOVE_BONUS[0]
                elif self.killer_moves[1][depth] == move:
                    score += self.KILLER_MOVE_BONUS[1]
            
            # History heuristic
            move_str = move.uci()
            if move_str in self.move_history:
                score += self.move_history[move_str] / 100

            return score

        return sorted(board.legal_moves, key=move_value, reverse=True)

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

    def choose_move(self, board):
        # Check opening book first
        if board.fen() in self.OPENING_BOOK:
            moves = self.OPENING_BOOK[board.fen()]
            total_weight = sum(weight for _, weight in moves)
            rand = random.randint(0, total_weight - 1)
            current_weight = 0
            for move, weight in moves:
                current_weight += weight
                if rand < current_weight:
                    return move

        # If not in opening book, proceed with regular search
        self.start_time = time.time()
        self.nodes_visited = 0
        best_move = None
        best_value = -math.inf

        # Iterative deepening
        for depth in range(1, self.depth + 1):
            current_best_move = None
            current_best_value = -math.inf
            alpha = -math.inf
            beta = math.inf

            for move in self.order_moves(board, depth):
                board.push(move)
                value = -self.alpha_beta(board, depth - 1, -beta, -alpha, True)
                board.pop()

                if value is None:
                    print(f"Time limit reached. Stopping at depth {depth-1}")
                    return best_move

                if value > current_best_value:
                    current_best_value = value
                    current_best_move = move
                    self.update_move_history(move, value, depth)

                alpha = max(alpha, current_best_value)

            if current_best_value > best_value:
                best_value = current_best_value
                best_move = current_best_move

            print(f"Depth {depth} completed. Best move: {best_move}")

        end_time = time.time()
        print(f"EnhancedQuiescenceAI recommending move {best_move}")
        print(f"Nodes visited: {self.nodes_visited}")
        print(f"Time taken: {end_time - self.start_time:.2f} seconds")

        return best_move

    def update_move_history(self, move, value, depth):
        move_str = move.uci()
        if move_str not in self.move_history:
            self.move_history[move_str] = 0
        self.move_history[move_str] += 2 ** depth  # Exponential depth bonus