# ---------------------------- package setup ------------------------------- #
from tkinter import *
from tkinter import messagebox, filedialog
from datetime import datetime
import numpy as np

# ---------------------------- parameter setup ------------------------------- #
CURRENT = datetime.now()
THEME_COLOR = "#375362"
translation = {"a": (0, 2), "b": (0, 3), "c": (0, 4),
               "d": (1, 2), "e": (1, 3), "f": (1, 4),
               "g": (2, 0), "h": (2, 1), "i": (2, 2), "j": (2, 3), "k": (2, 4), "l": (2, 5), "m": (2, 6),
               "n": (3, 0), "o": (3, 1), "p": (3, 2), "x": (3, 3), "P": (3, 4), "O": (3, 5), "N": (3, 6),
               "M": (4, 0), "L": (4, 1), "K": (4, 2), "J": (4, 3), "I": (4, 4), "H": (4, 5), "G": (4, 6),
               "F": (5, 2), "E": (5, 3), "D": (5, 4),
               "C": (6, 2), "B": (6, 3), "A": (6, 4)}
dot_info = np.array([[2, 2, 1, 1, 1, 2, 2],
                     [2, 2, 1, 1, 1, 2, 2],
                     [1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 0, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 1, 1, 1, 2, 2],
                     [2, 2, 1, 1, 1, 2, 2]])

# ---------------------------- UI setup ------------------------------- #
window = Tk()
window.title("Peg Solitaire Game")
window.config(padx=50, pady=50, background=THEME_COLOR)

for key, (x, y) in translation.items():
    globals()[f"dot{x}{y}"] = Button(text=f"🔴{key}", highlightthickness=0)
    globals()[f"dot{x}{y}"].grid(row=x+1, column=y+1)
globals()["dot33"].config(text="⚪x")

user_input = Entry()
user_input.insert(INSERT, "e.g. ex")
user_input.grid(row=1, column=10)

for _ in range(0, 7):
    row_label = Label(text=f"{_}", background=THEME_COLOR, foreground="white")
    row_label.grid(row=0, column=_+1)
    column_label = Label(text=f"{_}", background=THEME_COLOR, foreground="white")
    column_label.grid(row=_+1, column=0)


# ---------------------------- Test for valid input ------------------------------- #
def valid_check():
    """
    Check if user input right from/to dot_info are valid
    """
    global from_dot_first, from_dot_second, middle_dot_first, middle_dot_second, to_dot_first, \
        to_dot_second, middle_dot
    # Get the input value from entry
    try:

        from_dot = translation[user_input.get()[0]]
        from_dot_first = int(from_dot[0])
        from_dot_second = int(from_dot[1])

        to_dot = translation[user_input.get()[1]]
        to_dot_first = int(to_dot[0])
        to_dot_second = int(to_dot[1])

        middle_dot_first = int((from_dot_first + to_dot_first) / 2)
        middle_dot_second = int((from_dot_second + to_dot_second) / 2)
        for k, (a, b) in translation.items():
            if (a, b) == (middle_dot_first, middle_dot_second):
                middle_dot = k

        valid_jump = [(from_dot_first - 2, from_dot_second), (from_dot_first + 2, from_dot_second),
                      (from_dot_first, from_dot_second - 2), (from_dot_first, from_dot_second + 2)]
    # 1. Check if the dot exist
    except (KeyError, IndexError):
        messagebox.showwarning(title="Warning", message="The dot position not exist or not two dots!")

    else:
        # 2. Check if the from_dot is filled and the to_dot is empty:
        if dot_info[from_dot_first, from_dot_second] != 1 or dot_info[to_dot_first, to_dot_second] != 0:
            messagebox.showwarning(title="Warning", message="Please make sure the from dot is filled and the to dot is "
                                                            "empty!")
            is_valid = False

        # 3. Check if it's a diagonal jump
        elif (to_dot_first, to_dot_second) not in valid_jump:
            messagebox.showwarning(title="Warning", message="It's a diagonal jump! Please try again!")
            is_valid = False

        # 4. Check if the middle dot is filled
        elif dot_info[middle_dot_first, middle_dot_second] != 1:
            messagebox.showwarning(title="Warning", message="The dot between these two is empty!")
            is_valid = False

        else:
            is_valid = True

        return is_valid


# ---------------------------- Make dot move ------------------------------- #
def move():
    """
    Make and record dot move if input are valid
    """
    global from_dot_first, from_dot_second, middle_dot_first, middle_dot_second, to_dot_first, \
        to_dot_second, middle_dot
    try:
        is_valid = valid_check()
    except TypeError:
        is_valid = False

    if is_valid:
        # 1. Record the move in log file
        try:
            with open(f"log_{CURRENT}.txt", mode="a") as file:
                file.write(f"{user_input.get()},")
        except FileNotFoundError:
            with open(f"log_{CURRENT}.txt", mode="w") as file:
                file.write(f"{user_input.get()},")

        # 2. Update dot color
        globals()[f"dot{from_dot_first}{from_dot_second}"].config(text=f"⚪{user_input.get()[0]}")
        globals()[f"dot{middle_dot_first}{middle_dot_second}"].config(text=f"⚪{middle_dot}")
        globals()[f"dot{to_dot_first}{to_dot_second}"].config(text=f"🔴{user_input.get()[1]}")

        # 3. Update dot_info array
        dot_info[from_dot_first, from_dot_second] = 0
        dot_info[middle_dot_first, middle_dot_second] = 0
        dot_info[to_dot_first, to_dot_second] = 1

        check_game_over()


