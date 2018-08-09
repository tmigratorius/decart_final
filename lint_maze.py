# cool game to play, beat the maze and save the day
"""
this module is game 1, the maze game in the multi-game package
the goal is to escape the maze while collecting coins and avoiding enemies
escape each maze level to reach the next!
"""
import turtle
import math
import random

window = turtle.Screen()
window.bgcolor('black')
window.title('Maze Escape')
window.setup(600, 600)
window.tracer(0)

mypen = turtle.Turtle()
mypen.color('white')
mypen.penup()
mypen.hideturtle()
mypen.setposition(-500, 500)
mypen.speed(0)


# draw the maze background
class Blocks(turtle.Turtle):


    """
    the blocks class describes how the maze structure is built
    """
    def __init__(self):
        """
        wall blocks defaults
        """
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('gray')
        self.penup()
        self.speed(0)




# player class, this is the controlled block
class Player(turtle.Turtle):


    """
        the player class describes how the user moves the player square through the maze
    """
    def __init__(self):
        """
        player turtle attributes set-up
        """
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('red')
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        """
        up direction behavior
        """
        # spot to move to
        new_pos_x = self.xcor()
        new_pos_y = self.ycor() + 24
        # is spot occupied, if no, move
        if (new_pos_x, new_pos_y) not in walls:
            self.goto(new_pos_x, new_pos_y)

    def go_left(self):
        """
        left direction behavior
        """
        # spot to move to
        new_pos_x = self.xcor() - 24
        new_pos_y = self.ycor()
        # is spot occupied, if no, move
        if (new_pos_x, new_pos_y) not in walls:
            self.goto(new_pos_x, new_pos_y)

    def go_down(self):
        """
        down direction behavior
        """
        # spot to move to
        new_pos_x = self.xcor()
        new_pos_y = self.ycor() - 24
        # is spot occupied, if no, move
        if (new_pos_x, new_pos_y) not in walls:
            self.goto(new_pos_x, new_pos_y)

    def go_right(self):
        """
        Right direction behavior
        """
        # spot to move to
        new_pos_x = self.xcor() + 24
        new_pos_y = self.ycor()
        # is spot occupied, if no, move
        if (new_pos_x, new_pos_y) not in walls:
            self.goto(new_pos_x, new_pos_y)

    # method to determine if player is hitting any game elements
    def is_collision(self, other):
        """
        how to detect a collision between player and other things
        """
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        # pythagorean theorm to find dist between elements
        dist = math.sqrt((a ** 2) + b ** 2)

        if dist < 5:
            return True
        else:
            return False


# Coins class, pick up money as you go
class Coin(turtle.Turtle):


    """
    the coin class describes how the gold in the maze behaves
    """
    def __init__(self, x, y):
        """
        set up of treasure turtles
        """
        turtle.Turtle.__init__(self)
        self.shape('circle')
        self.color('gold')
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    # hide coin when it is 'pocketed'
    def pocket(self):
        """
        method to 'hide' coins after they are picked up
        """
        self.goto(1000, 1000)
        self.hideturtle()


class BadGuy(turtle.Turtle):


    """
    the BadGuy class describes how the enemies behave and move
    """
    def __init__(self, x, y):
        """
        enemy set-up
        """
        turtle.Turtle.__init__(self)
        self.shape('triangle')
        self.color('green')
        self.penup()
        self.speed(0)
        self.gold = 50
        self.goto(x, y)
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def move(self):
        """
        movement behavior for enemies
        """
        if self.direction == 'up':
            dx = 0
            dy = 24
        elif self.direction == 'down':
            dx = 0
            dy = -24
        elif self.direction == 'left':
            dx = -24
            dy = 0
        elif self.direction == 'right':
            dx = 24
            dy = 0

        # check to see if the player is nearby, if it is, follow
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = 'left'
            elif player.xcor() > self.xcor():
                self.direction = 'right'
            elif player.ycor() < self.xcor():
                self.direction = 'down'
            elif player.xcor() > self.xcor():
                self.direction = 'down'

        # calc the coords bad guy should go to
        goto_x = self.xcor() + dx
        goto_y = self.ycor() + dy

        # does the space you want to go to have a wall?
        if (goto_x, goto_y) not in walls:
            self.goto(goto_x, goto_y)
        else:
            # if it's a wall, go somewhere else
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        # need a timer to move the thig again in a sec
        turtle.ontimer(self.move, t=random.randint(100, 300))

    def is_close(self, other):
        """
        check if enemy is close to player, influences chase behavior
        """
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        dist = math.sqrt((a ** 2) + b ** 2)

        if dist < 75:
            return True
        else:
            return False

    def die(self):
        """
        method to destroy or hide enemies when they are not needed-between levels
        """
        self.goto(1000, 1000)
        self.hideturtle()


