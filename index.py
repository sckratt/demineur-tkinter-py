from random import *
import tkinter as tk
from tkinter import messagebox
from time import sleep

class Window:
    def __init__(self, title) -> None:
        self.root = tk.Tk()
        self.root.title(title)

    def launch(self):
        self.root.mainloop()

    def info(self, title, text):
        messagebox.showinfo(title, text)
    def warning(self, title, text):
        messagebox.showwarning(title, text)
    def error(self, title, text):
        messagebox.showerror(title, text)

class Click:
    def __init__(self) -> None:
        self.type = 0

    def toggle(self, btn):
        self.type = -self.type + 1
        btn.config(text=self.typeString())

    def typeString(self):
        if self.type == 0:
            return "NORMAL",
        elif self.type == 1:
            return "DRAPEAU"

class Timer:
    def __init__(self, window: Window, boardgame) -> None:
        self.window = window
        self.boardgame: BoardGame = boardgame
        self.isDestroyed = False
        self.timestamp = 0
        self.label = self.createLabel()
        
    def createLabel(self):
        label = tk.Label(self.window.root, text=str(self.timestamp))
        label.grid(row=0, column=0, columnspan=self.boardgame.width//4, sticky="nesw")
        return label

    def start(self):
        if self.isDestroyed: return
        self.timestamp += 1
        self.label.config(text=str(self.timestamp))
        self.window.root.after(1000, self.start)

    def destroy(self):
        self.isDestroyed = True

class BoardGame:
    def __init__(self, game, width, height, bombs_count) -> None:
        self.game = game
        self.window = Window("Démineur")
        self.click = Click()
        self.buttons = [[None for i in range(width)] for j in range(height)]
        self.width = width
        self.height = height
        self.bombs_count = bombs_count
        self.T = [[0 for i in range(width)] for j in range(height)]
        self.timer = Timer(self.window, self)
        
        for i in range(self.bombs_count):
            self.createBomb()

    def createBomb(self):
        y, x = randint(0, self.height-1), randint(0, self.width-1)
        if self.T[y][x] == -1:
            return self.createBomb()
        self.T[y][x] = -1
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if i >= 0 and i < len(self.T) and j >= 0 and j < len(self.T[i]) and self.T[i][j] != -1:
                    self.T[i][j] += 1
    def createButtons(self, game):
        destroyButton = tk.Button(self.window.root, text="LEAVE", command=self.destroy)
        destroyButton.grid(row=0, column=self.width//4, columnspan=self.width//4, sticky="nesw")
        restartButton = tk.Button(self.window.root, text="RESTART", command=self.restart)
        restartButton.grid(row=0, column=self.width//4*2, columnspan=self.width//4, sticky="nesw")
        toggleTypeButton = tk.Button(self.window.root, text=self.click.typeString(), command=lambda: self.click.toggle(toggleTypeButton))
        toggleTypeButton.grid(row=0, column=self.width//4*3, columnspan=self.width//4, sticky="nesw")

        for i in range(len(self.T)):
            for j in range(len(self.T[i])):
                self.buttons[i][j] = tk.Button(self.window.root, text="", width=2, height=1, command=lambda x=j, y=i: self.play(x, y))
                self.buttons[i][j].grid(row=i+1, column=j)

    def play(self, x, y):
        if self.click.type == 0:
            if self.buttons[y][x].cget("text") == "❓": return
            if self.T[y][x] == -1:
                for i in range(len(self.T)):
                    for j in range(len(self.T[i])):
                        self.buttons[i][j].config(text="💣" if self.T[i][j] == -1 else str(self.T[i][j]), state="disabled")
                self.timer.destroy()
                self.window.error("You lost", "You clicked on a bomb !")
                self.restart()
                return
            elif self.T[y][x] == 0:
                self.discover(x,y)
            else:
                self.buttons[y][x].config(text="💣" if self.T[y][x] == -1 else str(self.T[y][x]), state="disabled")
        elif self.click.type == 1:
            self.buttons[y][x].config(text="❓" if not(self.buttons[y][x].cget("text")) else "")

        if self.allDiscovered():
            self.timer.destroy()
            self.window.info("You won", "You just won the game !")
            self.restart()
            return
    def restart(self):
        self.window.root.destroy()
        self.__init__(self.game, self.width, self.height, self.bombs_count)
        self.game.start()
    def destroy(self):
        self.window.root.destroy()

    def discover(self, x, y):
        if y >= 0 and x >= 0 and y < len(self.T) and x < len(self.T[y]) and self.buttons[y][x].cget("text") != str(self.T[y][x]):
            self.buttons[y][x].config(text=str(self.T[y][x]), state="disabled")
            if self.T[y][x] == 0:
                for i in range(y-1, y+2):
                    for j in range(x-1, x+2):
                        self.discover(j, i)
    def allDiscovered(self):
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                if self.buttons[i][j]["state"] != "disabled" and self.T[i][j] != -1:
                    return False
        return True  

    def showConsole(self):
        for i in range(len(self.T)):
            for j in range(len(self.T[i])):
                print("{:>2}".format(str(self.T[i][j])), end="")
            print("")

class Game:
    def __init__(self, width, height, bombs_count) -> None:
        self.boardGame = BoardGame(self, width, height, bombs_count)

    def start(self):
        self.boardGame.createButtons(self)
        self.boardGame.timer.start()
        self.boardGame.window.launch()


game = Game(40, 20, 80)
game.start()