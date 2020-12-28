#!/usr/bin/env python
# coding: utf-8

from a2_support import *

import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog

import PIL
from PIL import ImageTk, Image
import time


class GameLogic:
    """
    GameLogic contains all the game information and how the game should play out. By default,
    GameLogic should be constructed with ​GameLogic(dungeon_name=”game1.txt”)​.
    """

    def __init__(self, dungeon_name="game1.txt"):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level.
        """

        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)

        # you need to implement the Player class first.
        self._player = Player(GAME_LEVELS[dungeon_name])

        # you need to implement the init_game_information() method for this.
        self._game_information = self.init_game_information()

        self._win = False

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.
        """

        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def get_dungeon_size(self) -> int:
        '''
        Returns:
            int: Return the width of the dungeon as an integer.
        '''
        return self._dungeon_size

    def init_game_information(self) -> dict:
        """
        This method should return a dictionary containing the position and the corresponding Entity as the
        keys and values respectively. This method also sets the Player’s position. At the start of the
        game this method should be called to find the position of all entities within the current dungeon.

        Returns:
            d(dict<tuple<int, int>): Return a dictionary containing the position and the corresponding Entity.
        """
        d = {}
        wall = Wall()
        door = Door()
        move_increase = MoveIncrease()
        key = Key()

        list_player = self.get_positions(PLAYER)
        self._player.set_position(list_player[0])

        list_key = self.get_positions(KEY)
        if list_key:
            d[list_key[0]] = key

        list_door = self.get_positions(DOOR)
        d[list_door[0]] = door

        list_wall = self.get_positions(WALL)
        for i in list_wall:
            d[i] = wall

        list_move_increase = self.get_positions(MOVE_INCREASE)
        for i in list_move_increase:
            d[i] = move_increase

        return d

    def get_game_information(self) -> dict:
        """
        Returns a dictionary containing the position and the corresponding Entity, as the keys and values, for the
        current dungeon.

        Returns:
            d(dict<tuple<int, int>): Return a dictionary containing the position and the corresponding Entity.
        """
        d = {}
        wall = Wall()
        door = Door()
        move_increase = MoveIncrease()
        key = Key()

        list_key = self.get_positions(KEY)
        if list_key:
            d[list_key[0]] = key

        list_door = self.get_positions(DOOR)
        d[list_door[0]] = door

        list_wall = self.get_positions(WALL)
        for i in list_wall:
            d[i] = wall

        list_move_increase = self.get_positions(MOVE_INCREASE)
        for i in list_move_increase:
            d[i] = move_increase

        return d

    def get_player(self):
        """
        This method returns the Player object within the game.

        Returns:
            Player: Return Player object within the game.
        """
        return self._player

    def get_entity(self, position):
        """
        Returns an Entity at a given position in the dungeon. Entity in the given direction or if the position is off
        map then this function should return None

        Parameters:
            position(tuple<int,int>): Position of the Entity to be returned.

        Returns:
            Entity or None: Return the Entity in the given direction.

        """
        d = self.get_game_information()
        if position in d:
            return d[position]
        else:
            return None

    def get_entity_in_direction(self, direction):
        """
        Returns an Entity in the given direction of the Player’s position. If there is no Entity in the given direction
        or if the direction is off map then this function should return None.

        Parameters:
            direction(str): Direction of the Player’s position.

        Returns:
            Entity: Return the Entity at the given direction.

        """
        new_position = self.new_position(direction)
        return self.get_entity(new_position)

    def collision_check(self, direction) -> bool:
        """
        Returns ​False​ if a player can travel in the given direction, they won’t collide. ​True, they will collide,
        otherwise

        Parameters:
            direction(str):The given direction of the player to travel.

        Returns:
            bool: Return ​False​ if a player can travel in the given direction. ​True, they will collide.
        """
        entity = self.get_entity_in_direction(direction)
        if entity:
            return not entity.can_collide()
        else:
            return False

    def new_position(self, direction) -> tuple:
        """
        Returns a tuple of integers that represents the new position given the direction.

        Parameters:
            direction(str):Given the direction to be updated.

        Returns:
            new_position(tuple<int,int>): Return the new position given the direction.
        """
        dx, dy = DIRECTIONS[direction]
        x, y = self._player.get_position()
        new_position = (x + dx, y + dy)
        return new_position

    def move_player(self, direction) -> None:
        """
        Update the Player’s position to place them one position in the given direction.

        Parameters:
            direction(str): New position of the player.
        """
        new_position = self.new_position(direction)
        self._player.set_position(new_position)

    def check_game_over(self) -> bool:
        """
        Return True if the game has been ​lost and False otherwise.

        Returns:
            bool: Return True if the game has been ​lost and False otherwise.
        """
        if self._player.moves_remaining() == 0:
            return True
        else:
            return False

    def set_win(self, win) -> None:
        """
        Set the game’s win state to be True or False.

        Parameters:
            win(bool): The game’s win state to be True or False.
        """
        self._win = win

    def won(self) -> bool:
        """
        Return game’s win state.

        Returns:
            bool:Return game’s win state.
        """
        return self._win


