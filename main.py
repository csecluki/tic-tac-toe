import pygame
from tkinter import *
import minimax

pygame.init()
pygame.display.set_caption("Tic-Tac-Toe")

SCREEN_X = 720
SCREEN_Y = 480
CROSS_IMAGE = pygame.image.load("graphics/cross.png")
CIRCLE_IMAGE = pygame.image.load("graphics/circle.png")
FONT_NORMAL = pygame.font.SysFont("helvetica", 28)
FONT_BOLD = pygame.font.SysFont("helvetica", 24, True)
FONT_BOLD_BIGGER = pygame.font.SysFont("helvetica", 48, True)
RESULT_LABEL = FONT_BOLD.render("CROSS   :   CIRCLE", 1, (255, 255, 255))
CONTINUE_LABEL = FONT_BOLD.render("Click anywhere to continue", 1, (255, 255, 255))


class Window:

    def __init__(self):

        self.frame = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
        self.restart_button = Option(400, 350, 100, 50, "Restart")
        self.new_game_button = Option(520, 350, 150, 50, "New Game")

        self.start_new_game()

    def start_new_game(self):
        self.board = Board()
        self.cross = Player("cross", CROSS_IMAGE, "Cross' turn", "Cross wins!!!")
        self.circle = Player("circle", CIRCLE_IMAGE, "Circle's turn", "Circle wins!!!")

        self.starting_player = self.cross
        self.current_turn = self.cross

        self.win_limit, self.ai_player = intro()

        if self.win_limit is not None:
            self.play()
        else:
            quit()

    def draw(self):
        self.frame.fill((0, 0, 0))
        self.board.draw(self.frame)
        self.restart_button.draw(self.frame)
        self.new_game_button.draw(self.frame)
        self.frame.blit(RESULT_LABEL, ((350 + (SCREEN_X - 350 - RESULT_LABEL.get_width()) / 2), 50))
        self.frame.blit((FONT_BOLD_BIGGER.render(str(self.cross.games_won), 1, (255, 255, 255))), (455, 90))
        self.frame.blit((FONT_BOLD_BIGGER.render(str(self.circle.games_won), 1, (255, 255, 255))), (585, 90))
        pygame.display.update()

    def play(self):
        self.draw()
        while True:
            turn_info = FONT_NORMAL.render(self.current_turn.turn_info, 1, (255, 255, 255))
            self.frame.blit(turn_info, ((350 + (SCREEN_X - 350 - turn_info.get_width()) / 2), 190))
            pygame.display.update()

            if self.ai_player and self.current_turn == self.circle:
                x, y = minimax.bestscore(self.board.grid)
                self.board.handle_move(x, y, self.current_turn)
                self.draw()
                move_result = self.board.give_result_of_game()
                if move_result == "continue":
                    self.change_player()
                elif move_result == "win":
                    self.current_turn.games_won += 1
                    self.draw()
                    if self.current_turn.games_won == self.win_limit:
                        self.outro()
                        self.click_to_continue()
                        self.start_new_game()
                    self.click_to_continue()
                    self.next_game()
                elif move_result == "draw":
                    self.click_to_continue()
                    self.next_game()

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                    if event.type == pygame.MOUSEBUTTONUP:
                        pos_x, pos_y = pygame.mouse.get_pos()

                        if self.restart_button.x <= pos_x <= self.restart_button.x + self.restart_button.w and \
                                self.restart_button.y <= pos_y <= self.restart_button.y + self.restart_button.h:
                            self.board.restart()
                            self.current_turn = self.starting_player
                            self.draw()
                            continue

                        if self.new_game_button.x <= pos_x <= self.new_game_button.x2 and \
                                self.new_game_button.y <= pos_y <= self.new_game_button.y2:
                            self.start_new_game()

                        if 50 <= pos_x < 350 and 50 <= pos_y < 350:
                            # changing click coordinates to position on board
                            x = (pos_x - 50) // 100
                            y = (pos_y - 50) // 100

                            self.board.handle_move(x, y, self.current_turn)
                            self.draw()
                            move_result = self.board.give_result_of_game()
                            if move_result == "continue":
                                self.change_player()
                            elif move_result == "win":
                                self.current_turn.games_won += 1
                                self.draw()
                                if self.current_turn.games_won == self.win_limit:
                                    self.outro()
                                    self.click_to_continue()
                                    self.start_new_game()
                                self.click_to_continue()
                                self.next_game()
                            elif move_result == "draw":
                                self.click_to_continue()
                                self.next_game()

    def change_player(self):
        if self.current_turn == self.cross:
            self.current_turn = self.circle
        else:
            self.current_turn = self.cross

    def next_game(self):
        self.board.restart()
        if self.starting_player == self.cross:
            self.starting_player = self.circle
            self.current_turn = self.circle
        else:
            self.starting_player = self.cross
            self.current_turn = self.cross
        self.draw()

    def click_to_continue(self):
        self.frame.blit(CONTINUE_LABEL, (40, 400))
        pygame.display.update()
        stop = True
        while stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    stop = False

    def outro(self):
        label = FONT_BOLD_BIGGER.render(self.current_turn.win_info, 1, (255, 255, 255))
        self.frame.blit(label, ((350 + (SCREEN_X - 350 - label.get_width()) / 2), 270))
        pygame.display.update()


