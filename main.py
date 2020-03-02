import pygame
from tkinter import *


class Grid:

    def __init__(self):
        self.board = [[0] * 3 for i in range(3)]
        self.win_combinations = [[(0, 0), (0, 1), (0, 2)],
                                 [(1, 0), (1, 1), (1, 2)],
                                 [(2, 0), (2, 1), (2, 2)],
                                 [(0, 0), (1, 0), (2, 0)],
                                 [(0, 1), (1, 1), (2, 1)],
                                 [(0, 2), (1, 2), (2, 2)],
                                 [(0, 0), (1, 1), (2, 2)],
                                 [(2, 0), (1, 1), (0, 2)],
                                 ]

    def check_click(self, x, y):
        if self.board[x][y] != 0:
            return False
        return True

    def choose(self, x, y, player):
        if player.name == "cross":
            self.board[x][y] = 1
        else:
            self.board[x][y] = 2
        draw_window()

    def win_check(self):
        for i in self.win_combinations:
            if self.board[i[0][0]][i[0][1]] == self.board[i[1][0]][i[1][1]] == self.board[i[2][0]][i[2][1]] != 0:
                return True
        return False

    def is_full(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        return True

    def restart(self):
        self.board = [[0] * 3 for i in range(3)]


class Player:
    def __init__(self, name, char, info, win):
        self.name = name
        self.char = char
        self.wins = 0
        self.info = info
        self.win = win


class Option:

    def __init__(self, x_cor, y_cor, width, height, text=""):
        self.x = x_cor
        self.y = y_cor
        self.w = width
        self.h = height
        self.t = text

    def draw(self):
        pygame.draw.rect(window, (255, 255, 255), (self.x - 2, self.y - 2, self.w, self.h), 2)
        if self.t != "":
            text = font_bold.render(self.t, 1, (255, 255, 255))
            window.blit(text, (self.x + (self.w / 2 - text.get_width() / 2),
                               self.y + (self.h / 2 - text.get_height() / 2)))


pygame.init()
screen_x = 720
screen_y = 480
window = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Tic-Tac-Toe")
cross_image = pygame.image.load("cross.png")
circle_image = pygame.image.load("circle.png")
font = pygame.font.SysFont("calibri", 28)
font_bold = pygame.font.SysFont("calibri", 24, True)
font_2 = pygame.font.SysFont("calibri", 48, True)
restart_button = Option(400, 350, 100, 50, "Restart")
new_game_button = Option(520, 350, 150, 50, "New Game")
result_label = font_bold.render("CROSS   :   CIRCLE", 1, (255, 255, 255))
continue_label = font.render("Click anywhere to continue", True, (255, 255, 255))
game = Grid()


def draw_window():
    window.fill((0, 0, 0))
    pygame.draw.line(window, (255, 255, 255), (150, 50), (150, 350), 6)
    pygame.draw.line(window, (255, 255, 255), (250, 50), (250, 350), 6)
    pygame.draw.line(window, (255, 255, 255), (50, 150), (350, 150), 6)
    pygame.draw.line(window, (255, 255, 255), (50, 250), (350, 250), 6)
    restart_button.draw()
    new_game_button.draw()
    window.blit(result_label, ((350 + (screen_x - 350 - result_label.get_width()) / 2), 50))
    window.blit((font_2.render(str(cross.wins), 1, (255, 255, 255))), (475, 90))
    window.blit((font_2.render(str(circle.wins), 1, (255, 255, 255))), (575, 90))
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            if game.board[i][j] == 1:
                window.blit(cross_image, (50 + 100 * i, 50 + 100 * j))
            elif game.board[i][j] == 2:
                window.blit(circle_image, (50 + 100 * i, 50 + 100 * j))
    pygame.display.update()


def intro():
    x = 0

    def go():
        nonlocal x
        x = int(number.get())
        tk.destroy()
        return x

    tk = Tk()
    tk.geometry("350x200")
    tk.title("TIC-TAC-TOE")
    var1 = IntVar()

    welcome = Label(tk, text="Welcome to TIC-TAC-TOE!", font=("Calibri", 14))
    welcome.pack(pady=25)

    choose_frame = Frame(tk)
    quantity = Label(choose_frame, text="Choose number of games to win the match:")
    quantity.grid(row=0, column=1, padx=5)
    number = Spinbox(choose_frame, from_=1, to=20, width=3)
    number.grid(row=0, column=2, padx=5)
    choose_frame.pack(pady=5)

    button_frame = Frame(tk)
    ok_button = Button(button_frame, text="OK", command=go)
    ok_button.grid(row=3, column=0, padx=20)
    cancel_button = Button(button_frame, text="Cancel", command=tk.destroy)
    cancel_button.grid(row=3, column=3, padx=20)
    button_frame.pack(pady=15)

    tk.mainloop()
    return x


def outro(player):
    label = font_2.render(player.win, 1, (255, 255, 255))
    window.blit(label, ((350 + (screen_x - 350 - label.get_width()) / 2), 270))
    pygame.display.update()
    click_to_continue()
    main()


def click_to_continue():
    global run
    wait = True
    window.blit(continue_label, (40, 400))
    pygame.display.update()
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                wait = False
            if event.type == pygame.MOUSEBUTTONUP:
                wait = False


def main():

    def play(starting, turn):
        global run
        end = False
        block = True
        while run:
            info = font.render(turn.info, 1, (255, 255, 255))
            window.blit(info, ((350 + (screen_x - 350 - info.get_width()) / 2), 170))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    if restart_button.x <= pos[0] <= restart_button.x + restart_button.w and \
                            restart_button.y <= pos[1] <= restart_button.y + restart_button.h:
                        game.board = [[0] * 3 for i in range(3)]
                        draw_window()
                        play(starting, starting)

                    if new_game_button.x <= pos[0] <= new_game_button.x + new_game_button.w and \
                            new_game_button.y <= pos[1] <= new_game_button.y + new_game_button.h:
                        main()

                    if 50 <= pos[0] < 350 and 50 <= pos[1] < 350:
                        x = (pos[0] - 50) // 100
                        y = (pos[1] - 50) // 100
                        if game.check_click(x, y):
                            game.choose(x, y, turn)
                            draw_window()
                            if not game.win_check():
                                if game.is_full():
                                    game.restart()
                                    click_to_continue()
                                    draw_window()
                            else:
                                turn.wins += 1
                                game.restart()
                                if turn.wins == games:
                                    outro(turn)
                                else:
                                    click_to_continue()
                                    draw_window()
                                    if starting == cross:
                                        play(circle, circle)
                                    else:
                                        play(cross, cross)

                            if turn == cross:
                                play(starting, circle)
                            else:
                                play(starting, cross)

    global games, run, cross, circle
    window.fill((0, 0, 0))
    pygame.display.update()
    run = False
    games = intro()
    cross = Player("cross", cross_image, "Cross' turn", "Cross wins!!!")
    circle = Player("circle", circle_image, "Circle's turn", "Circle wins!!!")
    if games > 0:
        run = True
        draw_window()
        play(cross, cross)
    pygame.quit()


main()
