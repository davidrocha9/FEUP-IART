import pygame
from pygame import gfxdraw
import pygame_menu
import time
from neutreeko.constants import *
from neutreeko.game import Game
from minimax.algorithm import AI
import time
import random
from bots.botmethods import *
from collections import Counter

FPS = 60

# Core Variables used for game handling
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')
END_FONT = pygame.font.Font('freesansbold.ttf', 32)
hintFont = pygame.font.Font('freesansbold.ttf', 10)
talkFont = pygame.font.Font('freesansbold.ttf', 15)
nameFont = pygame.font.Font('freesansbold.ttf', 25)
global global_mode, global_heuristic, global_method, global_pc1, global_pc2, global_name1, global_name2, global_method1, global_method2
global_mode = "pvp"
global_heuristic = 2
global_evaluation = 1
global_method = 1
global_pc1 = 1
global_pc2 = 1
global_name1 = ['Default1',1]
global_name2 = ['Default2',1]
global_method1 = 1
global_method2 = 1
againstPc = False

# List with bot line speech
xqcLines = ["Hikaru taught me this is the best move!", "BING!", "BANG!", "Chat, CHAT! I totally planned that.", "DUDE DUDE DUDE DUDE DUDE", "Jam a man of Fortune...", "Cheeto!", "...and J must seek my fortune!"]
botezLines = ["Let the games begin!", "I wonder if there is a London for Neutreeko...", "I guess that is playable.", "I was already expecting that.", "Bang. You're making it too easy.", "*changes Spotify playlist*"]
hikaruLines = ["This is all theory.", "*looks at ceiling and scratches head*", "Takes, takes and takes... I think this is winning.", "Is this a move? Probably. Let's play it.", "Let's keep going.", "Chat, this has to be winning!", "I'll just play my juicer here.", "If takes I just take, and then I must be winning.", "I go here, here, here and here and I win."]