def intro():
    ai = None
    limit = None

    def return_values():
        nonlocal ai, limit
        ai = ai_player.get()
        limit = int(number.get())
        tk.destroy()

    tk = Tk()
    tk.geometry("350x200")
    tk.title("TIC-TAC-TOE")

    ai_player = IntVar()

    welcome = Label(tk, text="Welcome to TIC-TAC-TOE!", font=("Calibri", 14))
    welcome.pack(pady=25)

    choose_frame = Frame(tk)

    quantity = Label(choose_frame, text="Choose number of games to win the match:")
    quantity.grid(row=0, column=1, padx=5)

    number = Spinbox(choose_frame, from_=1, to=20, width=3)
    number.grid(row=0, column=2, padx=5)

    is_ai = Checkbutton(choose_frame, text="Second player as AI", variable=ai_player, onvalue=1, offvalue=0)
    is_ai.grid(row=1, column=1, padx=5)

    choose_frame.pack(pady=5)

    button_frame = Frame(tk)

    ok_button = Button(button_frame, text="OK", command=return_values)
    ok_button.grid(row=3, column=0, padx=20)

    cancel_button = Button(button_frame, text="Cancel", command=quit)
    cancel_button.grid(row=3, column=3, padx=20)

    button_frame.pack(pady=15)

    tk.mainloop()

    return limit, ai


class Board:

    def __init__(self):
        self.grid = [[0] * 3 for i in range(3)]

        self.win_combinations = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)],
        ]

        self.lines = (
            ((255, 255, 255), (150, 50), (150, 350), 6),
            ((255, 255, 255), (250, 50), (250, 350), 6),
            ((255, 255, 255), (50, 150), (350, 150), 6),
            ((255, 255, 255), (50, 250), (350, 250), 6)
        )

    def draw(self, frame):
        for line in self.lines:
            pygame.draw.line(frame, *line)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    frame.blit(CROSS_IMAGE, (50 + 100 * i, 50 + 100 * j))
                elif self.grid[i][j] == 2:
                    frame.blit(CIRCLE_IMAGE, (50 + 100 * i, 50 + 100 * j))

    def handle_move(self, x, y, player):
        if self.check_click(x, y):
            self.choose(x, y, player)

    def check_click(self, x, y):
        if self.grid[x][y] != 0:
            return False
        return True

    def choose(self, x, y, player):
        if player.name == "cross":
            self.grid[x][y] = 1
        else:
            self.grid[x][y] = 2

    def give_result_of_game(self, name=False):
        # current player won
        for i in self.win_combinations:
            if self.grid[i[0][0]][i[0][1]] == self.grid[i[1][0]][i[1][1]] == self.grid[i[2][0]][i[2][1]] != 0:
                if name:
                    if self.grid[i[0][0]][i[0][1]] == 1:
                        return "cross"
                    else:
                        return "circle"
                return "win"

        # there is at least one empty field on board - game continues
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    return "continue"
        # draw
        return "draw"

    def restart(self):
        self.grid = [[0] * 3 for i in range(3)]

    def undo_move(self, x, y):
        self.grid[x][y] = 0

    def bestscore(self, players):
        optimal = -100
        x = 0
        y = 0
        for i in range(3):
            for j in range(3):
                if self.check_click(i, j):
                    print(i, j)
                    self.choose(i, j, players[1])
                    score = self.minmax(0, False, players)
                    self.undo_move(i, j)
                    if score > optimal:
                        optimal = score
                        x = i
                        y = j
        return x, y

    def minmax(self, depth, ismax, players):
        result = self.give_result_of_game(name=True)
        print(result)
        if result == "cross":
            return -1
        if result == "circle":
            return 1
        if result == "draw":
            return 0
        if result == "continue":
            if ismax:
                optimal = -100
                for i in range(3):
                    for j in range(3):
                        if self.check_click(i, j):
                            self.choose(i, j, players[1])
                            score = self.minmax(0, False, players)
                            self.undo_move(i, j)
                            optimal = max(score, optimal)
                return optimal
            else:
                optimal = 100
                for i in range(3):
                    for j in range(3):
                        self.handle_move(i, j, players[0])
                        score = self.minmax(0, False, players)
                        self.undo_move(i, j)
                        optimal = min(score, optimal)
                return optimal


class Player:

    def __init__(self, name, image, turn_info, win_info):
        self.name = name
        self.image = image
        self.games_won = 0
        self.turn_info = turn_info
        self.win_info = win_info


class Option:

    def __init__(self, x_cor, y_cor, width, height, text=""):
        self.x = x_cor
        self.x2 = x_cor + width
        self.y = y_cor
        self.y2 = y_cor + height
        self.w = width
        self.h = height
        self.t = text

    def draw(self, frame):
        pygame.draw.rect(frame, (255, 255, 255), (self.x - 2, self.y - 2, self.w, self.h), 2)
        if self.t != "":
            text = FONT_BOLD.render(self.t, 1, (255, 255, 255))
            frame.blit(text, (self.x + (self.w / 2 - text.get_width() / 2),
                              self.y + (self.h / 2 - text.get_height() / 2)))
