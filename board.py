from typing import List, Optional, Tuple
from pieces import ChessPiece, CheckersPiece, Pawn, Rook, Knight, Bishop, Queen, Spearman, HeavyCavalry, Monarch

class Board:
    """
    Класс, представляющий игровую доску для шахмат или шашек.
    Отвечает за хранение фигур, их перемещение и отображение доски.
    """
    def __init__(self, game_type: str):
        """
        Инициализация доски.
        Args:
            game_type (str): Тип игры ('chess' или 'checkers').
        """
        self.board: List[List[Optional[ChessPiece | CheckersPiece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.game_type = game_type
        self.setup_board()
        self.move_count = {'белые': 0, 'черные': 0}
        self.move_history: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        self.captured_pieces: List[Optional[ChessPiece | CheckersPiece]] = []

    def setup_board(self):
        """
        Расставляет фигуры на доске в зависимости от типа игры.
        """
        if self.game_type == 'chess':
            for i in range(8):
                if i == 0 or i == 7:
                    self.board[1][i] = Spearman('черные', (1, i))
                    self.board[6][i] = Spearman('белые', (6, i))
                else:
                    self.board[1][i] = Pawn('черные', (1, i))
                    self.board[6][i] = Pawn('белые', (6, i))

            self.board[0][0] = Rook('черные', (0, 0))
            self.board[0][7] = Rook('черные', (0, 7))
            self.board[7][0] = Rook('белые', (7, 0))
            self.board[7][7] = Rook('белые', (7, 7))

            self.board[0][1] = HeavyCavalry('черные', (0, 1))
            self.board[0][6] = Knight('черные', (0, 6))
            self.board[7][1] = HeavyCavalry('белые', (7, 1))
            self.board[7][6] = Knight('белые', (7, 6))

            self.board[0][2] = Bishop('черные', (0, 2))
            self.board[0][5] = Bishop('черные', (0, 5))
            self.board[7][2] = Bishop('белые', (7, 2))
            self.board[7][5] = Bishop('белые', (7, 5))

            self.board[0][3] = Queen('черные', (0, 3))
            self.board[7][3] = Queen('белые', (7, 3))

            self.board[0][4] = Monarch('черные', (0, 4))
            self.board[7][4] = Monarch('белые', (7, 4))
        elif self.game_type == 'checkers':
            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 1:
                        if i < 3:
                            self.board[i][j] = CheckersPiece('черные', (i, j))
                        elif i > 4:
                            self.board[i][j] = CheckersPiece('белые', (i, j))

    def is_empty(self, position: Tuple[int, int]) -> bool:
        """
        Проверяет, пуста ли клетка на доске.
        Args:
            position (Tuple[int, int]): Позиция на доске.
        Returns:
            bool: True, если клетка пуста, иначе False.
        """
        x, y = position
        return self.board[x][y] is None

    def get_piece(self, position: Tuple[int, int]) -> Optional[ChessPiece | CheckersPiece]:
        """
        Возвращает фигуру на указанной позиции.
        Args:
            position (Tuple[int, int]): Позиция на доске.
        Returns:
            Optional[ChessPiece | CheckersPiece]: Фигура или None, если клетка пуста.
        """
        x, y = position
        return self.board[x][y]

    def move_piece(self, start: Tuple[int, int], end: Tuple[int, int], current_turn: str) -> bool:
        """
        Перемещает фигуру с начальной позиции на конечную.
        Args:
            start (Tuple[int, int]): Начальная позиция.
            end (Tuple[int, int]): Конечная позиция.
            current_turn (str): Текущий ход ('белые' или 'черные').
        Returns:
            bool: True, если ход выполнен успешно, иначе False.
        """
        start_x, start_y = start
        end_x, end_y = end
        piece = self.board[start_x][start_y]
        if piece is not None and piece.color == current_turn:
            if end in piece.possible_moves(self):
                captured_piece = None
                if self.game_type == 'checkers' and abs(end_x - start_x) == 2:
                    mid_x, mid_y = (start_x + end_x) // 2, (start_y + end_y) // 2
                    captured_piece = self.board[mid_x][mid_y]
                    self.board[mid_x][mid_y] = None

                self.move_history.append((start, end))
                self.captured_pieces.append(captured_piece)
                self.board[end_x][end_y] = piece
                self.board[start_x][start_y] = None
                piece.position = (end_x, end_y)
                self.move_count[current_turn] += 1
                return True
        return False

    def undo_move(self) -> bool:
        """
        Отменяет последний ход.
        Returns:
            bool: True, если ход отменён успешно, иначе False.
        """
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        start, end = last_move
        captured_piece = self.captured_pieces.pop()

        piece = self.board[end[0]][end[1]]
        self.board[start[0]][start[1]] = piece
        piece.position = start

        self.board[end[0]][end[1]] = None

        if captured_piece is not None:
            if self.game_type == 'checkers':
                mid_x, mid_y = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
                self.board[mid_x][mid_y] = captured_piece
            else:
                self.board[end[0]][end[1]] = captured_piece

        self.move_count[piece.color] -= 1
        return True

    def show_possible_moves(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Возвращает список доступных ходов для фигуры на указанной позиции.
        Args:
            position (Tuple[int, int]): Позиция фигуры.
        Returns:
            List[Tuple[int, int]]: Список доступных ходов.
        """
        piece = self.get_piece(position)
        if piece is not None:
            return piece.possible_moves(self)
        return []

    def display(self, possible_moves: List[Tuple[int, int]] = None):
        """
        Отображает доску, выделяя доступные ходы.
        Args:
            possible_moves (List[Tuple[int, int]]): Список доступных ходов.
        """
        if possible_moves is None:
            possible_moves = []

        print("  a b c d e f g h")
        for i in range(8):
            row = [str(8 - i)]
            for j in range(8):
                piece = self.board[i][j]
                if (i, j) in possible_moves:
                    row.append('*')
                elif piece is not None:
                    if isinstance(piece, Spearman):
                        symbol = 'S'
                    elif isinstance(piece, HeavyCavalry):
                        symbol = 'H'
                    elif isinstance(piece, Monarch):
                        symbol = 'M'
                    else:
                        symbol = piece.__class__.__name__[0]
                    if piece.color == 'черные':
                        symbol = symbol.lower()
                    row.append(symbol)
                else:
                    row.append('.')
            print(' '.join(row))