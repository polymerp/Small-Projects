"""Car Racing Game."""

from tkinter import *
import random


class GUI:
    """Menu GUI.

    Attributes:
        self.GAME_WIDTH: Width of game window (pixels)
        self.GAME_HEIGHT: Height of game window (pixels)

        self.VERT_PAD:
        The vertical padding which the player is restricted from moving into
        (on vertical axis)

        self.MENU_WIDTH: Width of menu window (pixels)
        self.MENU_HEIGHT: Height of menu window (pixels)

        self.CAR_WIDTH: Width of all cars (pixels)
        self.CAR_HEIGHT: Height of all cars (pixels)

        self.POS_MULT: Multiplier for positive movement along axis
        self.NEG_MULT: Multiplier for negative movement along axis

        self.BUTTON_WIDTH:
        Width of buttons on main menu based on width of menu

        self.START_Y:
        self.TUTORIAL_Y:
        self.QUIT_Y:

        self.SPAWNING_VELOCITY: Speed at which enemies start spawning
        self.SPAWN_SPEED:
        self.UPDATE_RATE:

        self.LIFE_ICON_SIZE:
        Width/Height of life icons

        self.LIFE_PADDING:
        Padding between the life icons

        self.LIVES_NUM:
        Number of lives/strikes the player can reach before the game is over

        self.LANE_NUMBER:
        Number of lanes -1 as range includes
        (0,self.LANE_NUMBER)

        self.HIT_SPEED:
        Speed which the player needs to reach
        for the hit condition to be complete
    """

    GAME_WIDTH = 1000
    GAME_HEIGHT = 436
    VERT_PAD = 10

    MENU_WIDTH = 500
    MENU_HEIGHT = 375

    CAR_WIDTH = 65
    CAR_HEIGHT = 40

    POS_MULT = 1
    NEG_MULT = -1

    BUTTON_WIDTH = int(MENU_WIDTH / 10)
    START_Y = MENU_HEIGHT * (3 / 5)
    TUTORIAL_Y = START_Y + 45
    QUIT_Y = TUTORIAL_Y + 45

    SPAWNING_VELOCITY = 7
    SPAWN_SPEED = 200
    UPDATE_RATE = 16

    LIFE_ICON_SIZE = 10
    LIFE_PADDING = 10
    LIVES_NUM = 3

    LANE_NUMBER = 7

    HIT_SPEED = -2

    def __init__(self):
        """Initializes the GUI class.

        Parameters
            self.root: Program's Window

            self.canvas: Program's Tkinter canvas

            self.score: Current player's score

            self.start_button:
            Instance of a button in the main menu to start game
            self.tutorial_button:
            Instance of a button in the main menu to open tutorial screen
            self.quit_button:
            Instance of a button in the main menu to close the app
            self.return_button:
            Instance of a button in the tutorial menu
            to return to the main screen

            self.player: Instance of the player
            self.start_text: Text shown on screen at beginning of the game
            self.game_background: Instance of the background for the game
            self.explode: Instance of explosion visual effect

            self.car_on:
            Whether the player has started the game
            (True/False)

            self.enemy_list:
            List of ids of enemies on screen

            self.acceleration:
            The speed at which the enemies travel
            (changes causing acceleration effect)

            self.keys_binded:
            Whether WASD is bound to movement controls
            (True/False)

            self.lives: List of life icon objects on canvas during game
            self.strikes: The number of strikes (collisions) the player has had

            self.EXPLODE_SPRITE:
            Sprite for explosion
            (has to be defined after root is created)

            self.BACKGROUND_IMAGE:
            Background image for game
            (has to be defined after root is created)

            self.MENU_IMAGE:
            Wallpaper image for the Main Menu
            (has to be defined after root is created)
        """

        #   DEFINING CORE VARIABLES
        self.root = Tk()
        self.root.geometry(f"{self.MENU_WIDTH}x{self.MENU_HEIGHT}")
        self.root.title("Box Racing - Main Menu")

        self.canvas = None  # Canvas isn't needed yet so use None
        self.wallpaper_canvas = Canvas(
            self.root,
            width=self.MENU_WIDTH,
            height=self.MENU_HEIGHT,
            bg="Black"
        )

        #   DEFINING SPRITE VARIABLES
        #       Has to be after root is created
        self.EXPLODE_SPRITE = PhotoImage(file='hit1.png')
        self.BACKGROUND_SPRITE = PhotoImage(file='background.png')
        self.MENU_IMAGE = PhotoImage(file='wallpaper.png')

        #   SCORE VARIABLES
        self.score = 0

        #   SET WALLPAPER FOR MAIN MENU
        self.wallpaper_canvas.create_image(
            0, 0,
            image=self.MENU_IMAGE,
            anchor=NW)

        #   DEFINING/PACKING MENU BUTTONS
        self.start_button = Button(
            self.root,
            text='Start',
            width=self.BUTTON_WIDTH,
            bd='5',
            command=self.load_game)

        self.start_button.place(
            x=self.MENU_WIDTH / 2,
            #   Divided by 2 to get centre
            y=self.START_Y,
            anchor='center')

        self.tutorial_button = Button(
            self.root,
            text='Tutorial',
            width=self.BUTTON_WIDTH,
            bd='5',
            command=self.set_tutorial)

        self.tutorial_button.place(
            x=self.MENU_WIDTH / 2,
            #   Divided by 2 to get centre
            y=self.TUTORIAL_Y,
            anchor='center')

        self.quit_button = Button(
            self.root,
            text='Quit',
            width=self.BUTTON_WIDTH,
            bd='5',
            command=self.root.destroy)

        self.quit_button.place(
            x=self.MENU_WIDTH / 2,
            #   Divided by 2 to get centre
            y=self.QUIT_Y,
            anchor='center')

        self.return_button = None
        # return_button isn't created yet so use None

        #   DEFINING CANVAS OBJECTS
        self.player = None
        # player isn't created yet so use None
        self.start_text = None
        # start_text isn't created yet so use None
        self.game_background = None
        # game_background isn't created yet so use None
        self.explode = None
        # explode isn't created yet so use None

        #   DEFINING GAME VARIABLES
        self.car_on = False
        self.enemy_list = []  # Enemies aren't created yet so empty
        self.acceleration = 0
        self.keys_binded = False

        self.lives = []
        self.strikes = 0

        self.wallpaper_canvas.pack()
        self.root.mainloop()

    #   ----- WINDOW SET UP -----

    def start_menu(self):
        """Changes screen to start menu.
        """
        #   Not redundant as the game may be
        #   restarted prior to space keypress
        self.clear_root()
        self.root.geometry(f"{self.MENU_WIDTH}x{self.MENU_HEIGHT}")
        self.root.title("Box Racing - Main Menu")
        self.root.unbind("<space>")
        self.keybind(False)
        self.canvas = None
        self.player = None
        self.game_background = None
        self.lives = []
        self.enemy_list = []

        self.wallpaper_canvas = Canvas(
            self.root,
            width=self.MENU_WIDTH,
            height=self.MENU_HEIGHT,
            bg="Black"
        )

        #   SET WALLPAPER FOR MAIN MENU
        self.wallpaper_canvas.create_image(
            0, 0,
            image=self.MENU_IMAGE,
            anchor=NW)

        self.wallpaper_canvas.pack()

        self.start_button = Button(
            self.root,
            text='Start',
            width=self.BUTTON_WIDTH,
            bd='5',
            command=self.load_game)

        self.start_button.place(
            x=self.MENU_WIDTH / 2,
            #   Divided by 2 to get centre
            y=self.START_Y,
            anchor='center')

        self.tutorial_button = Button(
            self.root,
            text='Tutorial',
            width=self.BUTTON_WIDTH,
            bd='5',
            command=self.set_tutorial)

        self.tutorial_button.place(
            x=self.MENU_WIDTH / 2,
            #   Divided by 2 to get centre
            y=self.TUTORIAL_Y,
            anchor='center')

        self.quit_button = Button(
            self.root,
            text='Quit',
            width=self.BUTTON_WIDTH,
            bd='5',
            command=self.root.destroy)

        self.quit_button.place(
            x=self.MENU_WIDTH / 2,
            #   Divided by 2 to get centre
            y=self.QUIT_Y,
            anchor='center')

    def load_game(self):
        """Changes screen to new game.
        """
        self.clear_root()
        self.root.geometry(f"{self.GAME_WIDTH}x{self.GAME_HEIGHT}")
        self.root.title("Box Racing - Game Screen")
        self.canvas = Canvas(
            self.root,
            width=self.GAME_WIDTH,
            height=self.GAME_HEIGHT,
            bg="Black"
        )
        self.wallpaper_canvas = None
        self.canvas.pack()

        #   SET VARIABLES
        self.acceleration = 0
        self.score = 0

        #   SET KEY-BINDS
        self.root.bind("<space>", self.start_car)
        self.keybind(True)
        self.root.focus_set()

        #   CREATE OBJECTS
        self.game_background = self.canvas.create_image(
            0,
            0,
            image=self.BACKGROUND_SPRITE,
            anchor=NW
        )
        self.player = Car(self.canvas)
        for i in range(self.LIVES_NUM):
            print(i)
            self.lives.append(
                self.canvas.create_rectangle(
                    self.LIFE_PADDING +
                    i * self.LIFE_PADDING,
                    self.LIFE_PADDING,
                    self.LIFE_PADDING +
                    i * self.LIFE_PADDING +
                    self.LIFE_ICON_SIZE,
                    self.LIFE_PADDING + self.LIFE_ICON_SIZE,
                    fill="red"
                ))
        self.start_text = self.canvas.create_text(
            self.GAME_WIDTH / 2,
            self.GAME_HEIGHT / 2,
            text=f"press\n"
                 f"[SPACE]\n"
                 f"to start car",
            fill="White",
            font="Helvetica 26 bold"
        )

        self.root.update()

    def set_tutorial(self):
        """Sets the Menu to the tutorial.

        Parameters
            tutorial_text:
            text which is displayed on tutorial page
        """
        self.clear_root()
        self.root.geometry(f"{self.MENU_WIDTH}x{self.MENU_HEIGHT}")
        self.root.unbind("<space>")
        self.keybind(False)
        self.canvas = None
        self.player = None
        self.lives = ()

        tutorial_text = Label(self.root,
                              text="\n\nThis game is all about weaving\n"
                                   " and dodging through traffic.\n"
                                   "You can use WASD to control the car\n"
                                   "and you will need to\n\n"
                                   "start the car by pressing [SPACE]\n"
                                   " You are given 3 Lives which "
                                   "can be seen in\nthe top left "
                                   "corner of the screen\n\n"
                                   "Alt can temporarily pause the game\n"
                                   "until the next input")
        tutorial_text.pack()
        tutorial_text.config(font=("Courier", 11))

        self.return_button = Button(
            self.root,
            text='Return to Main Menu',
            width=self.BUTTON_WIDTH,
            bd='5',
            command=self.start_menu)

        self.return_button.place(
            x=self.MENU_WIDTH / 2,
            #   Divided by 2 to centre
            y=self.QUIT_Y,
            anchor='center')

    def keybind(self, is_press):
        """Binds/unbinds keys to car controls.

        Arguments:
            is_press:
            Whether the player needs key-binds
            (True/False)
        """
        if is_press:
            self.keys_binded = True
            #       KEY-PRESSES
            self.root.bind(
                "<w>",
                lambda _: self.player.vert_calc('press', self.NEG_MULT))
            self.root.bind(
                "<a>",
                lambda _: self.player.hori_calc('press', self.NEG_MULT))
            self.root.bind(
                "<s>",
                lambda _: self.player.vert_calc('press', self.POS_MULT))
            self.root.bind(
                "<d>",
                lambda _: self.player.hori_calc('press', self.POS_MULT))
            #       KEY-RELEASES
            self.root.bind(
                "<KeyRelease-w>",
                lambda _: self.player.vert_calc('release', self.NEG_MULT))
            self.root.bind(
                "<KeyRelease-a>",
                lambda _: self.player.hori_calc('release', self.NEG_MULT))
            self.root.bind(
                "<KeyRelease-s>",
                lambda _: self.player.vert_calc('release', self.POS_MULT))
            self.root.bind(
                "<KeyRelease-d>",
                lambda _: self.player.hori_calc('release', self.POS_MULT))
        elif not is_press:
            self.keys_binded = False
            self.root.unbind("<w>")
            self.root.unbind("<KeyRelease-w>")
            self.root.unbind("<a>")
            self.root.unbind("<KeyRelease-a>")
            self.root.unbind("<s>")
            self.root.unbind("<KeyRelease-s>")
            self.root.unbind("<d>")
            self.root.unbind("<KeyRelease-d>")

    def start_car(self, _):
        """Changes the score to 1 telling the game it has started.
        """
        self.root.unbind("<space>")
        self.canvas.delete(self.start_text)
        print("start")
        self.car_on = True
        self.frame()
        self.enemy_calculate()

    def clear_root(self):
        """Clears the canvas of all objects and resets a few variables.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        self.strikes = 0
        #   Short function but used a fair bit.

    #   ----- GENERATE ENEMY -----
    def enemy_calculate(self):
        """Depending on time spawn different amount of cars.
        """
        if self.car_on:
            if self.keys_binded:
                if self.acceleration >= GUI.SPAWNING_VELOCITY:
                    print("spawn")
                    self.enemy_spawn()
                elif self.acceleration < GUI.SPAWNING_VELOCITY:
                    self.acceleration += 1
            self.root.after(self.SPAWN_SPEED, self.enemy_calculate)

    def enemy_spawn(self):
        """Spawns in enemy.

        Parameters
            current_enemy:
            Specific enemy which is being created
            (is append-ed to a class list)
        """
        current_enemy = Enemy(
            self.canvas,
            random.randint(0, self.LANE_NUMBER),
            self.GAME_WIDTH,
            self.enemy_list)
        if current_enemy.id is not None:
            self.enemy_list.append(current_enemy)

    def enemy_hit(self):
        """Processes enemy hit.

        Slow down car and do appropriate actions
        to player when they hit a car
        """
        self.keybind(False)
        self.player.x_vel = 0
        self.player.y_vel = 0
        self.player.last_x_direction = None
        self.player.last_y_direction = None

        if self.explode is not None:
            self.canvas.delete(self.explode)
            self.explode = None

        self.explode = self.canvas.create_image(
            self.player.hitbox[0]+(self.CAR_WIDTH/2),
            self.player.hitbox[1],
            image=self.EXPLODE_SPRITE,
            anchor=NW
        )

        self.strikes += 1
        self.canvas.delete(self.lives[-1])
        self.lives.pop(-1)
        if self.strikes < self.LIVES_NUM:
            self.acceleration -= 1
        else:
            self.car_on = False
            self.canvas.create_text(
                self.GAME_WIDTH / 2,
                self.GAME_HEIGHT / 2,
                text=f"GAME OVER!\n"
                     f"score: {self.score} points!\n\n"
                     f"press [SPACE] to restart",
                fill="White",
                font="Helvetica 26 bold")
        self.root.update()

    #   ----- PLAYER COLLISIONS -----
    def move_scene(self):
        """Moves the player car.
        """
        #   MOVE CAR ALONG X
        if self.keys_binded:
            if (not self.canvas.coords(self.player.id)[0]
                    + self.player.x_vel <= 0
                    and not
                    self.canvas.coords(self.player.id)[0]
                    + self.CAR_WIDTH
                    + self.player.x_vel >= GUI.GAME_WIDTH):
                self.canvas.move(
                    self.player.id,
                    self.player.x_vel,
                    0
                )
            #   MOVE CAR ALONG Y
            if (not self.canvas.coords(self.player.id)[1]
                    + self.player.y_vel
                    <= 0 + self.VERT_PAD
                    and not
                    self.canvas.coords(self.player.id)[1]
                    + self.CAR_HEIGHT
                    + self.player.y_vel
                    >= GUI.GAME_HEIGHT - self.VERT_PAD):
                self.canvas.move(
                    self.player.id,
                    0,
                    self.player.y_vel
                )

        #   MOVE ENEMY
        #   Uses i as a temporary variable
        for i in self.enemy_list:
            i.hitbox = self.canvas.coords(i.id)
            self.canvas.move(i.id, -self.acceleration, 0)

            if (i.id in self.canvas.find_overlapping(
                self.player.hitbox[0],
                self.player.hitbox[1],
                self.player.hitbox[0] + self.CAR_WIDTH,
                self.player.hitbox[1] + self.CAR_HEIGHT
            )):
                self.enemy_list.remove(i)
                self.canvas.delete(i.id)
                self.enemy_hit()
            if i.hitbox[0] <= 0 - self.CAR_WIDTH:
                self.enemy_list.remove(i)
                self.canvas.delete(i.id)

    def frame(self):
        """Updates all required values and sprites for each frame of the game.
        """
        if self.car_on:
            self.player.hitbox = self.canvas.coords(self.player.id)
            if not self.keys_binded:
                if self.acceleration <= self.HIT_SPEED:
                    self.keybind(True)
                    self.canvas.delete(self.explode)
                    self.explode = None
                else:
                    self.acceleration -= 0.2
            self.move_scene()
            self.score += 1
            self.root.after(self.UPDATE_RATE, self.frame)
        else:
            self.root.bind(
                "<space>",
                lambda _: self.start_menu())


class Car:
    """Creates controllable player car.

    Attributes:
        self._START_X: The start x coordinate for the player car
        self._START_Y: The start y coordinate for the player car

        self._MAX_SPEED: Speed which the user can travel at
    """

    _START_X = GUI.GAME_WIDTH / 3
    _START_Y = GUI.GAME_HEIGHT / 2

    _MAX_SPEED = 6

    def __init__(self, canvas):
        """Initializes the Car class.

        Arguments:
            canvas: Game canvas

        Parameters
            self.canvas: Game canvas
            self.id: id of player on game canvas
            self.hitbox: coordinates of player

            self.x_vel:
            velocity of the player when moving along x-axis

            self.y_vel:
            velocity of the player when moving along y-axis
        """
        #   Constant defined when called so root exists
        self._SPRITE = PhotoImage(file='player.png')

        #   DEFINING CORE VARIABLES
        self.canvas = canvas
        self.id = canvas.create_image(
            self._START_X,
            self._START_Y,
            image=self._SPRITE,
            anchor=NW
        )
        self.hitbox = self.canvas.coords(self.id)

        #   DEFINING MOVEMENT VARIABLES
        self.x_vel = 0
        self.y_vel = 0
        self.last_x_direction = None
        self.last_y_direction = None

    def vert_calc(self, press_type, direction):
        """Calculates the car's vertical velocity.

        Arguments
            press_type: Whether the input is a key-press or key-release
            direction: The direction the car should travel
        """
        if (press_type == 'press') and (direction != self.last_y_direction):
            self.y_vel = direction * self._MAX_SPEED
            self.last_y_direction = direction

        elif press_type == 'release':
            if self.y_vel == direction * self._MAX_SPEED:
                self.y_vel = 0
                self.last_y_direction = None

    def hori_calc(self, press_type, direction):
        """Calculates the car's horizontal velocity.

        Arguments
            press_type: Whether the input is a key-press or key-release
            direction: The direction the car should travel
        """
        if (press_type == 'press') and (direction != self.last_x_direction):
            self.x_vel = direction * self._MAX_SPEED
            self.last_x_direction = direction

        elif press_type == 'release':
            if self.x_vel == direction * self._MAX_SPEED:
                self.x_vel = 0
                self.last_x_direction = None


class Enemy:
    """Spawns enemy obstacles.

    Attributes
        self._LANE_HEIGHT: The height of each lane
        self._LANE_LIST: List of lanes' top y coord

        self._SPAWN_OFFSET:
        Vertical offset for spawn
        (to not be on edge of lane)
    """

    _LANE_HEIGHT = (GUI.GAME_HEIGHT - 20) / 8
    _LANE_LIST = (
        10,
        10 + _LANE_HEIGHT,
        10 + _LANE_HEIGHT * 2,
        10 + _LANE_HEIGHT * 3,
        10 + _LANE_HEIGHT * 4,
        10 + _LANE_HEIGHT * 5,
        10 + _LANE_HEIGHT * 6,
        10 + _LANE_HEIGHT * 7
    )

    _SPAWN_OFFSET = (_LANE_HEIGHT - GUI.CAR_HEIGHT) / 2

    def __init__(self, canvas, lane_number, x, enemy_list):
        """Initializes the Enemy class.

        Arguments:
            canvas: Game canvas
            lane_number: number of lane to be spawned in
            x: X coordinate at which all cars spawn
            enemy_list: list of enemies

        Parameters
            self._SPRITE: Enemy cars' sprite

            self.canvas: Game canvas
            self.id: id of enemy on game canvas
            self.hitbox: coordinates of enemy
            self.enemy_list: list of enemies
        """

        #   Constant defined when called so root exists
        self._SPRITE = PhotoImage(file='enemy.png')

        self.canvas = canvas
        self.id = canvas.create_image(
            x,
            self._LANE_LIST[lane_number] + self._SPAWN_OFFSET,
            image=self._SPRITE,
            anchor=NW
        )

        self.enemy_list = enemy_list
        self.check_spawn(lane_number, x)

        if self.id is not None:
            self.hitbox = self.canvas.coords(self.id)

        print(self._LANE_LIST)
        print(self._LANE_HEIGHT)

    def check_spawn(self, lane_number, x):
        """Checks whether player can spawn.

        Arguments
            lane_number: number of lane to be spawned in
            x: X coordinate at which all cars spawn
        """
        #   Use i as temporary variable
        for i in self.enemy_list:
            if ((not x > i.hitbox[0]+GUI.CAR_WIDTH)
                    and self._LANE_LIST[lane_number]
                    + self._SPAWN_OFFSET == i.hitbox[1]):
                self.id = None
                self.canvas.delete(self.id)


GUI()
