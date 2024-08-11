from tkinter import *
from tkinter import messagebox
import randomcolor
import gtts
import playsound
import os

# Function to generate random colors and create a gradient
def create_diagonal_gradient(canvas, width, height, color1, color2):
    gradient = PhotoImage(width=width, height=height)
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    
    for i in range(width):
        nr = int(r1 + (r2 - r1) * (i / width))
        ng = int(g1 + (g2 - g1) * (i / width))
        nb = int(b1 + (b2 - b1) * (i / width))
        color = "#%04x%04x%04x" % (nr, ng, nb)
        gradient.put(color, to=(i, 0, i+1, height))
    
    return gradient

# Function to handle button clicks
def on_button_click(button):
    global turn
    if button["text"] == "":
        if turn:
            button["text"] = "X"
            turn = False
        else:
            button["text"] = "O"
            turn = True
        check_for_winner()

# Function to check for the winner
def check_for_winner():
    for combo in win_combinations:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] and buttons[combo[0]]["text"] != "":
            for index in combo:
                buttons[index].config(bg="lightgreen")
            announce_winner(buttons[combo[0]]["text"])
            disable_buttons()
            return
    if all(button["text"] != "" for button in buttons):
        announce_winner("No one")
        disable_buttons()

# Function to announce the winner using gtts
def announce_winner(winner):
    if winner == "No one":
        text = "It's a draw!"
    else:
        text = f"The winner is {winner}!"
    sound = gtts.gTTS(text, lang='en')
    sound.save("winner.mp3")
    playsound.playsound("winner.mp3")
    os.remove("winner.mp3")
    messagebox.showinfo("Tic-Tac-Toe", text)

# Function to disable all buttons
def disable_buttons():
    for button in buttons:
        button.config(state=DISABLED)

# Initialize main window
window = Tk()
window.title("Tic-Tac-Toe with Gradient Background")
window.geometry("400x450")

# Generate random colors for the gradient
rand_color = randomcolor.RandomColor()
color1 = rand_color.generate()[0]
color2 = rand_color.generate()[0]

# Create a canvas for the gradient background
canvas = Canvas(window, width=400, height=450)
canvas.pack(fill="both", expand=True)

# Create and set the diagonal gradient background
gradient = create_diagonal_gradient(canvas, 400, 450, color1, color2)
canvas.create_image(0, 0, anchor=NW, image=gradient)

# Initialize game variables
turn = True  # True for X's turn, False for O's turn
buttons = []
win_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

# Create buttons for Tic-Tac-Toe
for i in range(3):
    for j in range(3):
        button = Button(window, text="", font=("Arial", 20), width=5, height=2)
        button.config(command=lambda b=button: on_button_click(b))
        button.place(x=j*130 + 35, y=i*130 + 35)
        buttons.append(button)

# Start main loop
window.mainloop()