class Exit(turtle.Turtle):


    """
    the Exit class is the exit block that triggers movement to next level
    """
    def __init__(self, x, y):
        """
        enemy set-up
        """
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('black')
        self.penup()
        self.speed(0)
        self.goto(x, y)


level_0 = [
    'XXXXXX     XXXXXXXX',
    'XXX       P      XX',
    'XXXX           X XX',
    'XXX   XXXXXXX XXXXX',
    'XX  E  XXXXXX XXXXX',
    'XXXX     XXXX XXXXX',
    'XXXXXXXXXXXXX XXXXX',
    'XX              XXX',
    'X XXX XXXXXXXXX   X',
    'X XXX XXXXX   E  XX',
    'X XXX XXXXX  C   XX',
    'X XXX XX    E   XXX',
    'X XXX XXXXXXXX  XXX',
    'X XXX      C     XX',
    'X   EXXXXXXXXXXX XX',
    'XXC      XXXX XX XX',
    'XXXXX    XXXX XX XX',
    'XXXX             XX',
    'XXXXXXXXXOXXXXXXXXX',
]
level_1 = [
    'XXXXXXPXXXXXXXXXXXX',
    'XXX     XXXXXX X XX',
    'XXXX            EXX',
    'XXXXXXXX         XX',
    'XX C   XXXXX  XXXXX',
    'XXXX     XXXX    XX',
    'XXXXX XXXXXXX XXXXX',
    'XX              XXX',
    'X                 X',
    'X    E  X         X',
    'X XXXXXXXX        X',
    'X XXX XX    E   XXX',
    'X XXX XXXXXXXX  XXX',
    'X XXX      C     XX',
    'X   EXXXXXXXXXXX XX',
    'XXC       XXXCXX XX',
    'XXXXXXXXX     XX XX',
    'XXXXXXXXX CE      X',
    'XXXXXXXXXOXXXXXXXXX',
]
level_2 = [
    'XXXXXXXXXXXXXXXPXXX',
    'XXX XX    XXXX  CXX',
    'XXXX      XXX    XX',
    'XXXX      XXX    XX',
    'XXXX C   XXXX XXXXX',
    'XXXX     XXXX XXXXX',
    'XXXXX XXXXXXX XXXXX',
    'XX   E        XXXXX',
    'XX XXXXXXXXXXXXX  X',
    'X       C         X',
    'XXXXXXXXX         X',
    'XXXXE           XXX',
    'XXXX XXXXXXXX   XXX',
    'XXXX             XX',
    'X    XXXXXXXXXXX XX',
    'XXC        XXXXX XX',
    'XX XXXXXX     XX XX',
    'XX XXXC            X',
    'XXXXXXXXXOXXXXXXXXX',
]
level_3 = [
    'XXXXXXXXXXXXXXXXXXX',
    'XXXP            XXX',
    'XXX XXXXXXXXXXXXXXX',
    'XXX XXXXXXXXXXXXXXX',
    'XXX     XXXXXXXXXXX',
    'XXX XXXXXXXXXXXXXXX',
    'XXX XXXXXXXXXXXXXXX',
    'XXXXXXXXX XXXXXXXXX',
    'XXXXXXXXX XXXXXXXXX',
    'XXXXXXXXX XXXXXXXXX',
    'XXXXXXXXX XXXXXXXXX',
    'XXXXXXXXX XXXXXXXXX',
    'XXXXX XXXXXX XXXXXX',
    'XXXXX X XXXX XXXXXX',
    'XXXXX XX XXX XXXXXX',
    'XXXXX XXX XX XXXXXX',
    'XXXXX XXXX X XXXXXX',
    'XXXXX XXXXX XXXXXXX',
    'XXXXXXXXXXXXXXXXXXX',

]

