import pygame
import nltk
import random

pygame.init()


nltk.download('words')
from nltk.corpus import words


word_list = words.words()


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)
pink = (249, 77, 168)
blue = (58, 250, 229)

WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Wordle Knockoff')
turn = 0
board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

fps = 60
timer = pygame.time.Clock()
huge_font = pygame.font.Font('freesansbold.ttf', 56)
six_letter_words = [word for word in word_list if len(word) == 5]
secret_word = random.choice(six_letter_words)
# secret_word = random.choice(word_list)
game_over = False
letters = 0
turn_active = True



def draw_board():
    global turn
    global board
    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(screen, white, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 20)
            piece_text = huge_font.render(board[row][col], True, gray)
            screen.blit(piece_text, (col * 100 + 30, row * 100 + 25))
    pygame.draw.rect(screen, pink, [5, turn * 100 + 5, WIDTH - 10, 90], 3, 20)



def check_words():
    global turn
    global board
    global secret_word
    for col in range(0, 5):
        for row in range(0, 6):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(screen, green, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 20)
            elif board[row][col] in secret_word and turn > row:
                pygame.draw.rect(screen, yellow, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 20)



running = True
while running:
    timer.tick(fps)
    screen.fill(black)
    check_words()
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            entry = event.text.lower()
            if entry != " ":
                if letters < 5:
                    board[turn][letters] = entry
                    letters += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letters > 0:
                board[turn][letters - 1] = ' '
                letters -= 1
            if event.key == pygame.K_RETURN and not game_over:
                turn += 1
                letters = 0
            if event.key == pygame.K_RETURN and game_over:
                turn = 0
                letters = 0
                game_over = False
                secret_word = random.choice(word_list)
                board = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]

    if letters == 5:
        turn_active = False
    if letters < 5:
        turn_active = True

    for row in range(0, 6):
        guess = ''.join(board[row])
        if guess == secret_word and row < turn:
            game_over = True

    if turn == 6:
        game_over = True
    if game_over:
        if turn < 6:
            loser_text = pygame.font.Font('freesansbold.ttf', 36).render('Winner!', True, blue)
            loser_text_rect = loser_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(loser_text, loser_text_rect)
        else:
            correct_word_text = pygame.font.Font('freesansbold.ttf', 36).render('Correct Word: ' + secret_word, True, pink)
            correct_word_text_rect = correct_word_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(correct_word_text, correct_word_text_rect)

    pygame.display.flip()

pygame.quit()