class Entity:
    """
    Each Entity has an id, and can either be collided with (two entities can be in the same position)
    or not (two entities cannot be in the same position.) The collidable attribute should be set to
    True for an Entity upon creation. Entity should be constructed with Entity().
    """

    def __init__(self):
        """
        Constructor of the Entity class.
        """
        self.id = 'Entity'
        self.collidable = True

    def get_id(self) -> str:
        """
        Returns a string that represents the Entity’s ID.

        Returns:
            self.id(str): Returns a string that represents the Entity’s ID.
        """
        return self.id

    def set_collide(self, collidable: bool):
        """
        Set the collision state for the Entity to be True

        Parameters:
            collidable(bool): The collision state for the Entity.
        """
        self.collidable = collidable

    def can_collide(self) -> bool:
        """
        Returns True if the Entity can be collided with (another Entity can share the position that this one is in)
        and False otherwise.

        Returns:
            bool: Returns True if the Entity can be collided with and False otherwise.
        """
        return self.collidable

    def __str__(self) -> str:
        """
        Returns the string representation of the Entity. e.g. "Entity('Entity')"

        Returns:
            s(str): Return the string representation of the Entity.
        """
        s = "Entity('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()


class Wall(Entity):
    """
    A Wall is a special type of an Entity within the game.
    The Wall Entity cannot be collided with. Wall should be constructed with Wall().
    """

    def __init__(self):
        """
        Constructor of the Wall class.
        """
        self.id = WALL
        self.collidable = False

    def __str__(self) -> str:
        """
        Returns the string representation of the Wall. e.g. "Wall('#')"

        Returns:
            s(str): Return the string representation of the Wall.
        """
        s = "Wall('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()


class Item(Entity):
    """
    An Item is a special type of an Entity within the game. This is an abstract class.
    By default the Item Entity can be collided with. Item should be constructed with Item().
    """

    def __str__(self) -> str:
        """
        Returns the string representation of the Wall. e.g. "Item('Entity')"

        Returns:
            s(str): Return the string representation of the Wall.
        """
        s = "Item('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()

    def on_hit(self, game: GameLogic):
        """
        This function should raise the NotImplementedError.

        Parameters:
            game(GameLogic): The game.
        """
        raise NotImplementedError



class Key(Item):
    """
    A Key is a special type of Item within the game.
    The Key Item can be collided with. Key should be constructed with Key().
    """

    def __init__(self):
        """
        Constructor of the Key class.
        """
        self.id = KEY
        self.collidable = True

    def __str__(self) -> str:
        """
        Returns the string representation of the Key. e.g. "Key('K')"

        Returns:
            s(str): Return the string representation of the Key.
        """
        s = "Key('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()

    def on_hit(self, game: GameLogic) -> None:
        """
        When the player takes the Key the Key should be added to the Player’s inventory. The Key should then be
        removed from the dungeon once it’s in the Player’s inventory.

        Parameters:
            game(GameLogic): The game.
        """
        player = game.get_player()
        player.add_item(self)
        i, j = game.get_positions(KEY)[0]
        game._dungeon[i][j] = SPACE


