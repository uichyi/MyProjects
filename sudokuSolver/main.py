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
solve(0, 0)
for i in range(9):
    print(board[i])
print()
"""


def show():
    board.clear()
    board.append([])
    row = 0
    for entr in entries:
        i = str(entr.get())
        # накинуть проверку как valid
        if i == '' or (i.isdigit() and 1 <= int(i) <= 9):
            if i == '':
                i = "."
            board[row].append(i)
            if len(board[row]) == 9 and len(board) < 9:
                row += 1
                board.append([])
        else:
            board.clear()
            board.append([])
            return mb.showerror("Ошибка", "Числа введены неверно")
    solve(0, 0)
    for i in range(9):
        for j in range(9):
            lab = Label(root, text=board[i][j])
            lab.grid(row=i+11, column=j, pady=5, padx=5)
    for k in range(1, 10):
        Button(text=k, command=lambda n = k: highlight(n)).grid(row=22, column=k-1, pady=10)
    """
    for i in range(9):
        print(board[i])
    print()
    """


def highlight(num):
    for i in range(9):
        for j in range(9):
            if board[i][j] == str(num):
                lab = Label(root, text=board[i][j], background='red')
            else:
                lab = Label(root, text=board[i][j])
            lab.grid(row=i + 11, column=j, pady=5, padx=5)


root = Tk()
root.title("Sudoku Solver")
root.geometry("360x630")
entries = []
board = [[]]
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

Добавить:
1. Возможность нажимать на кнопки прказа отдельных цифр с клавиатуры
2. Удобно читаемый код.
"""