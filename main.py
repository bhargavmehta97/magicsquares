from tkinter import *
import tkinter.font as fnt
from logic import MagicSquare

root = Tk()
root.title("Play Magic Squares")
root.geometry("760x550+100+100")

# shortening N + E + S + W to just be NESW
NESW = N + E + S + W

# defining time
seconds = 0
minutes = 0
hours = 0

# defining fonts for text usage
font1 = fnt.Font(family='Helvetica', size=12)
font2 = fnt.Font(family='Helvetica', size=14, weight="bold")
font3 = fnt.Font(family='Helvetica', size=16, weight="bold")
font4 = fnt.Font(family='Helvetica', size=18, weight="bold")

# creating a frame for the Buttons
frame_buttons = Frame(root)
# creating a frame to put the colored text with constant and puzzle size inside
frame_colored_text_main = Frame(root)
# creating a frame for the time label to start new timer when creating new puzzles
frame_time_label = Frame(root)
# creating a frame to put the Entry Fields inside
frame_entries = Frame(root)

# defining "entries" as a dictionary so every entry from "entry_fields" can be stored inside
entries = {}


# --------------------------------------------------------------------------
# functions to create buttons, labels, etc

def new_magic_square(square_size):
    global magic, size, constant, size_text, puzzle, solution
    size = square_size
    magic = MagicSquare(size)
    puzzle = magic.puzzle()
    solution = magic.solution()
    constant = magic.magic_constant()
    size_text = str(size) + "x" + str(size)
    if size == 5:
        root.geometry("760x550+100+100")
    elif size == 7:
        root.geometry("760x670+100+100")


# using the MagicSquare function and creating the puzzle list of lists
new_magic_square(5)

# creating a puzzle file and its solution
magic.save("magic_square_file.txt")
saved_solution = magic.solution()


def new_button(button_text, button_frame=frame_buttons, button_row=0, button_column=0, button_sticky=NSEW,
               button_command=None, button_width=18, button_height=3):
    created_button = Button(button_frame, borderwidth="3", text=button_text, command=button_command, font=font1)
    created_button.config(width=button_width, height=button_height)
    created_button.grid(row=button_row, column=button_column, padx=8, pady=10, sticky=button_sticky)


def new_label(label_frame=root, label_font=font2, font_colour="blue", label_padx=10, label_justify=LEFT, label_text="",
              label_expand=True, label_anchor=W):
    created_label = Label(label_frame, font=label_font, fg=font_colour, padx=label_padx, justify=label_justify,
                          text=label_text)
    created_label.pack(expand=label_expand, anchor=label_anchor)


def new_colored_label(label_frame=frame_colored_text_main, label_font=font2, font_colour1="blue", font_colour2="black", font_colour3=None,
                      label_frame_padx=30, label_padx=0, label_text1="", label_text2="", label_text3=None):
    frame_colored_text_sub = Frame(label_frame)
    frame_colored_text_sub.pack(anchor=W, padx=label_frame_padx)
    colored_label1 = Label(frame_colored_text_sub, font=label_font, fg=font_colour1, padx=label_padx,
                           text=label_text1)
    colored_label2 = Label(frame_colored_text_sub, font=label_font, fg=font_colour2, padx=label_padx,
                           text=label_text2)
    colored_label3 = Label(frame_colored_text_sub, font=label_font, fg=font_colour3, padx=label_padx,
                           text=label_text3)
    colored_label1.grid(row=0, column=0)
    colored_label2.grid(row=0, column=1)
    colored_label3.grid(row=0, column=2)