# List of coin locations
coins = []
# list of bad_guys
bad_guys = []
# exit location
exit_block = []
# score variable
score = 0
# create coord list for wall block positions
walls = []

# construct the list of levels
levels = [level_0, level_1, level_2, level_3]


# make the maze
def make_maze(level):
    """
    this function constructs the maze within the main game loop
    """
    # nested loop, first looks at the 'height' of the level.
    for y in range(len(level)):
        # then goes for the length of that row-which is x
        for x in range(len(level[y])):
            # look at the level map XPECOs, note save that X or P to the var block_type
            # the coordinates are y, x, since it looks at how many rows first, then
            # how long those rows are
            block_type = level[y][x]
            # then get the pixel position of the blocks
            # Our screen is 1000x1000, play area is 900x900.
            # 0,0 is in the center of the screen, so top left edge is at (450,-450)
            # each block is 10
            position_y = 228 - (y * 24)
            position_x = -228 + (x * 24)
            # if theres an X at that position, draw a wall (stamp)
            # if theres a P at that position, draw a Player
            if block_type == 'X':
                blocks.goto(position_x, position_y)
                blocks.stamp()
                # add block positions to walls list
                walls.append((position_x, position_y))
            # puts the player on the map
            if block_type == 'P':
                player.goto(position_x, position_y)
            # puts coins on the map
            if block_type == 'C':
                coins.append(Coin(position_x, position_y))
            if block_type == 'E':
                bad_guys.append(BadGuy(position_x, position_y))
            if block_type == 'O':
                exit_block.append(Exit(position_x, position_y))


# make an instance of each class
blocks = Blocks()
player = Player()

# keyboard commands
turtle.listen()

turtle.onkey(player.go_left, 'Left')
turtle.onkey(player.go_right, 'Right')
turtle.onkey(player.go_up, 'Up')
turtle.onkey(player.go_down, 'Down')

# #turn off screen updates
# #window.tracer(0)

# create the maze, position the player
on_level = 0
make_maze(levels[0])

# start the bad guys moving - otherwise they won't move at all
for bg in bad_guys:
    turtle.ontimer(bg.move, t=250)

# Loop keeps the game open and running
while True:
    # check for coin pickup
    for coin in coins:
        if player.is_collision(coin):
            # put the coin in the pocket
            player.gold += coin.gold
            print('Player Gold: {}'.format(player.gold))
            # remove picked up coin from the screen
            coin.pocket()
            # remove the coin from the coin list
            coins.remove(coin)
            # write score(gold) on screen
            # mypen.clear()
            # mypen.penup()
            # mypen.hideturtle()
            mypen.goto(300, -300)
            score = player.gold
            scorestring = score
            mypen.write(scorestring, False, align='left', font=('Arial', 14, 'normal'))
    for bg in bad_guys:
        if player.is_collision(bg):
            # put the coin in the pocket
            player.gold -= bg.gold
            print('Player Gold: {}'.format(player.gold))
            # write score(gold) on screen
            # mypen.clear()
            # mypen.penup()
            # mypen.hideturtle()
            mypen.goto(300, -300)
            score = player.gold
            scorestring = score
            mypen.write(scorestring, False, align='left', font=('Arial', 14, 'normal'))
    # check to see if player has reached level end, move to next level
    if player.is_collision(exit_block[0]):
        on_level += 1
        for bg in bad_guys:
            bg.die()
        bad_guys = []
        for coin in coins:
            coin.pocket()
        coins = []
        # exit location
        exit_block = []
        # wall locs
        walls = []
        blocks.clearstamps(n = None)
        make_maze(levels[on_level])
        for bg in bad_guys:
            turtle.ontimer(bg.move, t=250)
    else:
        pass


    # update screen
    window.update()