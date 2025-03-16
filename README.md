# Chess_TRPO24-1_Chichigin

Базовая часть: Создать объектно-ориентированную реализацию программы для игры в шахматы.

# main.py - файл запуска игры.  
# pieces.py - файл реализации обычных и кастомных шахматных/шашочных фигур и их логики.
# board.py - файл реализации игрового поля, логики игры, функции отката ходов и функции отображения возможных ходов для фигуры.

Дополнительные задания:

1. "Придумать 3 новых вида фигур с оригинальными правилами перемещения и реализовать их классы. Создать модификацию шахмат с новыми фигурами с минимальным вмешательством в существующий код. Сложность 1." Придуманы 3 новые фигуры: "S" - копейщик, "H" - тяжёлая кавалерия, "M" - монарх (замена короля).
2. "На базе игры в шахматы реализовать игру в шашки. Разработать модификацию шахмат с минимальным вмешательством в существующий код. Сложность 2." В самом начале даётся выбор в какую игру играть (/chess или /checkers).
3. "Реализовать возможность «отката» ходов. С помощью специальной команды можно возвращаться на ход (или заданное количество ходов) назад вплоть до начала партии. Информация о ходах в партии должна храниться в объектно-ориентированном виде. Сложность 1." Реализуется вводом /back_step (число ходов) (Например: /backstep 3).
4. "Реализовать функцию подсказки выбора новой позиции фигуры: после выбора фигуры для хода функция визуально на поле показывает поля доступные для хода или фигуры соперника, доступные для взятия, выбранной фигурой. Информация о допустимых ходах должна храниться в объектно-ориентированном виде, алгоритм без модификации должен работать при добавлении новых типов фигур (задание берется совместно с заданием 1). Сложность 1." Возможные ходы для фигуры отображаются знаком "*", так же для отмена выбора какой фигуры для хода предусмотренна команда /cancel.

Итоговая суммарная сложность: 5
