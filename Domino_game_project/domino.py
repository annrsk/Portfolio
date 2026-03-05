import random


class Domino:
    """
    Класс, представляющий одну костяшку домино.
    Каждая костяшка имеет две стороны со значениями от 0 до 6.
    """
    
    def __init__(self, side1, side2):
        """
        Инициализация костяшки домино.
        
        Параметры:
        side1 (int): значение первой стороны (0-6)
        side2 (int): значение второй стороны (0-6)
        """
        self.side1 = side1
        self.side2 = side2
    
    def __str__(self):
        """Строковое представление костяшки в формате [X|Y]."""
        return f"[{self.side1}|{self.side2}]"
    
    def __repr__(self):
        """Представление объекта для отладки."""
        return str(self)
    
    def Is_double(self):
        """
        Проверка, является ли костяшка дублем.
        """
        return self.side1 == self.side2
    
    def Matches(self, value):
        """
        Проверка, совпадает ли одна из сторон с заданным значением.
        """
        return self.side1 == value or self.side2 == value
    
    def Get_other_side(self, value):
        """
        Получение значения противоположной стороны.
        """
        if self.side1 == value:
            return self.side2
        elif self.side2 == value:
            return self.side1
        return None


class DominoGame:
    """
    Основной класс игры в домино.
    Управляет игровым процессом, взаимодействием с игроком и компьютером.
    """
    
    def __init__(self):
        """
        Инициализация новой игры.
        """
        self.Initialize_game()
    
    def Initialize_game(self):
        # Создание полного набора из 28 костяшек
        self.full_set = []
        for i in range(7):
            for j in range(i, 7):
                self.full_set.append(Domino(i, j))
        
        # Перемешивание набора для случайности
        random.shuffle(self.full_set)
        
        # Раздача по 7 костяшек игроку и компьютеру
        self.player_hand = self.full_set[:7]
        self.computer_hand = self.full_set[7:14]
        self.stock = self.full_set[14:]  # Хранилище оставшихся костяшек
        
        # Игровое поле (цепочка костяшек)
        self.board = []
        
        # Определение первого ходящего
        self.current_player = self.Determine_first_player()
        self.game_over = False  # Флаг завершения игры
        self.winner = None      # Победитель игры
        
        print("Игра началась!")
    
    def Determine_first_player(self):
        """
        Определение первого ходящего.
        """
        # Поиск дублей у игрока
        player_doubles = [domino for domino in self.player_hand if domino.Is_double()]
        computer_doubles = [domino for domino in self.computer_hand if domino.Is_double()]
        
        # Поиск максимального дубля
        max_player_double = max(player_doubles, key=lambda d: d.side1) if player_doubles else None
        max_computer_double = max(computer_doubles, key=lambda d: d.side1) if computer_doubles else None
        
        # Определение первого ходящего по правилам домино
        if max_player_double and max_computer_double:
            if max_player_double.side1 > max_computer_double.side1:
                return "player"
            else:
                return "computer"
        elif max_player_double:
            return "player"
        elif max_computer_double:
            return "computer"
        else:
            # Если дублей нет - жребий
            return "player" if random.random() > 0.5 else "computer"
    
    def Display_game_state(self):
        """
        Отображение текущего состояния игры.
        """
        print("\n" + "="*50)
        print(f"Костяшек в хранилище: {len(self.stock)}")
        
        # Отображение игрового поля
        if self.board:
            board_str = " ".join(str(domino) for domino in self.board)
            print(f"Поле: {board_str}")
            print(f"Левый конец: {self.board[0].side1}, Правый конец: {self.board[-1].side2}")
        else:
            print("Поле: пусто")
        
        # Отображение костяшек компьютера (скрыто)
        print(f"Костяшки компьютера: {' '.join('[?]' for _ in self.computer_hand)}")
        
        # Отображение костяшек игрока с нумерацией
        print("Ваши костяшки:")
        for i, domino in enumerate(self.player_hand):
            print(f"{i+1}: {domino}")
        
        # Подсветка доступных ходов
        available_moves = self.Get_available_moves(self.player_hand)
        if available_moves:
            moves_str = [f"{move[0]+1}({'L' if move[1] == 'left' else 'R'})" for move in available_moves]
            print("Доступные ходы:", moves_str)
        else:
            print("Нет доступных ходов")
    
    def Get_available_moves(self, hand):
        """
        Определение допустимых ходов для заданной руки.
        """
        moves = []
        
        # Если поле пустое - можно положить любую костяшку
        if not self.board:
            for i, domino in enumerate(hand):
                moves.append((i, 'left'))  # Сторона не имеет значения
            return moves
        
        # Получаем значения на концах цепочки
        left_value = self.board[0].side1
        right_value = self.board[-1].side2
        
        # Проверяем каждую костяшку на совпадение с концами
        for i, domino in enumerate(hand):
            if domino.Matches(left_value):
                moves.append((i, 'left'))
            if domino.Matches(right_value):
                moves.append((i, 'right'))
        
        return moves
    
    def Make_move(self, hand, move_index, side):
        """
        Выполнение хода (механика хода).
        """
        domino = hand[move_index]
        
        # Первый ход в игре
        if not self.board:
            self.board.append(domino)
            hand.pop(move_index)
            return True
        
        # Ход на левую сторону цепочки
        if side == 'left':
            board_value = self.board[0].side1
            if domino.side2 == board_value:
                # Правильная ориентация
                self.board.insert(0, domino)
                hand.pop(move_index)
                return True
            elif domino.side1 == board_value:
                # Нужно перевернуть костяшку
                self.board.insert(0, Domino(domino.side2, domino.side1))
                hand.pop(move_index)
                return True
        # Ход на правую сторону цепочки
        else:  # side == 'right'
            board_value = self.board[-1].side2
            if domino.side1 == board_value:
                # Правильная ориентация
                self.board.append(domino)
                hand.pop(move_index)
                return True
            elif domino.side2 == board_value:
                # Нужно перевернуть костяшку
                self.board.append(Domino(domino.side2, domino.side1))
                hand.pop(move_index)
                return True
        
        # Ход невозможен
        return False
    
    def Player_turn(self):
        """
        Обработка хода игрока.
        """
        print("\n--- Ваш ход ---")
        
        # Проверка доступных ходов
        available_moves = self.Get_available_moves(self.player_hand)
        
        # Если нет доступных ходов
        if not available_moves:
            if self.stock:
                # Взятие костяшки из хранилища
                new_domino = self.stock.pop()
                self.player_hand.append(new_domino)
                print(f"Вы взяли костяшку из хранилища: {new_domino}")
                return True
            else:
                print("Нет доступных ходов. Ход пропускается.")
                return True
        
        # Цикл ввода и валидации
        while True:
            try:
                # Ввод выбора игрока
                choice = input("Выберите костяшку и сторону (например: '1 L' или '2 R'): ").strip().upper()
                if not choice:
                    print("Неверный ввод. Попробуйте снова.")
                    continue
                
                # Парсинг ввода
                parts = choice.split()
                if len(parts) != 2:
                    print("Введите номер костяшки и сторону (L/R).")
                    continue
                
                domino_index = int(parts[0]) - 1  # Преобразование в 0-based индекс
                side_char = parts[1]
                
                # Валидация индекса
                if domino_index < 0 or domino_index >= len(self.player_hand):
                    print("Неверный номер костяшки.")
                    continue
                
                # Валидация стороны
                if side_char not in ['L', 'R']:
                    print("Сторона должна быть L (слева) или R (справа).")
                    continue
                
                side = 'left' if side_char == 'L' else 'right'
                
                # Проверка допустимости хода
                move_valid = (domino_index, side) in available_moves
                if not move_valid:
                    print("Этот ход невозможен. Выберите другую костяшку или сторону.")
                    continue
                
                # Сохранение костяшки для сообщения
                domino_to_play = self.player_hand[domino_index]
                
                # Выполнение хода
                if self.Make_move(self.player_hand, domino_index, side):
                    print(f"Вы положили костяшку {domino_to_play} на {side} сторону")
                    return True
                else:
                    print("Ошибка при выполнении хода.")
                    return False
                    
            except ValueError:
                print("Неверный формат ввода. Используйте числа для номера костяшки.")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
    
    def Computer_turn(self):
        """
        Обработка хода компьютера.
        """
        print("\n--- Ход компьютера ---")
        
        # Проверка доступных ходов
        available_moves = self.Get_available_moves(self.computer_hand)
        
        # Если нет доступных ходов
        if not available_moves:
            if self.stock:
                # Взятие костяшки из хранилища
                new_domino = self.stock.pop()
                self.computer_hand.append(new_domino)
                print("Компьютер взял костяшку из хранилища")
                return True
            else:
                print("У компьютера нет доступных ходов. Ход пропускается.")
                return True
        
        # Случайный выбор из доступных ходов
        move_index, side = random.choice(available_moves)
        domino = self.computer_hand[move_index]
        
        # Выполнение хода
        if self.Make_move(self.computer_hand, move_index, side):
            print(f"Компьютер положил костяшку на {side} сторону")
            return True
        
        return False
    
    def Check_game_over(self):
        """
        Проверка условий завершения игры.
        """
        # Игрок выложил все костяшки
        if not self.player_hand:
            self.game_over = True
            self.winner = "player"
            return True
        
        # Компьютер выложил все костяшки
        if not self.computer_hand:
            self.game_over = True
            self.winner = "computer"
            return True
        
        # Проверка на "рыбу"
        player_can_move = bool(self.Get_available_moves(self.player_hand)) or self.stock
        computer_can_move = bool(self.Get_available_moves(self.computer_hand)) or self.stock
        
        if not player_can_move and not computer_can_move:
            self.game_over = True
            
            # Подсчет очков для определения победителя
            player_score = sum(d.side1 + d.side2 for d in self.player_hand)
            computer_score = sum(d.side1 + d.side2 for d in self.computer_hand)
            
            if player_score < computer_score:
                self.winner = "player"
            elif computer_score < player_score:
                self.winner = "computer"
            else:
                self.winner = "draw"  # Ничья
            return True
        
        return False
    
    def Play_game(self):
        """
        Основной игровой цикл.
        """
        print(f"Первым ходит: {'Вы' if self.current_player == 'player' else 'Компьютер'}")
        
        # Основной игровой цикл
        while not self.game_over:
            # Отображение текущего состояния
            self.Display_game_state()
            
            # Ход текущего игрока
            if self.current_player == "player":
                if self.Player_turn():
                    self.current_player = "computer"
            else:
                if self.Computer_turn():
                    self.current_player = "player"
            
            # Проверка условий завершения
            if self.Check_game_over():
                break
        
        # Отображение финального результата
        self.Display_final_result()
    
    def Display_final_result(self):
        """
        Отображение результатов завершенной игры.
        """
        print("\n" + "="*50)
        print("ИГРА ОКОНЧЕНА!")
        
        # Определение и вывод победителя
        if self.winner == "player":
            print("ВЫ ВЫИГРАЛИ!")
        elif self.winner == "computer":
            print("Компьютер выиграл. Попробуйте еще раз!")
        else:
            print("Ничья!")
        
        # Подсчет и вывод очков
        player_score = sum(d.side1 + d.side2 for d in self.player_hand)
        computer_score = sum(d.side1 + d.side2 for d in self.computer_hand)
        
        print(f"Ваши оставшиеся очки: {player_score}")
        print(f"Очки компьютера: {computer_score}")


def main():
    """
    Главная функция программы.
    """
    while True:
        # Создание и запуск новой игры
        game = DominoGame()
        game.Play_game()
        
        # Предложение сыграть еще раз
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").strip().lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру!")
            break


if __name__ == "__main__":
    main()