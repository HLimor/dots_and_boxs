from tkinter import *
from tkinter import font
from tkinter import colorchooser as colorchooser
import time
from copy import deepcopy


class Graphic:
    def __init__(self,root,parent):
        self.root = root
        self.parent = parent
        self.size = 0
        # human player color, can be changed from GUI
        self.color_player1 = "black"
        # Computer color , can be changed from GUI
        self.color_player2 = "white"
        #
        Label(self.root,text="Dotes & Boxes", font=("Arial", 25)).pack(side=TOP)
        # the size of the square. defualt value set, change according to the size of the game board
        self.span_size=8
        #Frame that contain the options that can be configured by user
        self.frame_user_options = None
        #Frame that contain the grafics widght game board
        self.frame_board=None
        #Frame that contain the frame_board and the scrollbar in aim to enable to connect between those two.
        self.canvas_frame = None
        self.scroll_bar = None
        #matrixs that contain the grafix widget so it can be changed by the computer side
        self.button_gui_matrix = [[]]
        #build and show the option frame
        self.build_frame_user_options()
        #build and show the game frame
        self.build_frame_board()

    # building all the boxes and the walls of the game for the init time and when resizing the game
    def build_frame_board(self):
        # first running need to create the Canvas and Frame
        if not self.canvas_frame :
            self.canvas_frame = Canvas(self.root,bg="pink")
            self.frame_board = Frame(self.canvas_frame)
            self.canvas_frame.pack(side=LEFT,fill="both", expand=True)
            self.frame_board.pack(pady=10,padx=10,side=TOP)
        self.build_game_board()

    # Function create the right side of the frame
    def build_frame_user_options(self):
        # Frame
        self.frame_user_options = Frame()
        self.frame_user_options.pack(side=RIGHT)
        # Create the buttons & the options
        self.build_option_board()

    # Building the button that gives user option to change the size of the game.
    def build_size_option(self):
        # Option to change the game size. defaults is 4
        size_list = list(range(4, 30))
        self.size_options = StringVar()
        self.size_options.set(size_list[0])  # default value
        self.size = size_list[0]
        self.size_options.trace("w", self.update_board_size)
        OptionMenu(self.frame_user_options, self.size_options, *size_list).pack()

    # Binding function that set the self attribute that saves the colors
    def choose_wall_color(self,player):
        if player == 1:
            self.color_player1 = colorchooser.askcolor(title="Choose color")[1]
        else:
            self.color_player2 = colorchooser.askcolor(title="Choose color")[1]
        self.parent.update_players_color(self.color_player1,self.color_player2)

    # Building the option to choose the colors for user & computer
    def build_color_option(self):
        Label(self.frame_user_options,text="Player 1:").pack()
        Button(self.frame_user_options, text="Select color",
               command=lambda :self.choose_wall_color(1)).pack()
        Label(self.frame_user_options,text="Player 2").pack()
        Button(self.frame_user_options, text="Select color",
               command=lambda :self.choose_wall_color(2)).pack()

    # Function create all the options that are giving to users
    def build_option_board(self):
        self.win_label = Label(self.frame_user_options,text="")
        self.win_label.pack(side=TOP)
        Label(self.frame_user_options,font=("Comic Sans MS", 30, "bold"),text="               ").pack()

        # adding option to change the size of the board game.
        self.build_size_option()
        self.build_color_option()
        self.frame_user_options.pack_propagate(1)

    # Function print win message on the graphic interface.
    # sleep enable it to show as animation
    def update_gui_win_message(self,message):
        for i in range(2):
            self.win_label.config(text=message,font=("Comic Sans MS", 20, "bold"), fg="pale green")
            self.win_label.update()
            time.sleep(1)
            self.win_label.config(text=message,font=("Comic Sans MS", 25, "bold"), fg="blue violet")
            self.win_label.update()
            time.sleep(1)

    # Function after changing the size of the game , it recreate the board
    # Destroy part of the things and rebuild it
    def update_board_size(self,*args):
        self.size = int(self.size_options.get())
        self.span_size = min(8, self.root.winfo_screenheight()//(10*self.size))
        if self.frame_user_options:
            self.win_label.config(text="")
        if self.frame_board:
            for widget in self.frame_board.winfo_children():
                widget.destroy()
        self.build_frame_board()
        if self.span_size*self.size*13 > self.root.winfo_screenheight():
            if not self.scroll_bar:
                self.scroll_bar = Scrollbar(self.root,orient=VERTICAL)
            self.scroll_bar.pack(side=LEFT ,fill=Y)
            self.scroll_bar.config(command=self.canvas_frame.yview)
            self.canvas_frame.config(yscrollcommand = self.scroll_bar.set)
            self.canvas_frame.create_window((100, 100), window=self.frame_board,anchor=CENTER)
            self.canvas_frame.bind("<Configure>", self.update_scrollregion)

        elif self.scroll_bar:
            self.scroll_bar.pack_forget()

        self.parent.update_game_size(self.size)

    def update_scrollregion(self, event):
        self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all"))
        #Move the bar to be up
        self.canvas_frame.update_idletasks()
        # This put the bar sign up.
        self.canvas_frame.yview_moveto(0)

    # Binding to button click
    def change_wall_color(self,event):
        # If this wall already been colored
        if event.widget['bg'] == self.color_player1 or event.widget['bg'] == self.color_player2:
            return
        event.widget.config(bg=self.color_player1, state=DISABLED)
        place = (event.widget.grid_info()['row'],event.widget.grid_info()['column'])
        self.parent.user_played(place, self.color_player1)

    # Function update graphic part after the computer calculate his steps
    def update_GUI(self,list_sq,color):
        copy_of_sq_list = deepcopy(list(list_sq))
        # This code colored the changes first to yellow to enable user to see the steps
        for place in copy_of_sq_list:
            self.button_gui_matrix[place[0]][place[1]].configure(bg="yellow",state=DISABLED)
        self.button_gui_matrix[0][0].update()
        time.sleep(1)
        for place in copy_of_sq_list:
            self.button_gui_matrix[place[0]][place[1]]["bg"]=color
        self.frame_board.update()

    # Function build the grid of the wall/squares game board
    def build_game_board(self):
        # just to make buttons more slim
        small_font = font.Font(family="Helvetica", size=4)

        # clean old data if exists.
        del self.button_gui_matrix
        # define it again as a Matrix
        self.button_gui_matrix =[[]]
        # size is the number of the squars.since squars sharing walls we need to add 1 wall to each square and add one that close the board.
        # doing that in 2 direction , this is why i & j are multiplay with 2 and adding 1
        for i in range(self.size*2+1):
            self.button_gui_matrix.append([])
            for j in range(self.size*2+1):
                #line of walls
                if i % 2 == 0:
                    if j % 2 == 0:
                        # disabled black buttons that only for decoration.
                        self.button_gui_matrix[i].append(Button(master=self.frame_board,bg="black",font=small_font,width=1,height=1,state=DISABLED))
                    else:
                        # horizental wall, can be changed by user
                        self.button_gui_matrix[i].append(Button(master=self.frame_board,bg="lightgreen", font=small_font,width=self.span_size*2))
                        self.button_gui_matrix[i][-1].bind('<Button>',self.change_wall_color)
                else:
                    if j % 2 == 0:
                        # vertical wall, can be changed by user.
                        # since height and width are not the same proportion need to multiply with 0.6
                        self.button_gui_matrix[i].append(Button(master=self.frame_board,bg="lightgreen",font=small_font, width=1,height=int(0.6*self.span_size)*2))
                        self.button_gui_matrix[i][-1].bind('<Button>',self.change_wall_color)
                    else:
                        # Square.
                        self.button_gui_matrix[i].append(Button(master=self.frame_board,width=self.span_size,height=int(0.6*self.span_size),state=DISABLED))
                #show the widget that was add before
                self.button_gui_matrix[i][-1].grid(row=i,column=j)

def main():
    root = Tk()
    Graphic(root)
    root.geometry("{0}x{1}+50+50".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.mainloop()

if __name__ == "__main__":
    main()