move_button = Button(text="Move", command=move)
move_button.grid(row=4, column=10)


# ---------------------Open button to import solution--------------------- #
def openfile():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    # 1. Show the open file dialog
    solution_file = filedialog.askopenfile(filetypes=filetypes)
    # 2. Read the text file and show its content on the Text
    data = solution_file.read().split(",")
    # 3. Loop
    for _ in data:
        user_input.delete(0, END)
        user_input.insert(0, f"{_}")
        move()


open_button = Button(text="Open", command=openfile)
open_button.grid(row=8, column=10)


# ---------------------Open button to import solution--------------------- #
def undo():
    with open(f"log_{CURRENT}.txt", "r") as file:
        lines = file.readlines()
        end = lines[0][-3: -1]
        print(lines)
        print(end)

    undo_from_dot = translation[end[0]]
    undo_from_dot_first = int(undo_from_dot[0])
    undo_from_dot_second = int(undo_from_dot[1])

    undo_to_dot = translation[end[1]]
    undo_to_dot_first = int(undo_to_dot[0])
    undo_to_dot_second = int(undo_to_dot[1])

    undo_middle_dot_first = int((undo_from_dot_first + undo_to_dot_first) / 2)
    undo_middle_dot_second = int((undo_from_dot_second + undo_to_dot_second) / 2)
    for k, (a, b) in translation.items():
        if (a, b) == (undo_middle_dot_first, undo_middle_dot_second):
            undo_middle_dot = k
    # 1. Update dot color
    globals()[f"dot{undo_to_dot_first}{undo_to_dot_second}"].config(text=f"⚪{end[-1]}")
    globals()[f"dot{undo_middle_dot_first}{undo_middle_dot_second}"].config(text=f"🔴{undo_middle_dot}")
    globals()[f"dot{undo_from_dot_first}{undo_from_dot_second}"].config(text=f"🔴{end[0]}")

    # 2. Update dot_info array
    dot_info[undo_from_dot_first, undo_from_dot_second] = 1
    dot_info[undo_middle_dot_first, undo_middle_dot_second] = 1
    dot_info[undo_to_dot_first, undo_to_dot_second] = 0

    # 3. Remove this move from log file
    with open(f"log_{CURRENT}.txt", mode="r") as file:
        line = file.readlines()[0][:-3]

    with open(f"log_{CURRENT}.txt", mode="w") as file:
        file.write(line)


undo_button = Button(text="Undo", command=undo)
undo_button.grid(row=8, column=1)


# ---------------------Check if there is valid left--------------------- #
def check_further_move():
    global tips
    tips = []
    for row in range(5):
        for col in range(5):
            if np.all(dot_info[row:row+3, col] == [0, 1, 1]) or np.all(dot_info[row:row+3, col] == [1, 1, 0]):
                for index, value in translation.items():
                    if value == (row, col):
                        start = index
                    elif value == (row + 2, col):
                        end = index
                pair = start + end
                tips.append(pair)

            if np.all(dot_info[row, col:col+3] == [0, 1, 1]) or np.all(dot_info[row, col:col+3] == [1, 1, 0]):
                for index, value in translation.items():
                    if value == (row, col):
                        start = index
                    elif value == (row, col + 2):
                        end = index
                pair = start + end
                tips.append(pair)
    if len(tips) == 0:
        further_move = False
    else:
        further_move = True

    return further_move


# ---------------------Tip button to show tips for next move--------------------- #
def tip():
    if check_further_move():
        messagebox.showinfo(title="Tips", message=f"Try {tips}")


tip_button = Button(text="Tips", command=tip, borderwidth=0)
tip_button.grid(row=8, column=7)


# -------------------- Check if the game can continue ----------------------- #
def check_game_over():
    if not check_further_move():
        if dot_info.sum() == 33:
            if dot_info[3, 3] == 1:
                messagebox.showinfo(title="", message="Congratulations! You win! :)")
            else:
                messagebox.showinfo(title="", message="Ops, the only peg is not in the middle. :(")
        else:
            messagebox.showinfo(title="", message="No more moves. You lose! :(")


# ---------------------Exit button to terminate the game--------------------- #
exit_button = Button(text="Exit", command=window.destroy)
exit_button.grid(row=8, column=3, columnspan=3)

window.mainloop()
