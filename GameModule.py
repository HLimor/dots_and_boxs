from random import randint,choice
from operator import attrgetter
from copy import deepcopy
from itertools import chain
from tools import Owner

class Square:
    def __init__(self,place):
        self.walls = {"E":None,"W":None,"S":None,"N":None}
        self.owned = 0
        self.color = 0
        self.numbers_of_occupied_walls =0
        self.place = place  #(i,j)

    # Occupied and return True if all walls are
    def update_square_state(self,color):
        i = 0
        for x in self.walls.values():
            if x.owned != 0:
                i+=1
        self.numbers_of_occupied_walls =i
        if self.numbers_of_occupied_walls > 4:
            print("Module Error: Can't have more the 4 walls")
            return 0
        if self.numbers_of_occupied_walls == 4:
            self.owned = color
            #give more step
            return 1
        return 0

class Wall:
    def __init__(self,place):
        self.owned=0
        self.square_affected= []
        self.place = place #(i,j)


class Module():

    def __init__(self,size):
        self.size_sq = size
        self.size = self.size*2+1
        self.game_module = [[]]
        self.sq_occupied_by_user = 0
        self.build_game_module()
        self.update_links_game_module()

    # Function build a data struct that similar to the grafic GUI but hold just the data.
    # empty element owned = 0, owner by user = 1 and owner by computer = 2
    def build_game_module(self):
        for i in range(self.size):
            self.game_module.append([])
            for j in range(self.size):
                # line of walls
                if i % 2 == 0:
                    if j % 2 == 0 :
                        # disabled black buttons that only for decoration.
                        self.game_module[i].append([])
                    else:
                        # horizental wall, can be changred by user
                        self.game_module[i].append(Wall((i,j)))
                else:
                    if j % 2 == 0:
                        # vertical wall, can be changed by user.
                        # since height and width are not the same proportion need to multiply with 0.6
                        self.game_module[i].append(Wall((i,j)))
                    else:
                        # Square.
                        self.game_module[i].append(Square((i,j)))
    # Function create the links between walls and squares and vas versa
    def update_links_game_module(self):
        for i in range(self.size):
            for j in range(self.size):
                # line of walls
                if i % 2 == 0:
                    if j % 2 == 0 :
                        pass
                    else:
                        #horizental wall, can be changred by user
                        if i>0 and type(self.game_module[i-1][j]) is Square :
                            self.game_module[i][j].square_affected.append(self.game_module[i-1][j] )
                        if i <self.size-1 and type(self.game_module[i+1][j]) is Square :
                            self.game_module[i][j].square_affected.append(self.game_module[i+1][j] )
                else:
                    if j % 2 == 0:
                        #vertical wall, can be changed by user.
                        if j>0 and type(self.game_module[i][j-1]) is Square :
                            self.game_module[i][j].square_affected.append(self.game_module[i][j-1] )
                        if j < self.size-1 and type(self.game_module[i][j +1]) is Square:
                            self.game_module[i][j].square_affected.append(self.game_module[i][j+1])
                    else:
                        #Square.
                        if i>0 and type(self.game_module[i-1][j]) is Wall :
                            self.game_module[i][j].walls["N"] = self.game_module[i-1][j]
                        if i<self.size and type(self.game_module[i+1][j]) is Wall :
                            self.game_module[i][j].walls["S"] = self.game_module[i+1][j]
                        if j>0 and type(self.game_module[i][j-1]) is Wall :
                            self.game_module[i][j].walls["E"] = self.game_module[i][j-1]
                        if j < self.size and type(self.game_module[i][j+1]) is Wall:
                            self.game_module[i][j].walls["W"] = self.game_module[i][j+1]


    @staticmethod
    def update_square_affected(game_board,place,color):
        list_of_sq_to_colored=[]
        for sq in game_board[place[0]][place[1]].square_affected:
            if (sq.update_square_state(color)):
                list_of_sq_to_colored.append(sq)

        return list_of_sq_to_colored

    # Function get the game board and return lists of squares sorted by the numbers of walls that ocuppied
    # When giving it number between 0 to 4, it return a list of squars that has this number of occupied walls
    def sort_sq(self,game_sq,num='ALL'):
        list_0 = []
        list_1 = []
        list_2 = []
        list_3 =[]

        for i in range(self.size):
            for j in range(self.size):
                if num == 'ALL':
                    if type(game_sq[i][j]) is Square and game_sq[i][j].numbers_of_occupied_walls != 4:
                        eval(f'list_{game_sq[i][j].numbers_of_occupied_walls}').append(game_sq[i][j])
                else:
                    if type(game_sq[i][j]) is Square and game_sq[i][j].numbers_of_occupied_walls == num:
                        eval(f'list_{game_sq[i][j].numbers_of_occupied_walls}').append(game_sq[i][j])

        # By default function create all the lists
        if num == 'ALL':
            return list_0,list_1,list_2,list_3
        else:
            return eval(f'list_{num}')

    '''def choose_square_to_play(self):
        filter_sq_with_0_wall = []
        filter_sq_with_1_wall = []
        filter_sq_with_2_wall = []
        filter_sq_with_3_wall = []
        filter_sq_with_4_wall = []

        def check_numbers_of_walls(square, num):
            if type(square) is Square and square.numbers_of_occupied_walls == num:
                return True
            return False

        for list_sq in self.game_module:
            filter_sq_with_0_wall += list(filter(lambda x: check_numbers_of_walls(x, 0), list_sq))
            filter_sq_with_1_wall += list(filter(lambda x: check_numbers_of_walls(x, 1), list_sq))
            filter_sq_with_2_wall += list(filter(lambda x: check_numbers_of_walls(x, 2), list_sq))
            filter_sq_with_3_wall += list(filter(lambda x: check_numbers_of_walls(x, 3), list_sq))
            filter_sq_with_4_wall += list(filter(lambda x: check_numbers_of_walls(x, 4), list_sq))

        if len(
                filter_sq_with_0_wall + filter_sq_with_1_wall + filter_sq_with_2_wall + filter_sq_with_3_wall) > self.size_sq * self.size_sq:
            print("Uston, we have aproblem")

        i=0
        sq_with_0=[]
        if len(filter_sq_with_0_wall) > 0:
            i = randint(0,len(filter_sq_with_0_wall)-1)
            sq_with_0 = filter_sq_with_0_wall[i]

        print("i=",i, "len",len(filter_sq_with_0_wall))

        return filter_sq_with_3_wall, sq_with_0'''

    # Update and return the number of occupied for a given number
    @staticmethod
    def get_numbers_of_occupied_walls(sq):
        numbers_of_occupied_walls = 0
        for wall in sq.walls.values():
            if wall.owned != 0:
                numbers_of_occupied_walls+=1
        sq.numbers_of_occupied_walls = numbers_of_occupied_walls
        # print("checking",sq.numbers_of_occupied_walls)
        return numbers_of_occupied_walls

    # Fuction check for each sq which is the longest optinal patch for computer turn
    def A_start (self):
        longest_closedset = []
        longest_closedset_wall = []
        all_sq = deepcopy(self.game_module)

        # Function go through all squares that are not occupied and for each one try thr longest steps that it can play.
        # then chose the longest path that was found
        for i in range(len(all_sq)*2-1):
            closedset = []
            closedset_wall = []
            # To avoid changes in the game itself till the best steps will be found
            all_sq = deepcopy(self.game_module)
            # Return list of squares the sroted according to the numbers of occupied walls
            sorted_sq_list = self.sort_sq(all_sq)
            openset_t = list(chain(sorted_sq_list[3],sorted_sq_list[0],sorted_sq_list[1],sorted_sq_list[2]))
            # Since we will remove the current square in the next line.
            # the next square to chack is in the index 0
            current_sq = openset_t[0]
            openset_t.remove(current_sq)

            # Till we found a wall that didn't occupied the square
            while True:
                # Randomly chose a wall
                wall = self.choose_wall(current_sq)
                if not wall:
                    break
                # Update that the wall is now occupied by computer
                wall.owned = Owner.OWN_BY_COMP
                closedset_wall.append(wall)
                # In case the wall didn't seccsed to close a square, computer turn ended
                if self.get_numbers_of_occupied_walls(current_sq) != 4:
                    break
                # Else square was occupied. add it to the path we found and colored the squeare to be owned by computer
                closedset.append(current_sq)
                current_sq.owned = Owner.OWN_BY_COMP
                # Check which squares were affected from this play
                new_sq = wall.square_affected
                # Ignore the square that was allready played
                new_sq.remove(current_sq)
                # print("new_sq",new_sq)
                # Only if the square can be closed in one move
                if new_sq not in [None,[]] and self.get_numbers_of_occupied_walls(new_sq[0])==3:
                    # Since one wall can affected on 2 square only and one was removed, the potentioak square is in index 0
                    current_sq = new_sq[0]
                elif openset_t:
                    # If no close square that can be closed, take the square from the list
                    current_sq = openset_t[0]
                else:
                    # No more square to check
                    break
                # print("The new ", current_sq.place)
                openset_t.remove(current_sq)

            if len(closedset) > len(longest_closedset) or len(closedset_wall) > len(longest_closedset_wall) :
                longest_closedset = closedset
                longest_closedset_wall = closedset_wall

        return longest_closedset+longest_closedset_wall

    # Function get a square and return a wall that is free.
    # It tries to return a wall that the other square that is affected has no 2 wall occupied
    @staticmethod
    def choose_wall(sq):
        empty_walls = []
        for x in sq.walls.values():
            if x.owned == 0:
                empty_walls.append(x)
        if len(list(empty_walls)) == 0:
            print("Module: weird. shouldn't chose this square ", sq.place)
        # every sq will colored one wall only
        elif len(list(empty_walls)) == 1:
            # print("1 sq=",sq.place, "wall",empty_walls[0].place)
            return empty_walls[0]
        else:
            # need to choose a wall that not affect another sq with 2 walls.
            tmp_wall = None
            for i in range(len(empty_walls)):
                found_2_walls_sq = False
                tmp_wall = choice(list(empty_walls))
                for sq in tmp_wall.square_affected:
                    if sq.numbers_of_occupied_walls == 2:
                        found_2_walls_sq = True
                # if no square that allredy have 2 walls ocupied, this wall is good choice
                if not found_2_walls_sq:
                    return tmp_wall
                # remove the sq that has 2 wall that already occupied.
                empty_walls.remove(tmp_wall)
            # print("2 sq=", sq.place, "wall", tmp_wall.place)

            return tmp_wall

    # static function so we can use it also for the AI.
    @staticmethod
    def adding_walls(game_module,sq_list):
        walls=[]
        for sq in sq_list:
            walls.append(Module.choose_wall(sq))
        for wall in walls:
            game_module[wall.place[0]][wall.place[1]].owned = Owner.OWN_BY_COMP
            # self.update_square_affected(wall.place,2)
            # owned 2 is for the computer
            # print("wall ", wall.place)
        return walls

    # Function get list of squares and return list of walls and squares that can be
    def select_wall_and_all_squares_affected(self,sq,adding_sq=1):

        walls_sq_to_play = []
        new_sq_wall = self.adding_walls(self.game_module, sq)
        if adding_sq :
            walls_sq_to_play = sq
        walls_sq_to_play += new_sq_wall
        for wali in new_sq_wall:
            wali.owned = Owner.OWN_BY_COMP
            self.update_square_affected(self.game_module, wali.place, Owner.OWN_BY_COMP)


        return walls_sq_to_play

    # Function get sorted lists of squars and return a list with squares and walls.
    # look for all squares with 3 walls to mark them all.
    # after if will for additional wall in sq with 0, 1 or 2 respectively.
    def computer_next_step_alg(self, sq_list):
        # first will choose all the squares with 3 walls that can be close by now
        # update th change that made and it affected on the other square.
        # walls_sq_to_play holding all squares that now owned by the computer and the walls that changed
        walls_sq_to_play = self.select_wall_and_all_squares_affected(sq_list[3])

        # check if after the steps that done, more sq are now with 3 walls
        while True:
            new_sq = None
            # check if new, after the step we did before, sq is with 3 walls
            new_sq = self.sort_sq(self.game_module, 3)
            if not new_sq:
                # The step we did didn't move any new squar to be with 3 occupied walls
                break
            # add square that also can be owned by computer and the wall.
            walls_sq_to_play += self.select_wall_and_all_squares_affected(new_sq)

        if len(sq_list[0]) > 0:
            list_to_choose_sq = sq_list[0]
        elif len(sq_list[1]) > 0:
            list_to_choose_sq = sq_list[1]
        else:
            list_to_choose_sq = sq_list[2]

        i = randint(0, len(list_to_choose_sq) - 1)
        tmp = [list_to_choose_sq[i]]
        # adding only the wall since the square is not fully colored.
        wall_to_play = self.select_wall_and_all_squares_affected(tmp,0)

        sq_walls_to_play = walls_sq_to_play + wall_to_play

        return sq_walls_to_play

    # Function update the not grafic part of the model with all the sq and walls that was occupied by computer
    def update_computer_steps_in_model(self, sq_wall_list):

        # update the game model with step that was computed with AI
        for item in sq_wall_list:
            if type(item) is Wall:
                place = item.place
                self.game_module[place[0]][place[1]].owned = Owner.OWN_BY_COMP
                self.update_square_affected(self.game_module,place,Owner.OWN_BY_COMP)


    # Function calcs the next step that will be taken by the computer.
    # first it check if there are obvious steps to do, else it use A star function.
    def computer_turn(self):

        sq_to_play0,sq_to_play1,sq_to_play2,sq_to_play3 = self.sort_sq(self.game_module)
        if len(sq_to_play0) == 0:
            # if no squares with 0 wall, need to use AI in aim to choose the next stage
            sq_walls_to_play = self.A_start()
            self.update_computer_steps_in_model(sq_walls_to_play)
        else:
            sq_walls_to_play = self.computer_next_step_alg([sq_to_play0,sq_to_play1,sq_to_play2,sq_to_play3])

        # sq_walls_to_play_places = (x.place for x in sq_walls_to_play if type(x) in [Wall,Square])
        # print("befor",sq_walls_to_play)
        sq_walls_to_play_places = list(map(attrgetter('place'), sq_walls_to_play))
        # print("sq",sq_walls_to_play_places)
        self.__class__.mro()[0].send_update_to_GUI(self, sq_walls_to_play_places,Owner.OWN_BY_COMP)

    def check_if_someone_win(self):
        sq_occupied_by_computer = 0
        sq_occupied_by_user = 0
        for i in range(self.size_sq):
            for j in range(self.size_sq):
                if self.game_module[i*2+1][j*2+1].owned == Owner.OWN_BY_COMP:
                    sq_occupied_by_computer+=1
                elif self.game_module[i*2+1][j*2+1].owned == Owner.OWN_BY_USER:
                    sq_occupied_by_user+=1
        # print("MODEL: ",sq_occupied_by_computer,sq_occupied_by_user)
        if sq_occupied_by_computer + sq_occupied_by_user == self.size_sq**2:
            if sq_occupied_by_computer > sq_occupied_by_user:
                self.__class__.mro()[0].win_message_to_gui(self,Owner.OWN_BY_COMP)
            elif sq_occupied_by_computer < sq_occupied_by_user:
                self.__class__.mro()[0].win_message_to_gui(self,Owner.OWN_BY_USER)
            else:
                self.__class__.mro()[0].win_message_to_gui(self,Owner.EMPTY)

    def update_user_step_in_module(self,place,color):
        if self.game_module[place[0]][place[1]].owned != 0:
            print("Module Error: trying to update occupied place ", place,self.game_module[place[0]][place[1]].owned)
            return
        if type(self.game_module[place[0]][place[1]]) != Wall:
            print("Module Error: trying to update Not a Wall", place)
            return

        # update wall owner with the right color
        self.game_module[place[0]][place[1]].owned = Owner.OWN_BY_USER
        # update Squre return True if user close new sq
        sq_to_closed_on_gui = self.update_square_affected(self.game_module, place,Owner.OWN_BY_USER)
        sq_to_closed_on_gui_places = list(map(attrgetter('place'), sq_to_closed_on_gui))
        if len(sq_to_closed_on_gui) > 0:
            # update the module part
            for place in sq_to_closed_on_gui_places:
                self.game_module[place[0]][place[1]].owner = Owner.OWN_BY_USER
                self.sq_occupied_by_user += 1
            # update the Graphic part
            self.__class__.mro()[0].send_update_to_GUI(self,sq_to_closed_on_gui_places,Owner.OWN_BY_USER)
            self.check_if_someone_win()
            # Gives the user another turn since he succeed to close a sq
            return

        self.check_if_someone_win()
        self.computer_turn()
        self.check_if_someone_win()


    def printme(self):
        for i in self.game_module:
            for j in i:
                if not j:
                    print(j.place)


def main():
    a = Module(3)
    a.printme()


if __name__ == "__main__":
    main()