# Author: Philip Peiffer
# Date: 06/02/2021
# Description: This program is the GUI that allows for player input as part of playing KubaGame.

import pygame
import KubaGame


game = [KubaGame.KubaGame(("Player 1", "W"), ("Player 2", "B"))]

# Create the constants that will define the board
num_col = 7
num_row = 7
grid_size = 90

# define the board and screen size
board_width = num_col * grid_size
board_height = num_row * grid_size
window_width = 1080
window_height = 720

# define the board edges
left_edge = (window_width - board_width) / 2
right_edge = left_edge + board_width
top_edge = (window_height - board_height) / 2
bottom_edge = top_edge + board_height

# define the button locations
reset_button_location = ((right_edge + window_width)/2, bottom_edge - grid_size/2)
reset_button_left_edge = reset_button_location[0] - 30
reset_button_right_edge = reset_button_location[0] + 30
reset_button_top = reset_button_location[1] - 15
reset_button_bottom = reset_button_location[1] + 15

rules_button_location = (reset_button_location[0], reset_button_location[1] + 30)   # go 30 pixels below reset_button
rules_button_left_edge = rules_button_location[0] - 30
rules_button_right_edge = rules_button_location[0] + 30
rules_button_top = rules_button_location[1] - 15
rules_button_bottom = rules_button_location[1] + 15

# create the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (214, 51, 51)
grey = (176, 176, 176)
board_color = (245, 242, 215)

# initialize pygame
pygame.init()
# create a surface
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Kuba Game")


def reset():
    """Resets the game and starts a new round."""
    game[0] = KubaGame.KubaGame(("Player 1", "W"), ("Player 2", "B"))


def declare_winner():
    """Creates a message that declares the winner once a winner has been crowned."""
    winner = game[0].get_winner()
    if winner is not None:
        text = pygame.font.Font(None, 50)
        winning_text = text.render(str(winner) + " is the winner!", True, black, white)
        winning_text_rect = winning_text.get_rect()
        winning_text_rect.midtop = (window_width / 2, (window_height - board_height) / 2)
        screen.blit(winning_text, winning_text_rect)


def draw_player_turn():
    """Displays the player turn on the screen"""
    text = pygame.font.Font(None, 26)
    # render the player turn
    player_turn = game[0].get_current_turn()
    if player_turn is None:
        player_turn = "Either Player"
    player_turn_text = text.render("Player turn: " + str(player_turn), True, black)
    player_turn_rect = player_turn_text.get_rect()
    player_turn_rect.midtop = (int(window_width / 2), int(top_edge/2))
    screen.blit(player_turn_text, player_turn_rect)


def draw_buttons():
    """Displays the reset button on the screen."""
    text = pygame.font.Font(None, 26)

    # render the text
    new_game_text = text.render("NEW GAME", True, black)
    rules_text = text.render("RULES", True, black)

    # create a rectangle to house the text
    new_game_text_rect = new_game_text.get_rect()
    rules_text_rect = rules_text.get_rect()

    # position the rectangle on the screen
    new_game_text_rect.midtop = reset_button_location
    rules_text_rect.midtop = rules_button_location

    # blit the text onto the rectangle
    screen.blit(new_game_text, new_game_text_rect)
    screen.blit(rules_text, rules_text_rect)

def draw_player_one_scoreboard():
    """Creates a scoreboard on the screen that shows player marble count and # of marbles captured"""
    text = pygame.font.Font(None, 18)

    # render the player_one text
    player_one_text = []
    player_one_marble_count = game[0].get_marble_count()[0]
    player_one_captured = game[0].get_captured("Player 1")
    player_one_text.append(text.render("Player 1 Info", True, black))
    player_one_text.append(text.render("Marble Count: " + str(player_one_marble_count), True, black))
    player_one_text.append(text.render("Marbles Captured: " + str(player_one_captured), True, black))

    # create rectangles for player_one info
    player_one_rects = []
    for text_box in player_one_text:
        player_one_rects.append(text_box.get_rect())

    # position the rectangles on the board for player 1
    top_left_corner = (left_edge - 200, top_edge + grid_size/2)
    for rect in player_one_rects:
        rect.topleft = top_left_corner
        top_left_corner = (top_left_corner[0], top_left_corner[1] + 20)

    for index in range(len(player_one_text)):
        screen.blit(player_one_text[index], player_one_rects[index])