def new_entry(entry_frame=frame_entries, entry_font=font3, font_color="black", entry_bg="white", entry_width=6,
              entry_justify=CENTER, entry_row=0,
              entry_column=0, entry_ipady=10, entry_padx=5, entry_pady=5, insert_bool=False, insert_position=0,
              insert_content=None, disable_state=False, use_callback=False):
    created_entry = Entry(entry_frame, bg=entry_bg, font=entry_font, fg=font_color, justify=entry_justify,
                          relief="solid")
    created_entry.config(width=entry_width)
    created_entry.grid(row=entry_row, column=entry_column, ipady=entry_ipady, padx=entry_padx, pady=entry_pady)

    if insert_bool:
        created_entry.insert(insert_position, insert_content)
    if disable_state:
        created_entry.config(state="disabled")
    if use_callback:
        created_entry.bind("<FocusOut>", lambda e: check_entry(puzzle))

    # adding the entry to a dictionary to access them later
    entries[(entry_row, entry_column)] = created_entry


# --------------------------------------------------------------------------
# functions for the time label and entry fields

def clock(time_reset):
    global seconds, minutes, hours, seconds_str, minutes_str, hours_str
    if time_reset:
        seconds = 0
        minutes = 0
        hours = 0
        time_reset = False
    seconds += 1
    # every 60 seconds, add 1 to minutes, reset seconds to 0; if seconds is only a single digit, add a "0" in front
    if seconds == 60:
        seconds = 0
        minutes += 1
    if seconds < 10:
        seconds_str = "0" + str(seconds)
    elif seconds >= 10:
        seconds_str = str(seconds)
    # every 60 minutes, add 1 to hours, reset seconds to 0; if minutes is only a single digit, add a "0" in front
    if minutes == 60:
        minutes = 0
        hours += 1
    if minutes < 10:
        minutes_str = "0" + str(minutes)
    elif minutes >= 10:
        minutes_str = str(minutes)
    # if hours is only a single digit, add a "0" in front
    if hours < 10:
        hours_str = "0" + str(hours)
    elif hours >= 10:
        hours_str = str(hours)

    created_time_label.config(text=f"Time = {hours_str}:{minutes_str}:{seconds_str}")
    # call clock function after 1000ms or 1s
    created_time_label.after(1000, lambda: clock(time_reset))


def new_time_label(label_frame=frame_time_label, label_font=font4, font_colour="green", label_padx=10, label_justify=RIGHT,
                   label_text="", label_expand=True, label_anchor=E, time_reset=False):
    global created_time_label
    created_time_label = Label(label_frame, font=label_font, fg=font_colour, padx=label_padx, justify=label_justify,
                               text=label_text)
    created_time_label.pack(expand=label_expand, anchor=label_anchor)
    # start clock function after 0 ms
    created_time_label.after(0, lambda: clock(time_reset))


def sum_vert(input_puzzle, index):
    result = 0
    for input_list in input_puzzle:
        result += input_list[index]
    return result


def entry_fields(input_puzzle):
    # placing the frame for the magic square entries
    frame_entries.pack(expand=True, anchor="e", padx="10", pady="10")
    for indexL, List in enumerate(input_puzzle):
        sum_hor = 0
        # creating the white and grey entries and calculating the horizontal sum
        for indexI, item in enumerate(List):
            sum_hor += item
            if item != 0:
                new_entry(entry_bg="grey", entry_row=indexL, entry_column=indexI, insert_bool=True,
                          insert_position=indexI, insert_content=item, disable_state=True)
            elif item == 0:
                new_entry(entry_bg="white", entry_row=indexL, entry_column=indexI, use_callback=True)
        # once List is iterated through, create another yellow entry field in a column to the right
        new_entry(entry_bg="yellow", font_color="red", entry_row=indexL, entry_column=indexI + 1, insert_bool=True,
                  insert_position=indexI + 1, insert_content=sum_hor)

    # once the rows are finished, create another row with yellow entry fields and the SUM label
    for index in range(len(puzzle)):
        vert_result = sum_vert(puzzle, index)
        new_entry(entry_bg="yellow", font_color="red", entry_row=indexL + 1, entry_column=index, insert_bool=True,
                  insert_position=indexI + 1, insert_content=vert_result)
    SUM = Label(frame_entries, text="SUM", font=font2, fg="red", justify=CENTER)
    SUM.grid(row=indexL + 1, column=index + 1, ipady=10)


