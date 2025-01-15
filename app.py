import os
import subprocess
from tkinter import Tk, Button, Label

def start_bot():
    # Replace 'bot.py' with your bot's main script name
    subprocess.Popen(["python", "main.py"])
    label.config(text="Bot is running!")

app = Tk()
app.title("Telegram Bot Launcher")

label = Label(app, text="Click to start the bot")
label.pack(pady=10)

start_button = Button(app, text="Start Bot", command=start_bot)
start_button.pack(pady=10)

app.mainloop()