def draw_player_two_scoreboard():
    """Creates a scoreboard on the screen that shows player marble count and # of marbles captured"""
    text = pygame.font.Font(None, 18)

    # render the player_two text
    player_two_text = []
    player_two_marble_count = game[0].get_marble_count()[1]
    player_two_captured = game[0].get_captured("Player 2")
    player_two_text.append(text.render("Player 2 Info", True, black))
    player_two_text.append(text.render("Marble Count: " + str(player_two_marble_count), True, black))
    player_two_text.append(text.render("Marbles Captured: " + str(player_two_captured), True, black))

    # create rectangles for player_two info
    player_two_rects = []
    for text_box in player_two_text:
        player_two_rects.append(text_box.get_rect())

    # position the rectangles on the board for player 2
    top_left_corner = (right_edge + 50, top_edge + grid_size/2)
    for rect in player_two_rects:
        rect.topleft = top_left_corner
        top_left_corner = (top_left_corner[0], top_left_corner[1] + 20)

    for index in range(len(player_two_text)):
        screen.blit(player_two_text[index], player_two_rects[index])


def draw_marble(coords, color):
    """Draws a marble on the surface."""
    pygame.draw.circle(screen, color, (coords[0], coords[1]), grid_size / 2 - 10)


def load_images(coord, image_type):
    """Loads an image onto the screen in the specified coordinate."""
    # first create icon surfaces and transform their size to match the board grid
    if image_type == 'gor_image':
        icon = pygame.image.load('gorilla.png')
        icon = pygame.transform.scale(icon, (int(grid_size), int(grid_size)))
    if image_type == 'man_image':
        icon = pygame.image.load('man-in-suit-and-tie.png')
        icon = pygame.transform.scale(icon, (int(grid_size), int(grid_size)))
    if image_type == 'earth_image':
        icon = pygame.image.load('planet-earth.png')
        icon = pygame.transform.scale(icon, (int(grid_size), int(grid_size)))

    # blit the surfaces onto the screen surface at the coordinate specified. Note that we have to adjust the coordinates
    # because the icons position themselves based on the top left corner of the icon
    screen.blit(icon, (coord[0] - grid_size/2, coord[1] - grid_size/2))


def draw_border():
    horizontal_pos = top_edge + grid_size
    vertical_pos = left_edge + grid_size
    # drawing border and filling with board_color so board is different color than background
    border = pygame.Rect(left_edge, top_edge, (right_edge - left_edge), (bottom_edge - top_edge))
    pygame.draw.rect(screen, board_color, border)
    # drawing horizontal gridlines
    while horizontal_pos < bottom_edge:
        pygame.draw.line(screen, black, (left_edge, horizontal_pos), (right_edge, horizontal_pos), 2)
        horizontal_pos += grid_size
    # drawing vertical gridlines
    while vertical_pos < right_edge:
        pygame.draw.line(screen, black, (vertical_pos, top_edge), (vertical_pos, bottom_edge), 2)
        vertical_pos += grid_size


def get_marble_coords():
    """This function returns the marble coordinates in a tuple format (x, y) for each marble on the board. The
    coordinates are adjusted from the list index to a position on the screen by adding the edge of the
    board to index * grid_size + grid_size/2"""
    board = game[0]._board.get_current_board()
    white_marble_coords = []
    black_marble_coords = []
    red_marble_coords = []

    for row_index in range(len(board[0])):
        row_pos = top_edge + (grid_size / 2) + (grid_size * row_index)
        for col_index in range(len(board[0])):
            col_pos = left_edge + (grid_size / 2) + (grid_size * col_index)
            if game[0].get_marble((row_index, col_index)) == "W":
                white_marble_coords.append((col_pos, row_pos))
            if game[0].get_marble((row_index, col_index)) == "B":
                black_marble_coords.append((col_pos, row_pos))
            if game[0].get_marble((row_index, col_index)) == "R":
                red_marble_coords.append((col_pos, row_pos))
    return white_marble_coords, black_marble_coords, red_marble_coords