# --------------------------------------------------------------------------
# generate new puzzles and new windows

def generate_puzzle_window():
    top = Toplevel()
    top.title("Play Magic Squares")
    top_frame = Frame(top)

    new_label(label_frame=top, label_text="Generate a new puzzle", label_justify=CENTER, label_anchor=S)
    top_frame.pack()
    new_button(button_frame=top_frame, button_text="5x5", button_row=0, button_column=0, button_height=2,
               button_command=lambda: on_click(5, create_new_puzzle=True))
    new_button(button_frame=top_frame, button_text="7x7", button_row=0, button_column=1, button_height=2,
               button_command=lambda: on_click(7, create_new_puzzle=True))
    new_label(label_frame=top, label_text="or", label_justify=CENTER, label_anchor=S)
    load_puzzle = Button(top, font=font1, text="load puzzle from a text file", borderwidth=3,
                         command=lambda: puzzle_from_file("magic_square_file.txt"))
    load_puzzle.config(width=30, height=2)
    load_puzzle.pack(pady=10)


def on_click(square_size, create_new_puzzle):
    global constant, size_text
    for widget in frame_colored_text_main.winfo_children():
        widget.destroy()
    for widget in frame_time_label.winfo_children():
        widget.destroy()
    for widget in frame_entries.winfo_children():
        widget.destroy()

    if create_new_puzzle:
        if square_size == 5:
            new_magic_square(5)
        if square_size == 7:
            new_magic_square(7)

    if size == 5:
        root.geometry("760x550+100+100")
    elif size == 7:
        root.geometry("760x670+100+100")

    new_colored_label(label_text1="You are now playing magic square with", label_text2=size_text,
                      label_text3="squares.",
                      font_colour3="blue")
    new_colored_label(label_text1="Magic constant is:", label_text2=constant)
    new_time_label(time_reset=True)
    entry_fields(puzzle)

    check_entry(puzzle)


# split then group file contents, to structure its contents better
def split_group(file_input_str):
    global file_puzzle_size, size
    output_list = []
    input_list = file_input_str.split()
    if len(input_list) / 5 == 5:
        file_puzzle_size = 5
        size = 5
    if len(input_list) / 7 == 7:
        file_puzzle_size = 7
        size = 7
    for i in range(file_puzzle_size):
        List_sub = []
        for l in range(file_puzzle_size):
            item = int(input_list[(l + 1) * (i + 1) - 1])
            List_sub.append(item)
        output_list.append(List_sub)
    return output_list


# get puzzle from saved file
def puzzle_from_file(file_name):
    global puzzle, saved_solution, solution, size, size_text, constant
    with open(file_name) as file:
        reader = file.readlines()
        solution_content = ""
        puzzle_content_temp = ""
        for line in reader:
            # create solution_content; break when puzzle content starts
            for char in line:
                if char.isnumeric() or char == " ":
                    solution_content += char
                if char == "|":
                    break
            # create puzzle_content_temp; include all numbers and whitespaces
            for char in line:
                if char.isnumeric() or char == " ":
                    puzzle_content_temp += char
                if char == "|":
                    puzzle_content_temp += " "
        # remove the solution_content from puzzle_content_temp, so it only includes the puzzle part
        puzzle_content = ""
        for i in range(len(puzzle_content_temp)):
            if i > len(solution_content):
                puzzle_content += puzzle_content_temp[i]
        # format the contents and assign them to solution and puzzle with "split_group" function
        solution = saved_solution
        puzzle = split_group(puzzle_content)
        constant = sum(solution[0])
        size_text = size_text = str(size) + "x" + str(size)
        on_click(file_puzzle_size, create_new_puzzle=False)


# --------------------------------------------------------------------------
# entry field updates, checks, etc

