from tkinter import *

from GameGraphic import Graphic
from GameModule import Module
from tools import Owner

class Game:

    def __init__(self, root,color_player1='black',color_player2='white'):
        # self.graphic = Graphic(root)
        self.graphics = Graphic(root,self)
        self.module = Module(self,self.graphics.size)
        self.color_player1 = color_player1
        self.color_player2 = color_player2

    def update_game_size(self,size):
        self.size = size
        # To save the new color if it change from GUI
        self.module = Module(size)


    def update_players_color(self,color1,color2):
        self.color_player1 = color1
        self.color_player2 = color2

    def win_message_to_gui(self,color):

        if color == Owner.OWN_BY_COMP:
            message = "Computer WIN"
        elif color == Owner.OWN_BY_USER:
            message = "USER WIN"
        else:
            message = "TIE"
        self.graphics.update_gui_win_message(message)

    def user_played(self,place,color):
        # print("Inside Game user played", place)
        self.module.update_user_step_in_module(place,color)

    def send_update_to_GUI(self,list_sq, color):
        # print("GAME: color is ",color)
        if color == Owner.OWN_BY_COMP:
            color = self.color_player2
        else:
            color = self.color_player1
        # print("update sq gui",color)
        self.graphics.update_GUI(list_sq,color)



def main():
    root = Tk()
    Game(root)
    root.geometry("{0}x{1}+50+50".format((root.winfo_screenwidth()//10)*9, ((root.winfo_screenheight()//10)*8)))
    root.mainloop()


if __name__ == '__main__':
    main()
