import curses

def main(stdscr):
    # Настройка окна
    curses.curs_set(0) # Скрываем курсор
    stdscr.scrollok(1) # Включаем автопрокрутку

    # Создаем и отображаем поле ввода
    input_win = curses.newwin(1, curses.COLS, curses.LINES-1, 0) # Создаем окно для поля ввода
    input_win.addstr(0, 0, "Введите текст: ") # Отображаем подсказку
    input_win.refresh() # Обновляем окно

    # Обработка ввода текста
    text = ""
    while True:
        c = stdscr.getch() # Получаем символ с клавиатуры
        if c == 10: # Если нажата клавиша "Enter"
            break
        elif c == curses.KEY_BACKSPACE: # Если нажата клавиша "Backspace"
            text = text[:-1] # Удаляем последний символ
        else:
            text += chr(c) # Добавляем символ к тексту
        stdscr.addstr(0, 13, " " * (curses.COLS-13)) # Очищаем старый текст
        stdscr.addstr(0, 13, text) # Выводим новый текст
        stdscr.refresh() # Обновляем окно

if __name__ == "__main__":
    curses.wrapper(main)
