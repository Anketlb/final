import pygame, sys
from os.path import join
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
import json

class Game:
    def __init__(self):
        #player_setup
        player_sprite = Player((screen_width / 2 ,screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #Health and score
        self.lives = 3
        self.live_surf = pygame.image.load(join('images', 'player', 'player.png')).convert_alpha()
        self.live_surf = pygame.transform.scale_by(self.live_surf, 0.6)
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font(join('font', 'Pixeled.ttf'), 20)

        #obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width/ self.obstacle_amount)for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start= screen_width / 15, y_start= 470)

        #alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        #extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40,80)

        #audio
        music = pygame.mixer.Sound(join('audio', 'music.wav'))
        music.set_volume(0.1)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
        self.laser_sound.set_volume(0.1)
        self.explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
        self.explosion_sound.set_volume(0.1)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start,offset_x,)

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset= 70, y_offset= 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    # alien_sprite = Alien('yellow',x,y)
                    alien_sprite = Alien('Sparchu', x, y)
                elif 1 <= row_index <= 2:
                    # alien_sprite = Alien('green',x,y)
                    alien_sprite = Alien('Finsta', x, y)
                else:
                    # alien_sprite = Alien('red',x,y)
                    alien_sprite = Alien('Larvea', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)
            elif alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']),screen_width))
            self.extra_spawn_time = randint(400, 800)

    def collision_checks(self):
        #player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()
                #extra collisions
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()


        #alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # player collisions
                if pygame.sprite.spritecollide(laser, self.player, False, pygame.sprite.collide_mask):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        with open(join('data', 'score.txt'), 'a+') as saved_scores:
                            json.dump(self.score, saved_scores)
                        pygame.quit()
                        sys.exit()
        # alien collide
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, True):
                    #change this to go to another screen
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x,8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You Won!', False, 'White')
            victory_rect = victory_surf.get_rect(center = (screen_width/2, screen_height/2))
            screen.blit(victory_surf,victory_rect)

    def arcade_score(self):
        pass


    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()
        self.extra.update()

        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load(join('images', 'extra', 'tv.png')).convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))


    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(85,100))
        self.create_crt_lines()
        screen.blit(self.tv, (0,0))

import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        # screen.fill((30,30,30))
        bg_surf = 'images/extra/bg.png'
        bg = pygame.image.load(bg_surf).convert_alpha()
        screen.blit(bg, (0,0))
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)
