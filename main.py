from board import Board

class Game:
    """
    Класс, управляющий игровым процессом.
    Отвечает за взаимодействие с пользователем и управление ходами.
    """
    def __init__(self, game_type: str):
        """
        Инициализация игры.
        Args:
            game_type (str): Тип игры ('chess' или 'checkers').
        """
        self.board = Board(game_type)
        self.current_turn = 'белые'
        self.game_type = game_type
        self.selected_piece = None
        self.possible_moves = []

    def play(self):
        """
        Основной игровой цикл.
        """
        while True:
            self.board.display(self.possible_moves)
            print(f"Ход {self.current_turn}")
            print(f"Ходы белых: {self.board.move_count['белые']}, Ходы черных: {self.board.move_count['черные']}")

            if self.selected_piece is None:
                command = input("Выбери фигуру: ").strip().lower()
                if command.startswith("/back_step"):
                    try:
                        steps = int(command.split()[1]) if len(command.split()) > 1 else 1
                        for _ in range(steps):
                            if not self.board.undo_move():
                                break
                            self.current_turn = 'белые' if self.current_turn == 'черные' else 'черные'
                    except ValueError:
                        pass
                    continue

                try:
                    x, y = 8 - int(command[1]), ord(command[0]) - ord('a')
                    piece = self.board.get_piece((x, y))
                    if piece is not None and piece.color == self.current_turn:
                        self.selected_piece = (x, y)
                        self.possible_moves = self.board.show_possible_moves((x, y))
                    else:
                        continue
                except (ValueError, IndexError):
                    continue
            else:
                command = input("Выбери клетку для хода: ").strip().lower()
                if command.startswith("/back_step"):
                    try:
                        steps = int(command.split()[1]) if len(command.split()) > 1 else 1
                        for _ in range(steps):
                            if not self.board.undo_move():
                                break
                            self.current_turn = 'белые' if self.current_turn == 'черные' else 'черные'
                    except ValueError:
                        pass
                    continue
                elif command.startswith("/cancel"):
                    self.selected_piece = None
                    self.possible_moves = []
                    continue

                try:
                    x, y = 8 - int(command[1]), ord(command[0]) - ord('a')
                    if (x, y) in self.possible_moves:
                        if self.board.move_piece(self.selected_piece, (x, y), self.current_turn):
                            self.current_turn = 'черные' if self.current_turn == 'белые' else 'белые'
                            self.selected_piece = None
                            self.possible_moves = []
                except (ValueError, IndexError):
                    continue

if __name__ == "__main__":
    print("Выберите игру: /chess или /checkers. Команды: /back_step (число) - откат n ходов, /cancel - отмена выбранной фигуры")
    selected_game_type = input("Введите команду: ").strip().lower()
    if selected_game_type == "/chess":
        game = Game('chess')
    elif selected_game_type == "/checkers":
        game = Game('checkers')
    else:
        print("Некорректный выбор игры.")
        exit()

    game.play()