class MoveIncrease(Item):
    """
    MoveIncrease is a special type of Item within the game. The MoveIncrease Item can be collided with. MoveIncrease
    should be constructed with MoveIncrease(moves=5: int) where moves describe how many extra moves the Player will be
    granted when they collect this Item, the default value should be 5.
    """

    def __init__(self, moves=5):
        """
        Constructor of the MoveIncrease class.

        Parameters:
            moves(int): moves describe how many extra moves the Player will be granted when they collect this Item.
        """
        self.id = MOVE_INCREASE
        self.collidable = True
        self.moves = moves

    def __str__(self) -> str:
        """
        Returns the string representation of the MoveIncrease. e.g. "MoveIncrease('M')"

        Returns:
            s(str): Return the string representation of the MoveIncrease.
        """
        s = "MoveIncrease('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()

    def on_hit(self, game) -> None:
        """
        When the player hits the MoveIncrease (M) item the number of moves for the player increases and the M item is
        removed from the game. These actions are implemented via the on_hit method. Specifically, extra moves should
        be granted to the Player and the M item should be removed from the game.

        Parameters:
            game(GameLogic): The game.
        """
        game.get_player().change_move_count(self.moves)
        i, j = game.get_positions(MOVE_INCREASE)[0]
        game._dungeon[i][j] = SPACE


class Door(Entity):
    """
    A Door is a special type of an Entity within the game. The Door Entity can be collided with (The Player should be
    able to share its position with the Door when the Player enters the Door.) Door should be constructed with Door().
    """

    def __init__(self):
        """
        Constructor of the Door class.
        """
        self.id = DOOR
        self.collidable = True

    def __str__(self) -> str:
        """
        Returns the string representation of the Door. e.g. "Door('D')"

        Returns:
            s(str): Return the string representation of the Door.
        """
        s = "Door('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()

    def on_hit(self, game: GameLogic) -> None:
        '''t'''
        player = game.get_player()
        inventory = player.get_inventory()
        if inventory:
            game.set_win(True)
        else:
            print("You don't have the key!")



class Player(Entity):
    """
    A Player is a special type of an Entity within the game. The Player Entity can be collided with. The Player
    should be constructed with Player(move_count: int) where moves represents how many moves a Player can have for
    the given dungeon they are in (see GAME_LEVELS).
    """

    def __init__(self, move_count):
        """
        Constructor of the Player class.

        Parameters:
            move_count(int): moves represents how many moves a Player can have for the given dungeon they are in.
        """
        self.id = PLAYER
        self.collidable = True
        self.move_count = move_count
        self.position = None
        self.inventory = []

    def set_position(self, position):
        """
        Sets the position of the Player.

        Parameters
            position(tuple<int, int>): The position of the Player.
        """
        self.position = position

    def get_position(self) -> tuple:
        """
        Returns a tuple of ints representing the position of the Player. If the Player’s position hasn’t been set yet
        then this method should return None.

        Returns:
            self.position(tuple<int, int>): Returns a tuple of ints representing the position of the Player.
        """
        return self.position

    def change_move_count(self, number):
        """
        Add the number to the Player’s move count.

        Parameters
            number(int): number to be added to the Player’s move count.
        """
        self.move_count += number

    def moves_remaining(self) -> int:
        """
        Returns an int representing how many moves the Player has left before they reach the maximum move count.

        Returns: self.move_count(int): Returns an int representing how many moves the Player has left before they
        reach the maximum move count.
        """
        return self.move_count

    def add_item(self, item):
        """
        Adds the item to the Player’s Inventory.

        Parameters:
            item(Entity): the item to be added to the Player’s Inventory.
        """
        self.inventory.append(item)

    def get_inventory(self) -> list:
        """
        Returns a list that represents the Player’s inventory. If the Player has nothing in their inventory then an
        empty list should be returned.

        Returns:
            self.inventory(list<Entity>): Returns a list that represents the Player’s inventory.
        """
        return self.inventory

    def __str__(self) -> str:
        """
        Returns the ​string representation of the Player​. e.g. "Player('O')"

        Returns:
            s(str): Returns the ​string representation of the Player
        """
        s = "Player('" + self.id + "')"
        return s

    def __repr__(self) -> str:
        """
        Same as str(self).
        """
        return self.__str__()


