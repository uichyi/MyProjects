from tkinter import *
from tkinter import messagebox as mb


def valid(row, col, num):
    row = int(row)
    col = int(col)
    for i in range(9):
        # Перекрестная проверка
        if board[i][col] == num or board[row][i] == num:
            return False

        # Проверка, есть ли такое же число в "коробке"
        if board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False

    return True


# Хорошо решается рекурсивным перебором
def solve(row, col):
    # Проверка чтобы указатели не выходили за "рамки" судоку
    if row == 9:
        return True
    if col == 9:
        return solve(row + 1, 0)

    # С числами мы ничего поделать не можем, поэтому триггеримся только на "точки"
    if board[row][col] == ".":
        for i in range(1, 10):
            if valid(row, col, str(i)):
                board[row][col] = str(i)
                if solve(row, col + 1):
                    return True
                else:
                    board[row][col] = "."
        return False
    else:
        return solve(row, col + 1)

"""
board = [
    [".","7",".",".",".",".","5",".","3"],
    ["3",".",".","9","1",".",".",".","."],
    [".",".","1",".",".","8","4",".","."],
    [".",".","6","2","7","3",".",".","."],
    ["8",".",".",".",".","4","2","6","."],
    [".",".",".","6",".",".",".",".","."],
    [".",".","9",".",".","2",".","8","5"],
    [".",".",".","3",".",".",".","2","."],
    ["5",".","2",".",".",".",".",".","."],
]
"""

board = [[]]
def show():
    row = 0
    entry_list = []
    for entr in entries:
        entry_list.append(str(entr.get()))
    for i in entry_list:
        # накинуть проверку как valid
        if i.isdigit() or i == '':
            if i == '':
                i = "."
            board[row].append(i)
            if len(board[row]) == 9 and len(board) < 9:
                row += 1
                board.append([])
        else:
            mb.showerror("Ошибка", "Числа введены неверно")
    solve(0, 0)
    for i in range(9):
        print(board[i])
    board.clear()
    board.append([])


root = Tk()
root.title("Sudoku Solver")
root.geometry("360x500")
entries = []
for j in range(9):
    for i in range(9):
        entry = Entry(width=4)
        entry.grid(row=j, column=i, pady=5, padx=5)
        entries.append(entry)
Button(text="Решить", command=show).grid(row=10, column=4, pady=10)
root.mainloop()

"""
Баги:
1. Если числа не подходят под условия самого судоку, программа вылетает.
2. Проверка ничего не делает, только выводит окошко, но не останавливает процесс.

Добавить:
1. Вывод решения в окошке.
2. Каждой цифре добавить либо различимую палитру так, чтобы глаз смог быстро распознать нахождение всех таких чисел,
либо сделать переключатель, который будет отмечать интересующие числа.
3. Удобно читаемый код.
"""