# checks if row and col sum are equal to constant, if true: color the entry green
def check_sum(check_input):
    global constant, user_input, size
    for index_li, li in enumerate(check_input):
        row_sum = sum(li)
        col_sum = 0
        for index_item, item in enumerate(li):
            col_sum += (check_input[index_item][index_li])

        if row_sum == constant:
            entries[index_li, size].delete(0, END)
            entries[index_li, size].insert(0, constant)
            entries[index_li, size].config(bg="green", fg="black")
        elif row_sum != constant:
            entries[index_li, size].delete(0, END)
            entries[index_li, size].insert(0, row_sum)
        if col_sum == constant:
            entries[size, index_li].delete(0, END)
            entries[size, index_li].insert(0, constant)
            entries[size, index_li].config(bg="green", fg="black")
        elif col_sum != constant:
            entries[size, index_li].delete(0, END)
            entries[size, index_li].insert(0, col_sum)


# check if the entries from the user are correct
def check_entry(check_input):
    global user_input, puzzle
    user_input = []
    for index_L, List in enumerate(check_input):
        sub_input = []
        for index_I, item in enumerate(List):
            content = int(item)
            # if the puzzle item is different from the solution item (puzzle item is 0) get the contents of that field
            if solution[index_L][index_I] != check_input[index_L][index_I]:
                entered = entries[index_L, index_I].get()
                # compare as string, since .get() could be empty that cant be converted into an integer
                if entered == str(solution[index_L][index_I]):
                    entries[index_L, index_I].config(bg="grey", fg="black", state="disabled")
                    content = int(entered)
                elif entered != "":
                    content = int(entered)
            sub_input.append(content)
        user_input.append(sub_input)
    check_sum(user_input)

    puzzle = user_input


# --------------------------------------------------------------------------
# Show solution button


# show solution function for solution button
def show_solution():
    for widget in frame_entries.winfo_children():
        widget.destroy()

    entry_fields(solution)

    check_sum(solution)
    pass


# show hint function for hint button
def show_hint():
    check_entry(puzzle)
    global user_input
    gave_hint = False
    new_input = []

    for index_L, List in enumerate(user_input):
        sub_input = []
        for index_I, item in enumerate(List):
            content = int(item)
            sub_input.append(content)
            # if the puzzle item is different from the solution item (puzzle item is 0) get the contents of that field
            if solution[index_L][index_I] != user_input[index_L][index_I]:
                hint = int(solution[index_L][index_I])
                entries[index_L, index_I].delete(0, END)
                entries[index_L, index_I].insert(0, hint)
                gave_hint = True
            if gave_hint:
                break
        new_input.append(sub_input)
        if gave_hint:
            break

    user_input = new_input


# clear input function for clear input button
def clear_input():
    global user_input, solution
    new_input = []
    for index_L, List in enumerate(user_input):
        sub_input = []
        for index_I, item in enumerate(List):
            content = int(item)
            if user_input[index_L][index_I] != solution[index_L][index_I]:
                entries[index_L, index_I].delete(0, END)
                content = 0
            sub_input.append(content)
        new_input.append(sub_input)

    user_input = new_input
    check_sum(user_input)

    for widget in frame_entries.winfo_children():
        widget.destroy()
    entry_fields(user_input)



#######################################################################################################################
# using all functions to create the starting window

# placing frame for buttons
frame_buttons.pack(expand=True, anchor="center")

# using button function to create buttons
new_button(button_text="New Puzzle", button_row=0, button_column=0, button_command=generate_puzzle_window)
new_button(button_text="Get Hint", button_row=0, button_column=1, button_command=show_hint)
new_button(button_text="Show Solution", button_row=0, button_column=2, button_command=show_solution)
new_button(button_text="Clear Input", button_row=0, button_column=3, button_command=clear_input)

frame_colored_text_main.pack(expand=True, anchor=W)

# using new_colored_label and new_label functions to place labels
new_colored_label(label_text1="You are now playing magic square with", label_text2=size_text, label_text3="squares.",
                  font_colour3="blue")
new_colored_label(label_text1="Magic constant is:", label_text2=constant)

frame_time_label.pack(expand=True, anchor=E)
new_time_label()

entry_fields(puzzle)

check_sum(puzzle)

mainloop()