def draw_board():
    """Creates the board on the screen."""

    # fill the background with a color
    screen.fill(grey)

    # draw the border
    draw_border()

    # draw the scoreboards and buttons
    draw_player_one_scoreboard()
    draw_player_two_scoreboard()
    draw_player_turn()
    draw_buttons()

    # loop through the marble coordinates from the board and draw them on the screen
    marble_coords = get_marble_coords()
    white_marble_coords = marble_coords[0]
    black_marble_coords = marble_coords[1]
    red_marble_coords = marble_coords[2]

    for marble in white_marble_coords:
        load_images(marble, 'gor_image')

    for marble in black_marble_coords:
        load_images(marble, 'man_image')

    for marble in red_marble_coords:
        load_images(marble, 'earth_image')


def get_player_by_marble(marble_color):
    if marble_color == "W":
        return game[0].get_player_by_name("Player 1")
    else:
        return game[0].get_player_by_name("Player 2")


def get_marble_at_click(click_pos):
    """Returns the color of the marble at a position clicked on the screen. Will only return W or B marbles, as these
    are the only ones that can be played. Requires a positional coordinate on the screen as input (x-value, y-value)."""
    marble_screen_coords = get_marble_coords()
    # get the color of the marble that was clicked on
    for marble_group in marble_screen_coords:
        for marble in marble_group:
            # calculate the offset from the click to each marble. If the click was within the radius of a marble
            # position, then find out which marble group it was in to return the correct color
            click_offset = ((click_pos[0] - marble[0]) ** 2 + (click_pos[1] - marble[1]) ** 2) ** 0.5
            if click_offset <= grid_size / 2 - 10:
                if marble in marble_screen_coords[0]:
                    return "W", marble
                if marble in marble_screen_coords[1]:
                    return "B", marble
    # if we can't find a marble within the area clicked, then return None, None
    return None, None


def make_move(player, play_marble_screen_coord, direction):
    """This function takes an input of the player (from clicking on the screen), the coordinates that they're trying
    to play at (from clicking on the screen), and the direction (from keyboard arrows). The coordinates are coordinates
    from the screen, so they are converted to regular list indices in order to use the make_move function from the
    KubaGame.py file."""
    # need to convert the screen coordinates to the board coordinates of the game
    col_index = int((play_marble_screen_coord[0] - (left_edge + grid_size/2)) / grid_size)
    row_index = int((play_marble_screen_coord[1] - (top_edge + grid_size/2)) / grid_size)
    play_marble_board_coord = (row_index, col_index)

    game[0].make_move(player.get_player_name(), play_marble_board_coord, direction)


# start the pygame loop
running = True
play_needs = [None, None, None]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if the player clicks on the screen, compare the location of the click to interactive objects
        if event.type == pygame.MOUSEBUTTONDOWN:

            # if the player clicks the reset button, run the reset function so new game starts
            if (reset_button_left_edge < event.pos[0] < reset_button_right_edge and
                    reset_button_top < event.pos[1] < reset_button_bottom):
                reset()

            # if they click a marble, get the location and color to run the make_move function
            marble_color = get_marble_at_click(event.pos)[0]
            marble_location = get_marble_at_click(event.pos)[1]
            play_needs[0] = marble_location
            play_needs[1] = marble_color

        # look for a direction input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = "L"
                play_needs[2] = direction
            if event.key == pygame.K_RIGHT:
                direction = "R"
                play_needs[2] = direction
            if event.key == pygame.K_UP:
                direction = "F"
                play_needs[2] = direction
            if event.key == pygame.K_DOWN:
                direction = "B"
                play_needs[2] = direction


    # draw the board
    draw_board()

    # check for a move command
    # enforce that a click goes first
    if not play_needs[0]:
        play_needs = [None, None, None]
    if None not in play_needs:
        make_move(get_player_by_marble(play_needs[1]), play_needs[0], play_needs[2])
        play_needs = [None, None, None]
    declare_winner()
    pygame.display.update()
