from typing import List, Tuple

class ChessPiece:
    """
    Базовый класс для шахматных фигур.
    Отвечает за хранение цвета и позиции фигуры, а также за возможные ходы.
    """
    def __init__(self, color: str, position: Tuple[int, int]):
        """
        Инициализация фигуры.
        Args:
            color (str): Цвет фигуры ('белые' или 'черные').
            position (Tuple[int, int]): Позиция фигуры на доске.
        """
        self.color = color
        self.position = position

    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        """
        Возвращает список возможных ходов для фигуры.
        Args:
            board (Board): Игровая доска.
        Returns:
            List[Tuple[int, int]]: Список возможных ходов.
        """
        raise NotImplementedError

class Pawn(ChessPiece):
    """
    Класс, представляющий пешку.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position
        direction = -1 if self.color == 'белые' else 1

        if board.is_empty((x + direction, y)):
            moves.append((x + direction, y))
            if (self.color == 'белые' and x == 6) or (self.color == 'черные' and x == 1):
                if board.is_empty((x + 2 * direction, y)):
                    moves.append((x + 2 * direction, y))

        for dy in [-1, 1]:
            if 0 <= y + dy < 8:
                target = (x + direction, y + dy)
                if not board.is_empty(target) and board.get_piece(target).color != self.color:
                    moves.append(target)

        return moves

class Rook(ChessPiece):
    """
    Класс, представляющий ладью.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board.is_empty((nx, ny)):
                    moves.append((nx, ny))
                else:
                    if board.get_piece((nx, ny)).color != self.color:
                        moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return moves

class Knight(ChessPiece):
    """
    Класс, представляющий коня.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                        (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in knight_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board.is_empty((nx, ny)) or board.get_piece((nx, ny)).color != self.color:
                    moves.append((nx, ny))
        return moves

class Bishop(ChessPiece):
    """
    Класс, представляющий слона.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board.is_empty((nx, ny)):
                    moves.append((nx, ny))
                else:
                    if board.get_piece((nx, ny)).color != self.color:
                        moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return moves

class Queen(ChessPiece):
    """
    Класс, представляющий ферзя.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board.is_empty((nx, ny)):
                    moves.append((nx, ny))
                else:
                    if board.get_piece((nx, ny)).color != self.color:
                        moves.append((nx, ny))
                    break
                nx += dx
                ny += dy
        return moves

class King(ChessPiece):
    """
    Класс, представляющий короля.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position
        king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in king_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board.is_empty((nx, ny)) or board.get_piece((nx, ny)).color != self.color:
                    moves.append((nx, ny))
        return moves

class CheckersPiece:
    """
    Класс, представляющий шашку.
    """
    def __init__(self, color: str, position: Tuple[int, int]):
        self.color = color
        self.position = position
        self.is_king = False

    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position
        direction = -1 if self.color == 'белые' else 1

        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board.is_empty((nx, ny)):
                    moves.append((nx, ny))

        for dy in [-2, 2]:
            nx, ny = x + 2 * direction, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                mid_x, mid_y = x + direction, y + dy // 2
                if not board.is_empty((mid_x, mid_y)) and board.get_piece((mid_x, mid_y)).color != self.color:
                    moves.append((nx, ny))

        if self.is_king:
            for dy in [-1, 1]:
                nx, ny = x - direction, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if board.is_empty((nx, ny)):
                        moves.append((nx, ny))

        return moves

class Spearman(ChessPiece):
    """
    Класс, представляющий копейщика.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position
        direction = -1 if self.color == 'белые' else 1

        if board.is_empty((x + direction, y)):
            moves.append((x + direction, y))

        for dy in [-1, 1]:
            if 0 <= y + dy < 8:
                target = (x + direction, y + dy)
                if board.is_empty(target) or board.get_piece(target).color != self.color:
                    moves.append(target)

        return moves

class HeavyCavalry(ChessPiece):
    """
    Класс, представляющий тяжёлую кавалерию.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position

        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board.is_empty((nx, ny)) or board.get_piece((nx, ny)).color != self.color:
                    moves.append((nx, ny))

        return moves

class Monarch(ChessPiece):
    """
    Класс, представляющий монарха.
    """
    def possible_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        x, y = self.position

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board.is_empty((nx, ny)) or board.get_piece((nx, ny)).color != self.color:
                    moves.append((nx, ny))

        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                mid_x, mid_y = x + dx // 2, y + dy // 2
                if board.is_empty((mid_x, mid_y)):
                    if board.is_empty((nx, ny)) or board.get_piece((nx, ny)).color != self.color:
                        moves.append((nx, ny))

        return moves