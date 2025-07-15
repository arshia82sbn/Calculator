import customtkinter as ctk
import datetime
import sqlite3
import os
from PIL import ImageTk, Image

# Initialize main window
root = ctk.CTk()
root.title("Calculator")
root.geometry("360x500")
root.resizable(False, False)
root._set_appearance_mode("dark")

# Set icon
logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
logo_icon = ImageTk.PhotoImage(Image.open(logo_path))
root.iconphoto(False, logo_icon)
root.after(250, lambda: root.iconphoto(False, logo_icon))

# DB setup
database_path = os.path.join(os.path.dirname(__file__), "calculator.db")
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operand1 REAL,
        operation TEXT,
        operand2 REAL,
        result REAL,
        timestamp TEXT
    )
''')
conn.commit()

# Variables
expression = ""
equation = ctk.StringVar()
equation.set("0")

# Functions
def save_history(operand1, operation, operand2, result):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO history (operand1, operation, operand2, result, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (operand1, operation, operand2, result, timestamp))
    conn.commit()

def show(value):
    global expression
    if equation.get() == "0":
        expression = str(value)
    else:
        expression += str(value)
    equation.set(expression)

def clear():
    global expression
    expression = ""
    equation.set("0")

def toggle_sign():
    global expression
    if expression:
        if expression[0] == "-":
            expression = expression[1:]
        else:
            expression = "-" + expression
        equation.set(expression)

def solve():
    global expression
    try:
        expression.replace("X","*")
        for op in ['+', '-','*', '/', '%']:
            if op in expression:
                parts = expression.split(op)
                print(parts)
                operand1 = float(parts[0])
                operand2 = float(parts[1])
                operation = op
                print(op)
                break
        result = eval(expression.replace("X", "*").replace("\u00f7", "/"))
        save_history(operand1, operation, operand2, result)
        equation.set(str(result))
        expression = str(result)
    except:
        equation.set("Error")
        expression = ""

def history_window():
    win = ctk.CTkToplevel(root)
    win.title("History")
    win.geometry("400x500")

    cursor.execute("SELECT operand1, operation, operand2, result, timestamp FROM history ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    for row in rows:
        line = f"[{row[4]}]:{row[0]} {row[1]} {row[2]} = {row[3]}"
        ctk.CTkLabel(
            win,
            text=line,
            fg_color="#214DBC",
            font=('Arial',12),
            anchor='w',
            corner_radius=20
        ).pack(side='top',fill='both',padx=5,pady=1)

# Entry field
entry = ctk.CTkEntry(root, font=("Arial", 30), width=340, height=60,
                     textvariable=equation, justify="right")
entry.place(x=10, y=20)

# History button
ctk.CTkButton(
    root,
    font=('Arial', 30, 'bold'),
    text="History",
    command=history_window,
    width=340,
    fg_color="#214DBC",
    height=55
).place(x=10, y=90)

# Button layout
buttons = [
    ["C", "()", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["+/-", "0", ".", "="]
]

commands = {
    "C": clear,
    "()": lambda: show("("),
    "%": lambda: show("%"),
    "/": lambda: show("/"),
    "7": lambda: show("7"),
    "8": lambda: show("8"),
    "9": lambda: show("9"),
    "*": lambda: show("*"),
    "4": lambda: show("4"),
    "5": lambda: show("5"),
    "6": lambda: show("6"),
    "-": lambda: show("-"),
    "1": lambda: show("1"),
    "2": lambda: show("2"),
    "3": lambda: show("3"),
    "+": lambda: show("+"),
    "+/-": toggle_sign,
    "0": lambda: show("0"),
    ".": lambda: show("."),
    "=": solve
}

# Create buttons
btn_width = 78
btn_height = 60
padding_x = 10
padding_y = 10
start_x = 10
start_y = 155

for i, row in enumerate(buttons):
    for j, btn_text in enumerate(row):
        ctk.CTkButton(
            root,
            text=btn_text,
            width=btn_width,
            height=btn_height,
            corner_radius=20,
            font=("Arial", 25),
            fg_color="#214DBC",
            hover_color="#4B4B4B",
            command=commands[btn_text]
        ).place(x=start_x + j * (btn_width + padding_x), y=start_y + i * (btn_height + padding_y))

# Run the app
root.mainloop()