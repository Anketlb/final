import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions and colors
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Enter Your Name")
font = pygame.font.Font(None, 48)  # Default font with size 48
text_color = (255, 255, 255)  # White
background_color = (0, 0, 0)  # Black

# Input variables
input_text = ""
active = True  # Whether the input field is active

# Game loop
while active:
    screen.fill(background_color)  # Clear the screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if END_BACK.checkForInput(END_MOUSE_POS):
        #         main_menu()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f'{input_text}: {int(score)}')
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    input_surface = font.render(input_text, True, 'white')
    input_rect = input_surface.get_rect(center=(600, 430))
    screen.blit(input_surface, input_rect)

    # Update the display
    pygame.display.update()

# Continue with your game logic or close the app
pygame.quit()
