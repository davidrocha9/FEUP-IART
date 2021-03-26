import pygame
from pygame import gfxdraw
import pygame_menu
import time
from neutreeko.constants import *
from neutreeko.game import Game
from minimax.algorithm import AI
import time
import random
from bots.easy import *

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')
END_FONT = pygame.font.Font('freesansbold.ttf', 32)
talkFont = pygame.font.Font('freesansbold.ttf', 15)
global global_mode, global_heuristic, global_method, global_pc1, global_pc2
global_mode = "pvp"
global_heuristic = 2
global_method = 1
global_pc1 = 1
global_pc2 = 1

xqcLines = ["Hikaru taught me this is the best move!", "BING!", "BANG!", "Chat, CHAT! I totally planned that.", "DUDE DUDE DUDE DUDE DUDE", "Jam a man of Fortune...", "Cheeto!", "...and J must seek my fortune!"]
botezLines = ["Let the games begin!"]
hikaruLines = ["This is all theory.", "*looks at ceiling and scratches head*", "Takes, takes and takes... I think this is winning.", "Is this a move? Probably. Let's play it.", "Let's keep going.", "Chat, this has to be winning!", "I'll just play my juicer here.", "If takes I just take, and then I must be winning.", "I go here, here, here and here and I win."]

def get_row_col_from_mouse(pos):
    x, y = pos
    x -= 175
    y -= 220
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_message(WIN, winner):
    pygame.draw.rect(WIN, (1,99,110,255), (150, 250, 500, 300))
    end_text = END_FONT.render("Player " + winner + " won!", 1, BLACK)
    WIN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    time.sleep(3)

def drawCards(WIN):
    #WIN.fill(PURPLE)
    pygame.draw.rect(WIN, CARDCOLOR, (150, 90, 500, 100), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.draw.rect(WIN, WHITE, (680, 220, 25, 225)) #Barra branca
    pygame.draw.rect(WIN, BLUE, (680, 445, 25, 225)) #Barra preta

def updateBars(WIN, p1, p2):
    total = p1 + p2
    p1Percentage = float(p1/total)
    p2Percentage = float(p2/total)
    pygame.draw.rect(WIN, WHITE, (680, 220, 25, p2Percentage * 450)) #Barra branca
    pygame.draw.rect(WIN, BLUE, (680, 220 + p2Percentage * 450, 25, p1Percentage * 450)) #Barra preta

def drawName(WIN, diff):
    if diff == 2:
        name = END_FONT.render("XQC - Famous Twitch Streamer", True, (0,0,0))
        WIN.blit(name, (150, 30))
    elif diff == 4:
        name = END_FONT.render("Andrea Botez - Chess Streamer", True, (0,0,0))
        WIN.blit(name, (155, 30))
    elif diff == 6:
        name = END_FONT.render("Hikaru Nakamura - Chess Grandmaster", True, (0,0,0))
        WIN.blit(name, (100, 30))

def drawWelcome(WIN, diff):
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    print(diff)
    if diff == 2:
        hint = talkFont.render("BING. BANG. BOOM. Let’s do this!", True, (0,0,0))
    elif diff == 4:
        hint = talkFont.render("I have some time before my stream... good luck :)", True, (0,0,0))
    elif diff == 6:
        hint = talkFont.render("Let's see what you have prepared for me.", True, (0,0,0))
    WIN.blit(hint, (175, 130))

def drawLine(WIN, diff):
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    if (diff == 1):
        x = random.randint(0,len(xqcLines)-1)
        hint = talkFont.render(xqcLines[x], True, (0,0,0))
    WIN.blit(hint, (175, 130))

def drawEnding(player, diff, WIN):
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    if diff == 2:
        if player == 2:
            hint = talkFont.render("GG EZ CLAP GET REKT", True, (0,0,0))
        else:
            hint = talkFont.render("NOOOOOOOOOOO! GO AGANE *slams desk*", True, (0,0,0))
    elif diff == 4:
        if player == 2:
            hint = talkFont.render("That was a fun game!", True, (0,0,0))
        else:
            hint = talkFont.render("That loss was chat's fault.", True, (0,0,0))
    else:
        if player == 2:
            hint = talkFont.render("That was good, but not good enough for Magnus.", True, (0,0,0))
        else:
            hint = talkFont.render("How did I not see that? I'm so bad.", True, (0,0,0))
    WIN.blit(hint, (175, 130))

    