class AbstractGrid(tk.Canvas): 
    def __init__(self, master, rows, cols, width, height, **kwargs):
        """
        Constructor of the AbstractGrid class.

        Parameters
            master
            rows
            cols
            width
            height
            **kwargs :‘**kwargs’ signifies that any named arguments supported by tk.Canvas class
        """
        self.master = master
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.dx = self.width / self.cols
        self.dy = self.height / self.rows
        super(AbstractGrid, self).__init__(master, **kwargs)
    
    def get_bbox(self, position):
        """
        Returns the bounding box for the (row, col) position.

        Parameters
            position: (row, col)
        """
        r, c = position
        X1 = c * self.dx
        Y1 = r * self.dy
        X2 = (c + 1) * self.dx
        Y2 = (r + 1) * self.dy
        return (X1, Y1, X2, Y2)
        
    def pixel_to_position(self, pixel):
        """
        Converts the x, y pixel position (in graphics units) to a (row, col) position

        Parameters
            pixel: pixel position (in graphics units)
        """
        x, y = pixel
        c = int(x // self.dx)
        r = int(y // self.dy)
        return (r, c)
        
    def get_position_center(self, position):
        """
        Gets the graphics coordinates for the center of the cell at the given (row, col) position.

        Parameters
            position: (row, col)
        """
        X1, Y1, X2, Y2 = self.get_bbox(position)
        Xm = int((X1 + X2)/2)
        Ym = int((Y1 + Y2)/2)
        return (Xm, Ym)
        
    def annotate_position(self, position, text):
        """
        Annotates the cell at the given (row, col) position with the provided text

        Parameters
            position: (row, col)
            text
        """
        lbl_pos = self.get_position_center(position)
        self.create_text(lbl_pos, text = text)


class DungeonMap(AbstractGrid):
    def __init__(self, master, size, width=600, **kwargs):
        """
        Constructor of the DungeonMap class.

        Parameters
            master
            size
            width
            kwargs
        """
        super(DungeonMap, self).__init__(master, size, size, width, width, **kwargs)
    
    def draw_grid(self, dungeon, player_position):
        """
        Draws the dungeon on the DungeonMap based on dungeon, and draws the player at the specified (row, col) position.

        Parameters
            dungeon
            player_position: the specified (row, col) position which player at
        """
        wall_pos = []
        key_pos = []
        moveincrease_pos = []
        door_pos = []
        for row, line in enumerate(dungeon):
            for col, char in enumerate(line):
                if char == WALL:
                    wall_pos.append((row, col))
                elif char == KEY:
                    key_pos.append((row, col))
                elif char == MOVE_INCREASE:
                    moveincrease_pos.append((row, col))
                elif char == DOOR:
                    door_pos.append((row, col))

        bbox_player = self.get_bbox(player_position)
        self.create_rectangle(bbox_player, fill = "#00fa9a")
        self.annotate_position(player_position,"Ibis")

        if len(key_pos)>0:
            bbox_key = self.get_bbox(key_pos[0])
            self.create_rectangle(bbox_key, fill = "yellow")
            self.annotate_position(key_pos[0], "Trash")
        
        if len(moveincrease_pos)>0:
            bbox_moveincrease = self.get_bbox(moveincrease_pos[0])
            self.create_rectangle(bbox_moveincrease, fill = "orange")
            self.annotate_position(moveincrease_pos[0], "Banana")

        if len(door_pos)>0:
            bbox_door = self.get_bbox(door_pos[0])
            self.create_rectangle(bbox_door, fill = "red")
            self.annotate_position(door_pos[0], "Nest")

        for i, item in enumerate(wall_pos):
            bbox_wall = self.get_bbox(item)
            self.create_rectangle(bbox_wall, fill = "#a9a9a9")


class KeyPad(AbstractGrid):
    def __init__(self, master, width=200, height=100, **kwargs):
        """
        Constructor of the KeyPad class.

        Parameters
            master
            width
            height
            kwargs
        """
        super(KeyPad, self).__init__(master, 1, 2, width, height, **kwargs) #Call the constructor of the parent class
        self.bN = (0, 1)
        self.bW = (1, 0)
        self.bS = (1, 1)
        self.bE = (1, 2)
        
        bbox_N = self.get_bbox(self.bN)
        self._N = self.create_rectangle(bbox_N, fill = "#a9a9a9")
        self.annotate_position(self.bN, "N")
        
        bbox_W = self.get_bbox(self.bW)
        self._W = self.create_rectangle(bbox_W, fill = "#a9a9a9")
        self.annotate_position(self.bW, "W")
        
        bbox_S = self.get_bbox(self.bS)
        self._S = self.create_rectangle(bbox_S, fill = "#a9a9a9")
        self.annotate_position(self.bS, "S")
        
        bbox_E = self.get_bbox(self.bE)
        self._E = self.create_rectangle(bbox_E, fill = "#a9a9a9")
        self.annotate_position(self.bE, "E")
    
    def pixel_to_direction(self, pixel):
        """
        Converts the x, y pixel position to the direction of the arrow depicted at that position.

        Parameters
            pixel
        """
        p = self.pixel_to_position(pixel)
        if p == self.bN:
            return "W"
        elif p == self.bW:
            return "A"
        elif p == self.bS:
            return "S"
        elif p == self.bE:
            return "D"


class AdvancedDungeonMap(AbstractGrid):
    def __init__(self, master, size, width=600, **kwargs):
        """
        Constructor of the AdvancedDungeonMap class.

        Parameters
            master
            size
            width
            **kwargs
        """
        super(AdvancedDungeonMap, self).__init__(master, size, size, width, width, **kwargs)

    def draw_grid(self, dungeon, player_position):
        """
        Draws the dungeon on the DungeonMap based on dungeon, and draws the player at the specified (row, col) position.

        Parameters
            dungeon
            player_position
        """
        wall_pos = []
        key_pos = []
        moveincrease_pos = []
        door_pos = []
        empty_pos = []
        empty_pos.append(player_position)
        for row, line in enumerate(dungeon):
            for col, char in enumerate(line):
                if char == WALL:
                    wall_pos.append((row, col))
                elif char == KEY:
                    key_pos.append((row, col))
                    empty_pos.append((row, col))
                elif char == MOVE_INCREASE:
                    moveincrease_pos.append((row, col))
                    empty_pos.append((row, col))
                elif char == DOOR:
                    door_pos.append((row, col))
                    empty_pos.append((row, col))
                else:
                    if (row, col) != player_position:
                        empty_pos.append((row, col))

        global p_wall
        wall = Image.open('images/wall.png')
        wall = wall.resize((int(self.dx), int(self.dy)))
        p_wall = ImageTk.PhotoImage(wall)
        for i, item in enumerate(wall_pos):
            (x, y) = self.get_position_center(item)
            self.create_image(x, y, image=p_wall, anchor='center')

        global p_empty
        empty = Image.open('images/empty.png')
        empty = empty.resize((int(self.dx), int(self.dy)))
        p_empty = ImageTk.PhotoImage(empty)
        for i, item in enumerate(empty_pos):
            (x, y) = self.get_position_center(item)
            self.create_image(x, y, image=p_empty, anchor='center')

        global p_key
        if len(key_pos) > 0:
            key = Image.open('images/key.png')
            key.thumbnail((self.dx, self.dy))
            p_key = ImageTk.PhotoImage(key)
            (x, y) = self.get_position_center(key_pos[0])
            self.create_image(x, y, image=p_key, anchor='center')

        global p_moveincrease
        if len(moveincrease_pos) > 0:
            moveincrease = Image.open('images/moveIncrease.png')
            moveincrease.thumbnail((self.dx, self.dy))
            p_moveincrease = ImageTk.PhotoImage(moveincrease)
            (x, y) = self.get_position_center(moveincrease_pos[0])
            self.create_image(x, y, image=p_moveincrease, anchor='center')

        global p_door
        if len(door_pos) > 0:
            door = Image.open('images/door.gif')
            door.thumbnail((self.dx, self.dy))
            p_door = ImageTk.PhotoImage(door)
            (x, y) = self.get_position_center(door_pos[0])
            self.create_image(x, y, image=p_door, anchor='center')

        global p_player
        player = Image.open('images/player.png')
        player.thumbnail((self.dx, self.dy))
        p_player = ImageTk.PhotoImage(player)
        (x, y) = self.get_position_center(player_position)
        self.create_image(x, y, image=p_player, anchor='center')


class StatusBar(AbstractGrid):
    def __init__(self, master, width=800, **kwargs):
        """
        Constructor of the StatusBar class.

        Parameters
            master
            width
            **kwargs
        """
        super(StatusBar, self).__init__(master, 1, 5, width, 100, **kwargs)
        self.btn_frm = tk.Frame(self)
        self.btn_newgame = tk.Button(self.btn_frm, text="New game")
        self.btn_quit = tk.Button(self.btn_frm, text="Quit")

    def draw(self, t, m):
        """
        Draw the statusbar for the game (TASK_TWO).

        Parameters
            t: time cost
            m: moves left
        """
        global p_clock
        global p_lightning

        self.btn_newgame.config(font=('Arial', 14))
        self.btn_newgame.grid(row=0, column=0)

        self.btn_quit.config(font=('Arial', 14))
        self.btn_quit.grid(row=1, column=0)
        self.btn_frm.grid(row=0, column=0)

        clock = Image.open('images/clock.png')
        clock.thumbnail((100, 100))
        p_clock = ImageTk.PhotoImage(clock)
        lb_clock = tk.Label(self, image=p_clock)
        lb_clock.grid(row=0, column=1)

        time_frm = tk.Frame(self)
        Time_title = tk.Label(time_frm, text="Time elapsed")
        Time_title.config(font=('Arial', 14))
        Time_title.grid(row=0, column=0)
        Time = tk.Label(time_frm, text= str(t))
        Time.config(font=('Arial', 14))
        Time.grid(row=1, column=0)
        time_frm.grid(row=0, column=2)

        lightning = Image.open('images/lightning.png')
        lightning.thumbnail((100, 100))
        p_lightning = ImageTk.PhotoImage(lightning)
        lb_lightning = tk.Label(self, image=p_lightning)
        lb_lightning.grid(row=0, column=3)

        move_frm = tk.Frame(self)
        Moves_title = tk.Label(move_frm, text="Moves left")
        Moves_title.config(font=('Arial', 14))
        Moves_title.grid(row=0, column=0)
        moves = tk.Label(move_frm, text= str(m) + " moves remaining")
        moves.config(font=('Arial', 14))
        moves.grid(row=1, column=0)
        move_frm.grid(row=0, column=4)


TASK_ONE = 1
TASK_TWO = 2

class GameApp():
    def __init__(self, master, task=TASK_ONE, dungeon_name="game2.txt"):
        """
        Constructor of the GameApp class.

        Parameters
            master
            task: TASK_ONE or TASK_TWO
            dungeon_name
        """
        self._dungeon_name = dungeon_name
        self._game = GameLogic(self._dungeon_name)
        self._master = master

        self._fr_game = tk.Frame(self._master)
        self._fr_game.columnconfigure(0, minsize=600)
        self._fr_game.columnconfigure(1, minsize=200)
        self._fr_game.rowconfigure(0, minsize=600)

        self._direction = ''
        self._end = False
        self._task = task

        self.start = time.time()
        self.timeoffset = 0
        self.t = 0

        self.keypad = KeyPad(self._fr_game, 200, 50)

        if self._task == TASK_TWO:
            self._fr_bar = tk.Frame(self._master)
            self.status = StatusBar(self._fr_bar)
            self.menubar = tk.Menu(self._master)
            self.menubar.add_command(label="Save game", command=self.savegame)
            self.menubar.add_command(label="Load game", command=self.loadgame)
            self.menubar.add_command(label="New game", command=self.newgame)
            self.menubar.add_command(label="Quit", command=self.quit)

    def play(self):
        """
        Handles the player interaction.
        """
        text0 = 'You have finished the level!'
        text1 = 'You have finished the level with a score of '
        text2 = 'Would you like to play again?'

        if not self._game.won() and not self._game.check_game_over():
            title = tk.Label(self._master, text="Key Cave Adventure Game", bg = "#00fa9a")
            title.config(font=('Arial', 30))
            title.grid(row=0, column=0, sticky='nsew')

            if self._task == TASK_ONE:
                self.Dungeon = DungeonMap(self._fr_game, self._game._dungeon_size, 600, bg="#d3d3d3")
            elif self._task == TASK_TWO:
                self.Dungeon = AdvancedDungeonMap(self._fr_game, self._game._dungeon_size, 600)
                self.gettime()
                m = self._game._player.moves_remaining()
                min = self.t // 60
                sec = self.t - min * 60
                self.status.draw(str(min) + 'm' + str(sec) + 's', m)
                self.status.grid(row=0, column=0, sticky='nsew')
                self.status.btn_quit.bind('<Button-1>', self.quit)
                self.status.btn_newgame.bind('<Button-1>', self.newgame)
                self._master.config(menu=self.menubar)
                self._fr_bar.grid(row=2, column=0, sticky='nsew')

            self.Dungeon.draw_grid(self._game._dungeon, self._game.get_player().get_position())

            self.keypad.bind("<Button-1>", self.on_Button)
            self._master.bind("<Key>", self.on_key_press)

            self.Dungeon.grid(row=0, column=0, sticky='nsew')
            self.keypad.grid(row=0, column=1, sticky='sw')

            self._master.after(50, self.play)
            self._fr_game.grid(row=1, column=0, sticky='nsew')

        elif self._game.won() and not self._end:
            if self._task == TASK_ONE:
                tk.messagebox.showinfo('You Won!', text0)
                self.quit()
            elif self._task == TASK_TWO:
                response = tk.messagebox.askyesno('You Won!', text1 + str(self.t) +'\n'+ text2)
                if response == True:
                    self.newgame()
                    self.play()
                else:
                    self.quit()
        elif self._game.check_game_over() and not self._end:
            if self._task == TASK_ONE:
                tk.messagebox.showinfo('You Losed!', LOSE_TEST)
                self.quit()
            elif self._task == TASK_TWO:
                response = tk.messagebox.askyesno('You Losed!', LOSE_TEST + '\n' + text2)
                if response == True:
                    self.newgame()
                    self.play()
                else:
                    self.quit()


    def gettime(self):
        """
        Get the game time.
        """
        now = time.time()
        self.t = int(now - self.start) + self.timeoffset

    def quit(self, event=0):
        """
        Quit the game.
        Parameters
        """
        response = tk.messagebox.askyesno('Quit?','Are you sure you would like to quit the game?')
        if response == True:
            self._end = True
            self._master.destroy()

    def newgame(self, event=0):
        """
        Restart the game.
        """
        self.start = time.time()
        self._game = GameLogic(self._dungeon_name)

    def on_Button(self, event):
        """
        Click the KeyPad to control the player.
        """
        self._direction = self.keypad.pixel_to_direction((event.x, event.y))
        self.move(self._direction)

    def on_key_press(self, event):
        """
        Press the Key to control the player.
        """
        c = event.char
        if c == 'w':
            self._direction = 'W'
        elif c == 's':
            self._direction = 'S'
        elif c == 'a':
            self._direction = 'A'
        elif c == 'd':
            self._direction = 'D'
        self.move(self._direction)

    def move(self, direction):
        """
        Move the player according to the direction.

        Parameters
            direction: 'W', 'S' ,'A' or 'D'
        """
        if direction in DIRECTIONS:
            entity = self._game.get_entity_in_direction(direction)
            if not self._game.collision_check(direction):
                self._game.move_player(direction)
            else:
                tk.messagebox.showinfo('Warn', INVALID)
            self._game.get_player().change_move_count(-1)
            if entity and entity.can_collide():
                entity.on_hit(self._game)

    def savegame(self):
        """
        Prompt the user for the location to save their file(.txt) and save all necessary information to replicate the current
        state of the game.
        Information saved include:
            time cost
            player's moves remaining
            player's position
            dungeon name
        """
        file_path = filedialog.askopenfilename()
        with open(file_path, 'w') as f:
            m = self._game._player.moves_remaining()
            ply = self._game._player.get_position()
            f.write(str(self.t)+'\n')
            f.write(str(m)+'\n')
            f.write(str(ply)+ '\n')
            f.write(self._dungeon_name)

    def loadgame(self):
        """
        Prompt the user for the location of the file(.txt) to load a game from and load the
        game described in that file.
        """
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r') as f:
            self.start = time.time()
            self.timeoffset = int(f.readline())
            self._game._player.move_count = int(f.readline())
            position_str = f.readline()
            self._game._player.position = (int(float(position_str[1])), int(float(position_str[4])))
            self._dungeon_name = f.readline()

def main():
    master = tkinter.Tk()
    game = GameApp(master, TASK_TWO, "game2.txt") # TASK_ONE or TASK_TWO
    game.play()
    master.mainloop()

if __name__ == "__main__":
    main()