# Calculates x and y based on mouse input position
def get_row_col_from_mouse(pos):
    x, y = pos
    x -= 175
    y -= 220
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Draws Hint Panel
def drawHintBoard(game, againstPc):
    lamp = pygame.image.load(r'.\assets\lamp.png')
    counter1 = nameFont.render("Counter: " + str(game.p1HintCounter), 1, (0, 0, 0))
    if againstPc is False:
        counter2 = nameFont.render("Counter: " + str(game.p2HintCounter), 1, (0, 0, 0))
    press = talkFont.render("Press H", 1, (0, 0, 0))
    press1 = talkFont.render("for a Hint!", 1, (0, 0, 0))
    pygame.draw.rect(WIN, CARDCOLOR, (15, 275, 150, 335), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    WIN.blit(counter1, (25, 530))
    if againstPc is False:
        WIN.blit(counter2, (25, 330))
    WIN.blit(press, (65, 465))
    WIN.blit(press1, (55, 480))
    WIN.blit(lamp, (20, 375))

# Displays ending message
def display_message(WIN, winner):
    rect = pygame.draw.rect(WIN, CARDCOLOR, (150, 250, 500, 300), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    if winner == "1":
        #pygame.draw.rect(WIN, (1,99,110,255), (150, 250, 500, 300))
        end_text = END_FONT.render(str(global_name1[0]) + " won!", 1, BLACK)
        WIN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
        pygame.display.update()
        global_name1[0] = "Default1"
        global_name2[0] = "Default2"
        time.sleep(3)

    elif winner == "2":
        #pygame.draw.rect(WIN, (1,99,110,255), (150, 250, 500, 300))
        end_text = END_FONT.render(str(global_name2[0]) + " won!", 1, BLACK)
        WIN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
        pygame.display.update()
        global_name1[0] = "Default1"
        global_name2[0] = "Default2"
        time.sleep(3)

    elif winner == "0":
        pygame.draw.rect(WIN, (1,99,110,255), (150, 250, 500, 300))
        end_text = END_FONT.render("It was a Draw!", 1, BLACK)
        WIN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
        pygame.display.update()
        time.sleep(3)

# Draws evaluation bars
def drawBars(WIN):
    pygame.draw.rect(WIN, WHITE, (680, 220, 25, 225)) #Barra branca
    pygame.draw.rect(WIN, BLUE, (680, 445, 25, 225)) #Barra preta

# Draws bot cards
def drawCards(WIN):
    #WIN.fill(PURPLE)
    pygame.draw.rect(WIN, CARDCOLOR, (150, 90, 500, 100), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.draw.rect(WIN, WHITE, (680, 220, 25, 225)) #Barra branca
    pygame.draw.rect(WIN, BLUE, (680, 445, 25, 225)) #Barra preta

# Updates evaluation bars
def updateBars(WIN, p1, p2):
    total = p1 + p2
    if total > 0:
        p1Percentage = float(p1/total)
        p2Percentage = float(p2/total)
        pygame.draw.rect(WIN, WHITE, (680, 220, 25, p2Percentage * 450)) #Barra branca
        pygame.draw.rect(WIN, BLUE, (680, 220 + p2Percentage * 450, 25, p1Percentage * 450)) #Barra preta

# Prints bot stats after making a move
def print_stats(time, moves):
    pygame.draw.rect(WIN, BLUE, (150, 185, 500, 30))
    end_text = nameFont.render("AI speed: " + str(time) + "s " + "Nodes traced: " + str(moves), 1, BLACK)
    WIN.blit(end_text, ( 160, 190))

def print_stats_down(time, moves):
    pygame.draw.rect(WIN, BLUE, (150, 675, 500, 30))
    end_text = nameFont.render("AI speed: " + str(time) + "s " + "Nodes traced: " + str(moves), 1, BLACK)
    WIN.blit(end_text, ( 160, 680))

#Draws bot's name
def drawName(WIN, diff):
    if diff == 2:
        name = END_FONT.render("XQC - Famous Twitch Streamer", True, (0,0,0))
        WIN.blit(name, (150, 30))
    elif diff == 4:
        name = END_FONT.render("Andrea Botez - Chess Streamer", True, (0,0,0))
        WIN.blit(name, (155, 30))
    elif diff == 5:
        name = END_FONT.render("Hikaru Nakamura - Chess Grandmaster", True, (0,0,0))
        WIN.blit(name, (100, 30))

# Draws welcoming message from bots
def drawWelcome(WIN, diff):
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    if diff == 2:
        hint = talkFont.render("BING. BANG. BOOM. Let’s do this!", True, (0,0,0))
    elif diff == 4:
        hint = talkFont.render("I have time before my stream... good luck :)", True, (0,0,0))
    elif diff == 5:
        hint = talkFont.render("Let's see what you have prepared for me.", True, (0,0,0))
    WIN.blit(hint, (175, 130))

# Draws a random bot's line after making a move
def drawLine(WIN, diff):
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    if diff == 2:
        x = random.randint(0,len(xqcLines)-1)
        speach = talkFont.render(xqcLines[x], True, (0,0,0))
    elif diff == 4:
        x = random.randint(0,len(botezLines)-1)
        speach = talkFont.render(botezLines[x], True, (0,0,0))
    elif diff == 5:
        x = random.randint(0,len(hikaruLines)-1)
        speach = talkFont.render(hikaruLines[x], True, (0,0,0))
    WIN.blit(speach, (175, 130))

# Draws bot's line after a game ends
def drawEnding(player, diff, WIN):
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    if diff == 2:
        if player == 2:
            hint = talkFont.render("GG EZ CLAP GET REKT", True, (0,0,0))
        else:
            hint = talkFont.render("NOOOOO! GO AGANE *slams desk*", True, (0,0,0))
    elif diff == 4:
        if player == 2:
            hint = talkFont.render("I kinda wished this would be over sooner.", True, (0,0,0))
        else:
            hint = talkFont.render("That loss was chat's fault.", True, (0,0,0))
    elif diff == 5:
        if player == 2:
            hint = talkFont.render("Good, but not good enough for Magnus.", True, (0,0,0))
        else:
            hint = talkFont.render("How did I not see that? I'm so bad.", True, (0,0,0))
    WIN.blit(hint, (175, 130))

