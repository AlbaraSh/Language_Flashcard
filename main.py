from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE = "French"
LANGUAGE_FILE = "data/french_words.csv"

# changing the words on the canvas
try:
    file = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_file = pandas.read_csv(LANGUAGE_FILE)
    word_dict = original_file.to_dict(orient="records")
else:
    word_dict = file.to_dict(orient="records")
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(word_dict)
    canvas.itemconfig(title, text=LANGUAGE, fill="black")
    canvas.itemconfig(word, text=current_card[LANGUAGE], fill="black")
    canvas.itemconfig(front_canvas, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(front_canvas, image=card_back_image)


def is_known():
    word_dict.remove(current_card)
    data = pandas.DataFrame(word_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
window.title("Flashcards")

flip_timer = window.after(2000, func=flip_card)

# card front canvas
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
front_canvas = canvas.create_image(400, 263, image=card_front_image)

# title text
title = canvas.create_text(400, 150, text="Title", font=("ariel", 40, "italic"))

# word label
word = canvas.create_text(400, 263, text="Word", font=("ariel", 60, "bold"))

# correct button
correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=is_known)
correct_button.grid(column=1, row=1)

# incorrect button
incorrect_image = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=incorrect_image, highlightthickness=0, command=next_card)
incorrect_button.grid(column=0, row=1)

next_card()

window.mainloop()
