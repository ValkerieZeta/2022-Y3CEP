import pygame
from pygame.locals import *
import random


# Helpers
#todo: add game music and death music and restart button and intro interface

def once(f):
    # Functions decorated with this will only run once in the entire programno matter how many times you call it
    # References: https://www.youtube.com/watch?v=r7Dtus7N4pI&ab_channel=Kite
    # References: https://www.youtube.com/watch?v=Kw4TS0OTnj0&ab_channel=Melardev

    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


# Scene System
# https://nicolasivanhoe.wordpress.com/2014/03/10/game-scene-manager-in-python-pygame/
class Director:
    def __init__(self):
        # Create screen
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("game")
        pygame.display.set_icon(pygame.image.load("Logo.png"))
        # There will be multiple scenes in this game
        # similar to how movies are
        # The "director" directs the scenes, telling when the scenes
        # should be played and cut
        # In total, there will are 9 scenes
        # Namely:
        # Credits
        # Intro
        # Scene 1
        # Scene 1 end
        # Scene 2
        # Scene 2 end
        # Scene 3
        # Scene 3 end
        # Game Over
        # These scenes allow me to change the code running at a time,
        # efficiently allowing me to add stages to the game
        self.scene = None
        # Previous Scene allows me to go back to the scene before for restart when you fail
        self.previous_scene = None
        # In Pygame, we will have to keep creating a surface in order to run our game.
        # However, if we just use a while loop, we will not be able to stop the program
        # unless we use task manager
        # Thank goodness, Pygame has a QUIT event
        # allowing us to exit the program by clicking the X button
        # self.quit_flag stores the current state of the game
        # when it's True, the game has stopped
        # and when it's False, the game is running
        self.quit_flag = False
        # this Clock function allows me to set the frame rate
        # so my computer and other computers should have similar experiences
        self.clock = pygame.time.Clock()

    def loop(self):
        while not self.quit_flag:
            # frame rate set at 60 fps
            time = self.clock.tick(60)

            # allows me to quit the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            # this updates the screen in order according to the scene
            if self.scene:
                self.scene.update(time)
                self.scene.show(self.screen)

            pygame.display.flip()
    # this change_screen function allows me to change the scenes according to my wishes
    # for example, after you die, I want to change the scene from Scene 1 (in game)
    # to Game Over (die screen)

    def change_scene(self, scene):
        self.scene = scene

    def quit(self):
        self.quit_flag = True

# Scenes


class Scene:
    def __init__(self, director):
        self.director = director
    # allows me to update the objects displayed on the screen
    # fixing my previously faced problem of having to create a new object
    # every time I want the object to move

    def update(self, delta_time):
        pass
    # show function in preparation for future usage
    # allows me to show a text on screen

    def show(self, screen):
        pass
# Scene With Background allows me to use the background in multiple scenes
# without having to blit it again


class SceneWithBackground(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.bg = Background("pixil-frame-0.png")
        self.bg.set_alpha(100)

    def update(self, delta_time):
        pass
    # shows background on screen

    def show(self, screen):
        self.bg.show(screen)
# Credits time
# since I made everything in this game, including the code, music and art, I have to credit myself for my work


class Credits(Scene):
    def __init__(self, director):

        super().__init__(director)

        # Intro music made by Wee Jie Rei on GarageBand
        # intro song will keep playing until intro scene ends
        self.intro_music = pygame.mixer.Sound("Intro .mp3")
        # credit frames allow me to track how much time has passed
        # allowing me to time my animations
        self.credit_frames = 0

        # Creating a surface for my text for music credits
        # setting the font
        self.font = pygame.font.Font("Game of Squids.ttf", 24)
        # creating the surface the text is on
        # note: For some reason, I can't change the alpha value on a text surface
        # maybe I'm just bad
        # that's why I had to create another surface to blit the text on
        self.music_text_surface = pygame.Surface((800, 60))
        # sets the alpha value, so I can control the transparency for cool fade-in effect
        self.music_alpha = 0
        # creating the text surface
        self.credits_music = self.font.render("Music by: Wee Jie Rei", True, (255, 255, 255))
        # blitting the text on the surface
        self.music_text_surface.blit(self.credits_music, pygame.Rect(0, 0, 10, 10))

        # creating the surface the text is on
        # note: For some reason, I can't change the alpha value on a text surface
        # maybe I'm just bad
        # that's why I had to create another surface to blit the text on
        self.art_text_surface = pygame.Surface((800, 60))
        # sets the alpha value, so I can control the transparency for cool fade-in effect
        self.art_alpha = 0
        # creating the text surface
        self.credits_art = self.font.render("Art by: Wee Jie Rei", True, (255, 255, 255))
        # blitting the text on the surface
        self.art_text_surface.blit(self.credits_art, pygame.Rect(0, 0, 10, 10))

        # creating the surface the text is on
        # note: For some reason, I can't change the alpha value on a text surface
        # maybe I'm just bad
        # that's why I had to create another surface to blit the text on
        self.code_text_surface = pygame.Surface((800, 60))
        # sets the alpha value, so I can control the transparency for cool fade-in effect
        self.code_alpha = 0
        # creating the text surface
        self.credits_code = self.font.render("Code by: Wee Jie Rei", True, (255, 255, 255))
        # blitting the text on the surface
        self.code_text_surface.blit(self.credits_code, pygame.Rect(0, 0, 10, 10))

    def update(self, delta_time):

        self.display(director.screen)
        # plays intro music (Made by Wee Jie Rei)
        self.play_intro_music()

        # allows the player to skip the credits if they are tired of seeing my name appear 3 times
        if pygame.mouse.get_pressed()[0]:
            self.director.previous_scene = credits
            # changes the scene to the intro when the mouse is clicked
            self.director.change_scene(intro)

    def display(self, screen):
        # turns the screen black for fun
        self.director.screen.fill((0, 0, 0))
        # timing for animations of credits
        if self.credit_frames < 250:
            self.music_alpha += 0.8
            self.music_text_surface.set_alpha(self.music_alpha)
            screen.blit(self.music_text_surface, (50, 500))
            self.credit_frames += 1

        elif self.credit_frames < 500:
            self.music_alpha -= 0.8
            self.music_text_surface.set_alpha(self.music_alpha)
            screen.blit(self.music_text_surface, (50, 500))
            self.credit_frames += 1

        elif self.credit_frames < 750:
            self.art_alpha += 0.8
            self.art_text_surface.set_alpha(self.art_alpha)
            screen.blit(self.art_text_surface, (450, 50))
            self.credit_frames += 1

        elif self.credit_frames < 1000:
            self.art_alpha -= 0.8
            self.art_text_surface.set_alpha(self.art_alpha)
            screen.blit(self.art_text_surface, (450, 50))
            self.credit_frames += 1

        elif self.credit_frames < 1250:
            self.code_alpha += 0.8
            self.code_text_surface.set_alpha(self.code_alpha)
            screen.blit(self.code_text_surface, (300, 300))
            self.credit_frames += 1

        elif self.credit_frames < 1450:
            self.code_alpha -= 0.8
            self.code_text_surface.set_alpha(self.code_alpha)
            screen.blit(self.code_text_surface, (300, 300))
            self.credit_frames += 1

        # after a while, the credits will finish playing and the player can enter the game.
        # do note that it took me forever to time the end of credits with the music
        else:
            self.director.previous_scene = credits
            self.director.change_scene(intro)

    # once decorator allows me to only play this particular song once
    # note: I faced a very puzzling problem while adding the music
    # for some reason the music would play twice in quick succession even if i call it once
    # unless I use the @once decorator
    # weird
    @once
    def play_intro_music(self):
        # according to pygame documentation, setting the number of times played to -1 plays it indefinitely
        # incase my player goes AFK :(
        self.intro_music.play(-1)
# Intro scene is the main menu where players can choose to play or to play
# they don't really have a choice since I didn't add a exit button
# but they always have the X on the top right hand corner to close the window :D


class IntroScene(SceneWithBackground):
    def __init__(self, director):

        super().__init__(director)

        # I have no idea what to name this game hahaha...
        self.intro_text = Text(280, 100, (255, 255, 255), "Game of Squids.ttf", 64, "GAME")
        # play button allows the player to play the game
        self.play_button = pygame.image.load("PRESS_PLAY.png")

    def update(self, delta_time):
        # self.mx and self.my get the position of the mouse
        # so that I can tell if they are pressing the button
        self.mx, self.my = pygame.mouse.get_pos()

        super().update(delta_time)

        # blits the play button onto the screen
        self.PRESS_PLAY(director.screen)
        # detects when the player presses the play button
        if 370 < self.mx < 430 and 400 < self.my < 460 and pygame.mouse.get_pressed()[0]:
            # stops the intro music to play the epic rock/heavy metal music for the battle
            self.director.previous_scene.intro_music.stop()
            # changes the scene to the gameplay
            self.director.change_scene(Scene1(director))

    def show(self, screen):
        super().show(screen)

        self.intro_text.show(screen)

    def PRESS_PLAY(self, screen):
        screen.blit(self.play_button, (370, 400))


class GameOver(SceneWithBackground):
    def __init__(self, director):

        super().__init__(director)

        # setting the death music, which is the same as the Intro music
        self.death_music = pygame.mixer.Sound("Intro .mp3")
        # death text just tell you that you are bad
        self.death_text = Text(240, 100, (255, 255, 255), "Game of Squids.ttf", 64, "GAME OVER")
        # replay button allows you to play again, if you want to get good
        self.replay_button = pygame.image.load("RE_START.png")
        # another way i can get the music to play only once, but not sure if it works
        # theoretically gets the music to play only once
        self.played = False

    def update(self, delta_time):
        # once again finds the position of the cursor to press the restart button
        self.mx, self.my = pygame.mouse.get_pos()

        super().__init__(director)

        # plays the DEATH MUSICCCC
        self.play_death_music()
        # blits the restart button onto the screen
        self.RE_PLAY(director.screen)
        # detects when the player is pressing the button
        if 370 < self.mx < 430 and 400 < self.my < 460 and pygame.mouse.get_pressed()[0]:
            # stops the DEATH MUSICCCC
            self.death_music.stop()
            # scene changes back to the previous scene :D
            # allowing the player to restart the stage
            self.director.change_scene(director.previous_scene)
            # stored the previous scene as game over
            self.director.previous_scene = gameover
    # shows the death text (game over)

    def show(self, screen):
        self.death_text.show(screen)
    # maybe solves the problem of double playing??

    def play_death_music(self):
        if not self.played:
            self.death_music.play(-1)
            self.played = True
    # function to blit restart button onto the screen

    def RE_PLAY(self, screen):
        screen.blit(self.replay_button, (370, 400))
# Finally we arrive at the game stages
# each stage has a Level n Scene
# which sets up the basic interface and the enemies spawning
# while the Scene n
# sets up the locations of the enemies


class Level1Scene(SceneWithBackground):
    def __init__(self, director):

        super().__init__(director)

        # creates the player
        self.player = Player(370, 480)
        # sets up the bullets
        self.bullets = self.initial_bullets()
        # starts playing the epic battle music
        self.bgm = pygame.mixer.Sound("ingamerock.mp3")
        # !!!IMPORTANT!!!
        # helps me keep track of how much time has passed since the start of the stage
        # allows me to end the stage when the stage is done
        self.start_time = pygame.time.get_ticks()
        # once again my questionable solution to the double-playing problem
        self.played = False

    def update(self, delta_time):

        super().update(delta_time)

        # plays the epic background music made by Wee Jie Rei
        self.play_bgm()
        self.player.update(delta_time)
        # moves bullets
        for bullet in self.bullets:
            bullet.update(delta_time)
            # checks the collsion of the player and the bullet.
            # check line 1300 for more details
            self.player.check_collision(bullet)
        # checks if the player is still alive
        if self.player.lives <= 0:
            # stored the previous scene as Scene1 so that we can return after we die
            self.director.previous_scene = Scene1(director)
            # stops the epic battle music D:
            self.bgm.stop()
            # changes the scene to game over, because the player died
            self.director.change_scene(gameover)
        # detects when the stage is completed
        elif pygame.time.get_ticks() - self.start_time > 18000:
            # stops the epic batle music :(
            self.bgm.stop()
            # changes scene to the scene completion scene because the player stronk
            self.director.change_scene(scene1_end)
    # spawns the bullets

    def show(self, screen):

        super().show(screen)

        self.player.show(self.director.screen)
        for bullet in self.bullets:
            bullet.show(self.director.screen)

    # plays bgm once?
    def play_bgm(self):
        if not self.played:
            self.bgm.play()
            self.played = True

    def initial_bullets(self):
        pass

# very long list of bullet locations that are not necessary to read through


class Scene1(Level1Scene):
    def initial_bullets(self):
        return [
            # Wave 1
            Bullet(800, 0, -6, 0, 0),
            Bullet(800, 120, -6, 0, 0),
            Bullet(800, 240, -6, 0, 0),
            Bullet(800, 360, -6, 0, 0),
            Bullet(800, 480, -6, 0, 0),
            # Wave 2
            Bullet(800, 60, -6, 0, 1000),
            Bullet(800, 180, -6, 0, 1000),
            Bullet(800, 300, -6, 0, 1000),
            Bullet(800, 420, -6, 0, 1000),
            Bullet(800, 540, -6, 0, 1000),
            # Wave 3
            Bullet(800, 30, -6, 0, 2000),
            Bullet(800, 90, -6, 0, 2000),
            Bullet(800, 150, -6, 0, 2000),
            Bullet(800, 210, -6, 0, 2000),
            Bullet(800, 270, -6, 0, 2000),
            Bullet(800, 330, -6, 0, 2000),
            Bullet(800, 390, -6, 0, 2000),
            Bullet(800, 450, -6, 0, 2000),
            Bullet(800, 570, -6, 0, 2000),
            # Wave 4
            Bullet(800, 0, -6, 0, 3000),
            Bullet(800, 60, -6, 0, 3000),
            Bullet(800, 120, -6, 0, 3000),
            Bullet(800, 180, -6, 0, 3000),
            Bullet(800, 300, -6, 0, 3000),
            Bullet(800, 360, -6, 0, 3000),
            Bullet(800, 420, -6, 0, 3000),
            Bullet(800, 480, -6, 0, 3000),
            Bullet(800, 540, -6, 0, 3000),
            # Wave 5
            Bullet(800, 30, -6, 0, 4000),
            Bullet(800, 150, -6, 0, 4000),
            Bullet(800, 210, -6, 0, 4000),
            Bullet(800, 270, -6, 0, 4000),
            Bullet(800, 330, -6, 0, 4000),
            Bullet(800, 390, -6, 0, 4000),
            Bullet(800, 450, -6, 0, 4000),
            Bullet(800, 510, -6, 0, 4000),
            Bullet(800, 570, -6, 0, 4000),
            # Wave 6
            Bullet(800, 0, -6, 0, 5000),
            Bullet(800, 60, -6, 0, 5000),
            Bullet(800, 120, -6, 0, 5000),
            Bullet(800, 180, -6, 0, 5000),
            Bullet(800, 240, -6, 0, 5000),
            Bullet(800, 300, -6, 0, 5000),
            Bullet(800, 360, -6, 0, 5000),
            Bullet(800, 420, -6, 0, 5000),
            Bullet(800, 480, -6, 0, 5000),
            # Wave 7
            Bullet(800, 30, -6, 0, 6000),
            Bullet(800, 90, -6, 0, 6000),
            Bullet(800, 150, -6, 0, 6000),
            Bullet(800, 210, -6, 0, 6000),
            Bullet(800, 270, -6, 0, 6000),
            Bullet(800, 330, -6, 0, 6000),
            Bullet(800, 390, -6, 0, 6000),
            Bullet(800, 450, -6, 0, 6000),
            Bullet(800, 510, -6, 0, 6000),
            Bullet(800, 570, -6, 0, 6000),

            # Wave 8
            Bullet(800, 0, -6, 0, 7500),
            Bullet(800, 60, -6, 0, 7700),
            Bullet(800, 120, -6, 0, 7900),
            Bullet(800, 180, -6, 0, 8100),
            Bullet(800, 240, -6, 0, 8300),
            Bullet(800, 300, -6, 0, 8500),
            Bullet(800, 360, -6, 0, 8700),
            Bullet(800, 420, -6, 0, 8900),
            Bullet(800, 480, -6, 0, 9100),
            Bullet(800, 540, -6, 0, 9300),

            # Wave 9
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(10500, 12000)),

            # Wave 10
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000)),
            Bullet(800, random.randint(0, 540), -6, 0, random.randint(12000, 13000))
            ]

# stage 1 completion scene


class Scene1_End(SceneWithBackground):
    def __init__(self, director):

        super().__init__(director)

        # plays the win music
        # which is the same as the intro music :P
        # which is made by Wee Jie Rei
        self.win_music = pygame.mixer.Sound("Intro .mp3")
        # win text to tell the player that he won
        self.win_text = Text(240, 100, (255, 255, 255), "Game of Squids.ttf", 32, "LEVEL 1: COMPLETE")
        # next stage button to progress to next stage
        self.next_stage_button = pygame.image.load("nextstage.png")

    def update(self, delta_time):
        # finds the mouse position to detect when the player is pressing the button
        self.mx, self.my = pygame.mouse.get_pos()

        super().__init__(director)

        # blits next stage button to screen
        self.NEXT_STAGE(director.screen)
        # plays win music
        self.play_win_music()
        # detects the player pressing the button
        if 370 < self.mx < 430 and 400 < self.my < 460 and pygame.mouse.get_pressed()[0]:
            # stops the win music :(
            self.win_music.stop()
            # changes the scene to stage 2
            self.director.change_scene(Scene2(director))
            # stores the previous scene as the completion stage
            self.director.previous_scene = Scene1_End(director)
    # shows the win text :D

    def show(self, screen):
        self.win_text.show(screen)

    # plays the win music once, infinitely

    @once
    def play_win_music(self):
        self.win_music.play(-1)
    # loads the next stage button

    def NEXT_STAGE(self, screen):
        screen.blit(self.next_stage_button, (370, 400))


class Level2Scene(SceneWithBackground):
    def __init__(self, director):
        super().__init__(director)
        self.player = Player(370, 480)
        self.bullets = self.initial_bullets()
        self.bgm = pygame.mixer.Sound("ingamerock.mp3")
        self.played = False
        self.start_time = pygame.time.get_ticks()

    def update(self, delta_time):
        global gameover

        super().update(delta_time)

        self.play_bgm()
        self.player.update(delta_time)
        for bullet in self.bullets:
            bullet.update(delta_time)
            self.player.check_collision(bullet)
        if self.player.lives <= 0:
            self.director.previous_scene = Scene2(director)
            self.bgm.stop()
            self.director.change_scene(gameover)
        elif pygame.time.get_ticks() - self.start_time > 15000:
            self.bgm.stop()
            self.director.change_scene(scene2_end)

    def show(self, screen):
        super().show(screen)

        self.player.show(self.director.screen)
        for bullet in self.bullets:
            bullet.show(self.director.screen)

    def play_bgm(self):
        if not self.played:
            self.bgm.play()
            self.played = True

    def initial_bullets(self):
        pass


class Scene2(Level2Scene):
    def initial_bullets(self):
        return [
            # Wave 1
            Bullet(800, 0, -8, 6, 0),
            Bullet(800, 120, -8, 3, 0),
            Bullet(800, 240, -8, 0, 0),
            Bullet(800, 360, -8, -3, 0),
            Bullet(800, 480, -8, -6, 0),
            # Wave 2
            Bullet(800, 300, -8, -2, 500),
            Bullet(800, 300, -8, -1, 500),
            Bullet(800, 300, -8, 0, 500),
            Bullet(800, 300, -8, 1, 500),
            Bullet(800, 300, -8, 2, 500),
            # Wave 3
            Bullet(800, 300, -8, -2, 1000),
            Bullet(800, 300, -8, -1, 1000),
            Bullet(800, 300, -8, 0, 1000),
            Bullet(800, 300, -8, 1, 1000),
            Bullet(800, 300, -8, 2, 1000),
            # Wave 4
            Bullet(800, 200, -8, -2, 1500),
            Bullet(800, 200, -8, -1, 1500),
            Bullet(800, 200, -8, 0, 1500),
            Bullet(800, 200, -8, 1, 1500),
            Bullet(800, 200, -8, 2, 1500),
            Bullet(800, 300, -8, -2, 1500),
            Bullet(800, 300, -8, -1, 1500),
            Bullet(800, 300, -8, 0, 1500),
            Bullet(800, 300, -8, 1, 1500),
            Bullet(800, 300, -8, 2, 1500),
            Bullet(800, 400, -8, -2, 1500),
            Bullet(800, 400, -8, -1, 1500),
            Bullet(800, 400, -8, 0, 1500),
            Bullet(800, 400, -8, 1, 1500),
            Bullet(800, 400, -8, 2, 1500),
            # Wave 5
            Bullet(800, 100, -8, -2, 2000),
            Bullet(800, 100, -8, -1, 2000),
            Bullet(800, 100, -8, 0, 2000),
            Bullet(800, 100, -8, 1, 2000),
            Bullet(800, 100, -8, 2, 2000),
            Bullet(800, 300, -8, -2, 2000),
            Bullet(800, 300, -8, -1, 2000),
            Bullet(800, 300, -8, 0, 2000),
            Bullet(800, 300, -8, 1, 2000),
            Bullet(800, 300, -8, 2, 2000),
            Bullet(800, 500, -8, -2, 2000),
            Bullet(800, 500, -8, -1, 2000),
            Bullet(800, 500, -8, 0, 2000),
            Bullet(800, 500, -8, 1, 2000),
            Bullet(800, 500, -8, 2, 2000),
            # Wave 6
            Bullet(800, 0, random.randint(-20, -10), 0, 3000),
            Bullet(800, 30, random.randint(-20, -10), 0, 3000),
            Bullet(800, 60, random.randint(-20, -10), 0, 3000),
            Bullet(800, 90, random.randint(-20, -10), 0, 3000),
            Bullet(800, 120, random.randint(-20, -10), 0, 3000),
            Bullet(800, 150, random.randint(-20, -10), 0, 3000),
            Bullet(800, 180, random.randint(-20, -10), 0, 3000),
            Bullet(800, 210, random.randint(-20, -10), 0, 3000),
            Bullet(800, 240, random.randint(-20, -10), 0, 3000),
            Bullet(800, 270, random.randint(-20, -10), 0, 3000),
            Bullet(800, 300, random.randint(-20, -10), 0, 3000),
            Bullet(800, 330, random.randint(-20, -10), 0, 3000),
            Bullet(800, 360, random.randint(-20, -10), 0, 3000),
            Bullet(800, 390, random.randint(-20, -10), 0, 3000),
            Bullet(800, 420, random.randint(-20, -10), 0, 3000),
            Bullet(800, 450, random.randint(-20, -10), 0, 3000),
            Bullet(800, 480, random.randint(-20, -10), 0, 3000),
            Bullet(800, 510, random.randint(-20, -10), 0, 3000),
            Bullet(800, 570, random.randint(-20, -10), 0, 3000),
            # Wave 7
            Bullet(800, 0, -8, 0, 3500),
            Bullet(800, 60, -8, 0, 3600),
            Bullet(800, 120, -8, 0, 3700),
            Bullet(800, 180, -8, 0, 3800),
            Bullet(800, 240, -8, 0, 3900),
            Bullet(800, 330, -8, 0, 3900),
            Bullet(800, 390, -8, 0, 3800),
            Bullet(800, 450, -8, 0, 3700),
            Bullet(800, 510, -8, 0, 3600),
            Bullet(800, 570, -8, 0, 3500),
            # Wave 8
            Bullet(800, 0, -10, 0, 5400),
            Bullet(800, 60, -10, 0, 5200),
            Bullet(800, 120, -10, 0, 5000),
            Bullet(800, 180, -10, 0, 4800),
            Bullet(800, 240, -10, 0, 4600),
            Bullet(800, 330, -10, 0, 4600),
            Bullet(800, 390, -10, 0, 4800),
            Bullet(800, 450, -10, 0, 5000),
            Bullet(800, 510, -10, 0, 5200),
            Bullet(800, 570, -10, 0, 5400),
            # Wave 9
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 6000),
            # Wave 10
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7050),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7100),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7150),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7200),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7250),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7300),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7350),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7400),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7450),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7550),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7600),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7650),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7700),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7800),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7850),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7900),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 7950),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8050),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8100),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8150),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8200),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8250),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8300),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8350),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8400),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8450),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8550),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8600),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8650),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8700),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8800),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8850),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8900),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 8950),
            # Wave 11
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9050),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9100),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9150),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9200),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9250),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9300),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9350),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9400),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9450),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9550),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9600),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9650),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9700),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9800),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9850),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9900),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 9950),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10050),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10100),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10150),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10200),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10250),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10300),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10350),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10400),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10450),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10550),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10600),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10650),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10700),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10800),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10850),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10900),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), 0, 10950)
            ]

class Scene2_End(SceneWithBackground):
    def __init__(self, director):
        super().__init__(director)
        self.win_music = pygame.mixer.Sound("Intro .mp3")
        self.win_text = Text(240, 100, (255, 255, 255), "Game of Squids.ttf", 32, "LEVEL 2: COMPLETE")
        self.replay_button = pygame.image.load("nextstage.png")

    def update(self, delta_time):
        self.mx, self.my = pygame.mouse.get_pos()

        super().__init__(director)

        self.NEXT_STAGE(director.screen)
        self.play_win_music()
        if 370 < self.mx < 430 and 400 < self.my < 460 and pygame.mouse.get_pressed()[0]:
            self.win_music.stop()
            self.director.change_scene(Scene3(director))
            self.director.previous_scene = Scene2_End(director)

    def show(self, screen):
        self.win_text.show(screen)

    @once
    def play_win_music(self):
        self.win_music.play(-1)

    def NEXT_STAGE(self, screen):
        screen.blit(self.replay_button, (370, 400))


class Level3Scene(SceneWithBackground):
    def __init__(self, director):
        super().__init__(director)
        self.player = Player(370, 480)
        self.bullets = self.initial_bullets()
        self.bgm = pygame.mixer.Sound("ingamerock.mp3")
        self.played = False
        self.start_time = pygame.time.get_ticks()

    def update(self, delta_time):
        global gameover

        super().update(delta_time)

        self.play_bgm()
        self.player.update(delta_time)
        for bullet in self.bullets:
            bullet.update(delta_time)
            self.player.check_collision(bullet)
        if self.player.lives <= 0:
            self.director.previous_scene = Scene3(director)
            self.bgm.stop()
            self.director.change_scene(gameover)
        elif pygame.time.get_ticks() - self.start_time > 27000:
            self.bgm.stop()
            self.director.change_scene(scene3_end)

    def show(self, screen):
        super().show(screen)

        self.player.show(self.director.screen)
        for bullet in self.bullets:
            bullet.show(self.director.screen)

    def play_bgm(self):
        if not self.played:
            self.bgm.play()
            self.played = True

    def initial_bullets(self):
        pass

# Introduces new bullet
# laser
# deals continuous damage, and is very painful
# I coded it by joining multiple laser bullets together, each bullet dealing one damage
# thus, if you go into the beam
# you take alot of damage


class Scene3(Level3Scene):
    def initial_bullets(self):
        return [
            # Wave 1
            # Laser Beam 1
            Laser(800, 0, -8, 0, 0),
            Laser(800, 0, -8, 0, 240),
            Laser(800, 0, -8, 0, 480),
            Laser(800, 0, -8, 0, 720),
            Laser(800, 0, -8, 0, 960),
            Laser(800, 0, -8, 0, 1200),
            Laser(800, 0, -8, 0, 1440),
            Laser(800, 0, -8, 0, 1680),
            Laser(800, 0, -8, 0, 1920),
            Laser(800, 0, -8, 0, 2160),
            Laser(800, 0, -8, 0, 2400),
            # Laser Beam 2
            Laser(800, 240, -8, 0, 0),
            Laser(800, 240, -8, 0, 240),
            Laser(800, 240, -8, 0, 480),
            Laser(800, 240, -8, 0, 720),
            Laser(800, 240, -8, 0, 960),
            Laser(800, 240, -8, 0, 1200),
            Laser(800, 240, -8, 0, 1440),
            Laser(800, 240, -8, 0, 1680),
            Laser(800, 240, -8, 0, 1920),
            Laser(800, 240, -8, 0, 2160),
            Laser(800, 240, -8, 0, 2400),
            # Laser Beam 3
            Laser(800, 480, -8, 0, 0),
            Laser(800, 480, -8, 0, 240),
            Laser(800, 480, -8, 0, 480),
            Laser(800, 480, -8, 0, 720),
            Laser(800, 480, -8, 0, 960),
            Laser(800, 480, -8, 0, 1200),
            Laser(800, 480, -8, 0, 1440),
            Laser(800, 480, -8, 0, 1680),
            Laser(800, 480, -8, 0, 1920),
            Laser(800, 480, -8, 0, 2160),
            Laser(800, 480, -8, 0, 2400),

            # Wave 2
            # Laser Beam 1
            Laser(800, 120, -8, 0, 2640),
            Laser(800, 120, -8, 0, 2640 + 240),
            Laser(800, 120, -8, 0, 2640 + 480),
            Laser(800, 120, -8, 0, 2640 + 720),
            Laser(800, 120, -8, 0, 2640 + 960),
            Laser(800, 120, -8, 0, 2640 + 1200),
            Laser(800, 120, -8, 0, 2640 + 1440),
            Laser(800, 120, -8, 0, 2640 + 1680),
            Laser(800, 120, -8, 0, 2640 + 1920),
            Laser(800, 120, -8, 0, 2640 + 2160),
            Laser(800, 120, -8, 0, 2640 + 2400),
            # Laser Beam 2
            Laser(800, 360, -8, 0, 2640 + 0),
            Laser(800, 360, -8, 0, 2640 + 240),
            Laser(800, 360, -8, 0, 2640 + 480),
            Laser(800, 360, -8, 0, 2640 + 720),
            Laser(800, 360, -8, 0, 2640 + 960),
            Laser(800, 360, -8, 0, 2640 + 1200),
            Laser(800, 360, -8, 0, 2640 + 1440),
            Laser(800, 360, -8, 0, 2640 + 1680),
            Laser(800, 360, -8, 0, 2640 + 1920),
            Laser(800, 360, -8, 0, 2640 + 2160),
            Laser(800, 360, -8, 0, 2640 + 2400),
            # Wave 3
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),
            Bullet(800, random.randint(0, 600), random.randint(-15, -5), random.randint(-2, 2), 6000),

            # Wave 4
            # Laser Beam 1
            Laser(800, 0, -8, 0, 6000),
            Laser(800, 0, -8, 0, 6240),
            Laser(800, 0, -8, 0, 6480),
            Laser(800, 0, -8, 0, 6720),
            Laser(800, 0, -8, 0, 6960),
            Laser(800, 0, -8, 0, 7200),
            Laser(800, 0, -8, 0, 7440),
            Laser(800, 0, -8, 0, 7680),
            Laser(800, 0, -8, 0, 7920),
            Laser(800, 0, -8, 0, 8160),
            Laser(800, 0, -8, 0, 8400),
            # Laser Beam 2
            Laser(800, 240, -8, 0, 6000),
            Laser(800, 240, -8, 0, 6240),
            Laser(800, 240, -8, 0, 6480),
            Laser(800, 240, -8, 0, 6720),
            Laser(800, 240, -8, 0, 6960),
            Laser(800, 240, -8, 0, 7200),
            Laser(800, 240, -8, 0, 7440),
            Laser(800, 240, -8, 0, 7680),
            Laser(800, 240, -8, 0, 7920),
            Laser(800, 240, -8, 0, 8160),
            Laser(800, 240, -8, 0, 8400),
            # Laser Beam 3
            Laser(800, 480, -8, 0, 6000),
            Laser(800, 480, -8, 0, 6240),
            Laser(800, 480, -8, 0, 6480),
            Laser(800, 480, -8, 0, 6720),
            Laser(800, 480, -8, 0, 6960),
            Laser(800, 480, -8, 0, 7200),
            Laser(800, 480, -8, 0, 7440),
            Laser(800, 480, -8, 0, 7680),
            Laser(800, 480, -8, 0, 7920),
            Laser(800, 480, -8, 0, 8160),
            Laser(800, 480, -8, 0, 8400),
            # Wave 5
            # Laser Beam 1
            Laser(800, 120, -8, 0, 8640),
            Laser(800, 120, -8, 0, 8640 + 240),
            Laser(800, 120, -8, 0, 8640 + 480),
            Laser(800, 120, -8, 0, 8640 + 720),
            Laser(800, 120, -8, 0, 8640 + 960),
            Laser(800, 120, -8, 0, 8640 + 1200),
            Laser(800, 120, -8, 0, 8640 + 1440),
            Laser(800, 120, -8, 0, 8640 + 1680),
            Laser(800, 120, -8, 0, 8640 + 1920),
            Laser(800, 120, -8, 0, 8640 + 2160),
            Laser(800, 120, -8, 0, 8640 + 2400),
            # Laser Beam 2
            Laser(800, 360, -8, 0, 8640 + 0),
            Laser(800, 360, -8, 0, 8640 + 240),
            Laser(800, 360, -8, 0, 8640 + 480),
            Laser(800, 360, -8, 0, 8640 + 720),
            Laser(800, 360, -8, 0, 8640 + 960),
            Laser(800, 360, -8, 0, 8640 + 1200),
            Laser(800, 360, -8, 0, 8640 + 1440),
            Laser(800, 360, -8, 0, 8640 + 1680),
            Laser(800, 360, -8, 0, 8640 + 1920),
            Laser(800, 360, -8, 0, 8640 + 2160),
            Laser(800, 360, -8, 0, 8640 + 2400),
            # Wave 6
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12000),
            # Wave 7
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12500),
            # Wave 8
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            Bullet(800, random.randint(0, 600), random.randint(-20, -10), random.randint(-2, 2), 12750),
            # Wave 9
            Laser(800, 0, -8, 0, 13000),
            Laser(800, 0, -8, 0, 13240),
            Laser(800, 0, -8, 0, 13480),
            Laser(800, 0, -8, 0, 13720),
            Laser(800, 0, -8, 0, 13960),
            Laser(800, 0, -8, 0, 14200),
            Laser(800, 0, -8, 0, 14440),
            Laser(800, 0, -8, 0, 14680),
            Laser(800, 0, -8, 0, 14920),
            Laser(800, 0, -8, 0, 15160),
            Laser(800, 0, -8, 0, 15400),
            Laser(800, 0, -8, 0, 2640 + 13000),
            Laser(800, 0, -8, 0, 2640 + 13240),
            Laser(800, 0, -8, 0, 2640 + 13480),
            Laser(800, 0, -8, 0, 2640 + 13720),
            Laser(800, 0, -8, 0, 2640 + 13960),
            Laser(800, 0, -8, 0, 2640 + 14200),
            Laser(800, 0, -8, 0, 2640 + 14440),
            Laser(800, 0, -8, 0, 2640 + 14680),
            Laser(800, 0, -8, 0, 2640 + 14920),
            Laser(800, 0, -8, 0, 2640 + 15160),
            Laser(800, 0, -8, 0, 2640 + 15400),
            # Laser Beam 2
            Laser(800, 240, -8, 0, 13000),
            Laser(800, 240, -8, 0, 13240),
            Laser(800, 240, -8, 0, 13480),
            Laser(800, 240, -8, 0, 13720),
            Laser(800, 240, -8, 0, 13960),
            Laser(800, 240, -8, 0, 14200),
            Laser(800, 240, -8, 0, 14440),
            Laser(800, 240, -8, 0, 14680),
            Laser(800, 240, -8, 0, 14920),
            Laser(800, 240, -8, 0, 15160),
            Laser(800, 240, -8, 0, 15400),
            Laser(800, 240, -8, 0, 2640 + 13000),
            Laser(800, 240, -8, 0, 2640 + 13240),
            Laser(800, 240, -8, 0, 2640 + 13480),
            Laser(800, 240, -8, 0, 2640 + 13720),
            Laser(800, 240, -8, 0, 2640 + 13960),
            Laser(800, 240, -8, 0, 2640 + 14200),
            Laser(800, 240, -8, 0, 2640 + 14440),
            Laser(800, 240, -8, 0, 2640 + 14680),
            Laser(800, 240, -8, 0, 2640 + 14920),
            Laser(800, 240, -8, 0, 2640 + 15160),
            Laser(800, 240, -8, 0, 2640 + 15400),
            # Laser Beam 3
            Laser(800, 480, -8, 0, 13000),
            Laser(800, 480, -8, 0, 13240),
            Laser(800, 480, -8, 0, 13480),
            Laser(800, 480, -8, 0, 13720),
            Laser(800, 480, -8, 0, 13960),
            Laser(800, 480, -8, 0, 14200),
            Laser(800, 480, -8, 0, 14440),
            Laser(800, 480, -8, 0, 14680),
            Laser(800, 480, -8, 0, 14920),
            Laser(800, 480, -8, 0, 15160),
            Laser(800, 480, -8, 0, 15400),
            Laser(800, 480, -8, 0, 2640 + 13000),
            Laser(800, 480, -8, 0, 2640 + 13240),
            Laser(800, 480, -8, 0, 2640 + 13480),
            Laser(800, 480, -8, 0, 2640 + 13720),
            Laser(800, 480, -8, 0, 2640 + 13960),
            Laser(800, 480, -8, 0, 2640 + 14200),
            Laser(800, 480, -8, 0, 2640 + 14440),
            Laser(800, 480, -8, 0, 2640 + 14680),
            Laser(800, 480, -8, 0, 2640 + 14920),
            Laser(800, 480, -8, 0, 2640 + 15160),
            Laser(800, 480, -8, 0, 2640 + 15400),
            # Wave 10
            # Laser Beam 1
            Laser(800, 120, -8, 0, 420 + 13000),
            Laser(800, 120, -8, 0, 420 + 13240),
            Laser(800, 120, -8, 0, 420 + 13480),
            Laser(800, 120, -8, 0, 420 + 13720),
            Laser(800, 120, -8, 0, 420 + 13960),
            Laser(800, 120, -8, 0, 420 + 14200),
            Laser(800, 120, -8, 0, 420 + 14440),
            Laser(800, 120, -8, 0, 420 + 14680),
            Laser(800, 120, -8, 0, 420 + 14920),
            Laser(800, 120, -8, 0, 420 + 15160),
            Laser(800, 120, -8, 0, 420 + 15400),
            Laser(800, 120, -8, 0, 2640 + 420 + 13000),
            Laser(800, 120, -8, 0, 2640 + 420 + 13240),
            Laser(800, 120, -8, 0, 2640 + 420 + 13480),
            Laser(800, 120, -8, 0, 2640 + 420 + 13720),
            Laser(800, 120, -8, 0, 2640 + 420 + 13960),
            Laser(800, 120, -8, 0, 2640 + 420 + 14200),
            Laser(800, 120, -8, 0, 2640 + 420 + 14440),
            Laser(800, 120, -8, 0, 2640 + 420 + 14680),
            Laser(800, 120, -8, 0, 2640 + 420 + 14920),
            Laser(800, 120, -8, 0, 2640 + 420 + 15160),
            Laser(800, 120, -8, 0, 2640 + 420 + 15400),
            # Laser Beam 2
            Laser(800, 360, -8, 0, 420 + 13000),
            Laser(800, 360, -8, 0, 420 + 13240),
            Laser(800, 360, -8, 0, 420 + 13480),
            Laser(800, 360, -8, 0, 420 + 13720),
            Laser(800, 360, -8, 0, 420 + 13960),
            Laser(800, 360, -8, 0, 420 + 14200),
            Laser(800, 360, -8, 0, 420 + 14440),
            Laser(800, 360, -8, 0, 420 + 14680),
            Laser(800, 360, -8, 0, 420 + 14920),
            Laser(800, 360, -8, 0, 420 + 15160),
            Laser(800, 360, -8, 0, 420 + 15400),
            Laser(800, 360, -8, 0, 2640 + 420 + 13000),
            Laser(800, 360, -8, 0, 2640 + 420 + 13240),
            Laser(800, 360, -8, 0, 2640 + 420 + 13480),
            Laser(800, 360, -8, 0, 2640 + 420 + 13720),
            Laser(800, 360, -8, 0, 2640 + 420 + 13960),
            Laser(800, 360, -8, 0, 2640 + 420 + 14200),
            Laser(800, 360, -8, 0, 2640 + 420 + 14440),
            Laser(800, 360, -8, 0, 2640 + 420 + 14680),
            Laser(800, 360, -8, 0, 2640 + 420 + 14920),
            Laser(800, 360, -8, 0, 2640 + 420 + 15160),
            Laser(800, 360, -8, 0, 2640 + 420 + 15400),
            # Laser Beam 3
            Laser(800, 600, -8, 0, 420 + 13000),
            Laser(800, 600, -8, 0, 420 + 13240),
            Laser(800, 600, -8, 0, 420 + 13480),
            Laser(800, 600, -8, 0, 420 + 13720),
            Laser(800, 600, -8, 0, 420 + 13960),
            Laser(800, 600, -8, 0, 420 + 14200),
            Laser(800, 600, -8, 0, 420 + 14440),
            Laser(800, 600, -8, 0, 420 + 14680),
            Laser(800, 600, -8, 0, 420 + 14920),
            Laser(800, 600, -8, 0, 420 + 15160),
            Laser(800, 600, -8, 0, 420 + 15400),
            Laser(800, 600, -8, 0, 2640 + 420 + 13000),
            Laser(800, 600, -8, 0, 2640 + 420 + 13240),
            Laser(800, 600, -8, 0, 2640 + 420 + 13480),
            Laser(800, 600, -8, 0, 2640 + 420 + 13720),
            Laser(800, 600, -8, 0, 2640 + 420 + 13960),
            Laser(800, 600, -8, 0, 2640 + 420 + 14200),
            Laser(800, 600, -8, 0, 2640 + 420 + 14440),
            Laser(800, 600, -8, 0, 2640 + 420 + 14680),
            Laser(800, 600, -8, 0, 2640 + 420 + 14920),
            Laser(800, 600, -8, 0, 2640 + 420 + 15160),
            Laser(800, 600, -8, 0, 18460),
            # Wave 11
            Bullet(800, 60, -10, 0, 19020),
            Bullet(800, 90, -10, 0, 19030),
            Bullet(800, 120, -10, 0, 19040),
            Bullet(800, 150, -10, 0, 19050),
            Bullet(800, 180, -10, 0, 19060),
            Bullet(800, 210, -10, 0, 19070),
            Bullet(800, 240, -10, 0, 19080),
            Bullet(800, 270, -10, 0, 19090),
            Bullet(800, 300, -10, 0, 19100),
            Bullet(800, 330, -10, 0, 19110),
            Bullet(800, 360, -10, 0, 19120),
            Bullet(800, 390, -10, 0, 19130),
            Bullet(800, 420, -10, 0, 19140),
            Bullet(800, 450, -10, 0, 19150),
            Bullet(800, 480, -10, 0, 19160),
            Bullet(800, 510, -10, 0, 19170),
            Bullet(800, 540, -10, 0, 19180),
            Bullet(800, 540, -10, 0, 19210),
            Bullet(800, 510, -10, 0, 19220),
            Bullet(800, 480, -10, 0, 19230),
            Bullet(800, 450, -10, 0, 19240),
            Bullet(800, 420, -10, 0, 19250),
            Bullet(800, 390, -10, 0, 19260),
            Bullet(800, 360, -10, 0, 19270),
            Bullet(800, 330, -10, 0, 19280),
            Bullet(800, 300, -10, 0, 19290),
            Bullet(800, 270, -10, 0, 19300),
            Bullet(800, 240, -10, 0, 19310),
            Bullet(800, 210, -10, 0, 19320),
            Bullet(800, 180, -10, 0, 19330),
            Bullet(800, 150, -10, 0, 19340),
            Bullet(800, 120, -10, 0, 19350),
            Bullet(800, 90, -10, 0, 19360),
            Bullet(800, 60, -10, 0, 19370),
            Bullet(800, 60, -10, 0, 19420),
            Bullet(800, 90, -10, 0, 19430),
            Bullet(800, 120, -10, 0, 19440),
            Bullet(800, 150, -10, 0, 19450),
            Bullet(800, 180, -10, 0, 19460),
            Bullet(800, 210, -10, 0, 19470),
            Bullet(800, 240, -10, 0, 19480),
            Bullet(800, 270, -10, 0, 19490),
            Bullet(800, 300, -10, 0, 19500),
            Bullet(800, 330, -10, 0, 19510),
            Bullet(800, 360, -10, 0, 19520),
            Bullet(800, 390, -10, 0, 19530),
            Bullet(800, 420, -10, 0, 19540),
            Bullet(800, 450, -10, 0, 19550),
            Bullet(800, 480, -10, 0, 19560),
            Bullet(800, 510, -10, 0, 19570),
            Bullet(800, 540, -10, 0, 19580),
            Bullet(800, 570, -10, 0, 19590),
            Bullet(800, 570, -10, 0, 19600),
            Bullet(800, 540, -10, 0, 19610),
            Bullet(800, 510, -10, 0, 19620),
            Bullet(800, 480, -10, 0, 19630),
            Bullet(800, 450, -10, 0, 19640),
            Bullet(800, 420, -10, 0, 19650),
            Bullet(800, 390, -10, 0, 19660),
            Bullet(800, 360, -10, 0, 19670),
            Bullet(800, 330, -10, 0, 19680),
            Bullet(800, 300, -10, 0, 19690),
            Bullet(800, 270, -10, 0, 19700),
            Bullet(800, 240, -10, 0, 19710),
            Bullet(800, 210, -10, 0, 19720),
            Bullet(800, 180, -10, 0, 19730),
            Bullet(800, 150, -10, 0, 19740),
            Bullet(800, 120, -10, 0, 19750),
            Bullet(800, 90, -10, 0, 19760),
            Bullet(800, 60, -10, 0, 19770),

            Laser(800, 120, -8, 0, 420 + 20000),
            Laser(800, 120, -8, 0, 420 + 20240),
            Laser(800, 120, -8, 0, 420 + 20480),
            Laser(800, 120, -8, 0, 420 + 20720),
            Laser(800, 120, -8, 0, 420 + 20960),
            Laser(800, 120, -8, 0, 420 + 21200),
            Laser(800, 120, -8, 0, 420 + 21440),
            Laser(800, 120, -8, 0, 420 + 21680),
            Laser(800, 120, -8, 0, 420 + 21920),
            Laser(800, 120, -8, 0, 420 + 22160),
            Laser(800, 120, -8, 0, 420 + 22400),
            Laser(800, 120, -8, 0, 2640 + 420 + 20000),
            Laser(800, 120, -8, 0, 2640 + 420 + 20240),
            Laser(800, 120, -8, 0, 2640 + 420 + 20480),
            Laser(800, 120, -8, 0, 2640 + 420 + 20720),
            Laser(800, 120, -8, 0, 2640 + 420 + 20960),
            Laser(800, 120, -8, 0, 2640 + 420 + 21200),
            Laser(800, 120, -8, 0, 2640 + 420 + 21440),
            Laser(800, 120, -8, 0, 2640 + 420 + 21680),
            Laser(800, 120, -8, 0, 2640 + 420 + 21920),
            Laser(800, 120, -8, 0, 2640 + 420 + 21160),
            Laser(800, 120, -8, 0, 2640 + 420 + 21400),
            # Laser Beam 2
            Laser(800, 360, -8, 0, 420 + 20000),
            Laser(800, 360, -8, 0, 420 + 20240),
            Laser(800, 360, -8, 0, 420 + 20480),
            Laser(800, 360, -8, 0, 420 + 20720),
            Laser(800, 360, -8, 0, 420 + 20960),
            Laser(800, 360, -8, 0, 420 + 21200),
            Laser(800, 360, -8, 0, 420 + 21440),
            Laser(800, 360, -8, 0, 420 + 21680),
            Laser(800, 360, -8, 0, 420 + 21920),
            Laser(800, 360, -8, 0, 420 + 22160),
            Laser(800, 360, -8, 0, 420 + 22400),
            Laser(800, 360, -8, 0, 2640 + 420 + 20000),
            Laser(800, 360, -8, 0, 2640 + 420 + 20240),
            Laser(800, 360, -8, 0, 2640 + 420 + 20480),
            Laser(800, 360, -8, 0, 2640 + 420 + 20720),
            Laser(800, 360, -8, 0, 2640 + 420 + 20960),
            Laser(800, 360, -8, 0, 2640 + 420 + 21200),
            Laser(800, 360, -8, 0, 2640 + 420 + 21440),
            Laser(800, 360, -8, 0, 2640 + 420 + 21680),
            Laser(800, 360, -8, 0, 2640 + 420 + 21920),
            Laser(800, 360, -8, 0, 2640 + 420 + 22160),
            Laser(800, 360, -8, 0, 2640 + 420 + 22400),
            # Laser Beam 3
            Laser(800, 600, -8, 0, 420 + 20000),
            Laser(800, 600, -8, 0, 420 + 20240),
            Laser(800, 600, -8, 0, 420 + 20480),
            Laser(800, 600, -8, 0, 420 + 20720),
            Laser(800, 600, -8, 0, 420 + 20960),
            Laser(800, 600, -8, 0, 420 + 21200),
            Laser(800, 600, -8, 0, 420 + 21440),
            Laser(800, 600, -8, 0, 420 + 21920),
            Laser(800, 600, -8, 0, 420 + 22160),
            Laser(800, 600, -8, 0, 420 + 2400),
            Laser(800, 600, -8, 0, 2640 + 420 + 20000),
            Laser(800, 600, -8, 0, 2640 + 420 + 20240),
            Laser(800, 600, -8, 0, 2640 + 420 + 20480),
            Laser(800, 600, -8, 0, 2640 + 420 + 20720),
            Laser(800, 600, -8, 0, 2640 + 420 + 20960),
            Laser(800, 600, -8, 0, 2640 + 420 + 21200),
            Laser(800, 600, -8, 0, 2640 + 420 + 21440),
            Laser(800, 600, -8, 0, 2640 + 420 + 21680),
            Laser(800, 600, -8, 0, 2640 + 420 + 21920),
            Laser(800, 600, -8, 0, 2640 + 420 + 22160),
            Laser(800, 600, -8, 0, 25460),
            ]

# finally the game has come to an end


class Scene3_End(SceneWithBackground):
    def __init__(self, director):
        super().__init__(director)
        self.win_music = pygame.mixer.Sound("Intro .mp3")
        self.win_text = Text(240, 100, (255, 255, 255), "Game of Squids.ttf", 32, "BOSS: COMPLETE")

    def update(self, delta_time):

        super().__init__(director)

        self.play_win_music()


    def show(self, screen):
        self.win_text.show(screen)

    @once
    def play_win_music(self):
        self.win_music.play(-1)

# Entities
# Now we move on to the entities like the player and the bullets
# parent class Entity


class Entity:
    def show(self, screen: pygame.Surface):
        pass

    def update(self, delta_time: int):
        pass

# player class
# controls all the necessary things that a player necessarily needs to play
# like x and y, speed, control, lives, etc.


class Player(Entity):
    # I am speed
    SPEED = 3

    def __init__(self, x, y):
        # self.x and self.y are the spawning locations of the player
        # self.dx and self.dy are the changes in the location of the player caused by inputs by the player
        # self.lives are the number of lives you have
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.lives = 5
        self.img = pygame.image.load("player.png")
        self.heart_img = pygame.image.load("heart.png")
        # note: the woomp sound was recorded using a mic by yours truly
        # 11/10 voice acting
        # Woomp.mp3 feat. Wee Jie Rei
        self.damage_sound = pygame.mixer.Sound("Woomp.mp3")

    def show(self, screen: pygame.Surface):
        screen.blit(self.img, (self.x, self.y))

        # hearts
        # this displays the hearts on screen
        # shows you how much life you have
        # if it drops to 0 you lose
        for i in range(self.lives):
            screen.blit(self.heart_img, (5 + i * 32, 5))

    def update(self, delta_time):
        pressed = pygame.key.get_pressed()

        # basic controls
        # if you press left, it go left
        # if you press right, it go right
        # if you press up, it go up
        # if you press down, it go down
        # i separated the dx and dy so that we can control the player more smoothly
        # if not then what happens is that the heart will sometimes go in the opposite directions of your input
        # which is weird
        # and not intentional

        if pressed[pygame.K_LEFT] and pressed[pygame.K_RIGHT]:
            self.dx = 0
        elif pressed[pygame.K_LEFT]:
            self.dx = -Player.SPEED
        elif pressed[pygame.K_RIGHT]:
            self.dx = Player.SPEED
        else:
            self.dx = 0

        if pressed[pygame.K_UP] and pressed[pygame.K_DOWN]:
            self.dy = 0
        elif pressed[pygame.K_UP]:
            self.dy = -Player.SPEED
        elif pressed[pygame.K_DOWN]:
            self.dy = Player.SPEED
        else:
            self.dy = 0

        self.x += self.dx
        self.y += self.dy

        # restricts the player so it doesn't run out of the player interface
        self.x = min(max(self.x, -2), 770)
        self.y = min(max(self.y, -4), 571)

    # checks the collision
    # since the bullets and lasers have different hitboxes, I coded them separately
    def check_collision(self, bullet):
        if type(bullet) == Bullet:
            if self.x <= bullet.x + 7 <= self.x + 29 and self.y <= bullet.y + 24 <= self.y + 29 \
                    and \
                    not bullet.taken_damage:
                self.lives -= 1
                # woomp
                self.damage_sound.play()
                bullet.taken_damage = True

        if type(bullet) == Laser:
            if bullet.x <= self.x <= bullet.x + 120 and bullet.y + 32 <= self.y <= bullet.y + 88\
                    and \
                    not bullet.taken_damage:
                self.lives -= 1
                # woomp
                self.damage_sound.play()
                bullet.taken_damage = True


# bullet class
# pew pew
class Bullet(Entity):
    def __init__(self, x, y, dx, dy, delay):
        # contains all the necessary tools for the bullet to kill the player
        # x, y determines the spawn location of the bullet
        # dx and dy show the change in the location
        # delay allows me to time when the bullets spawn
        # taken_damage allows me to stop the player from taking more damage from the same bullet
        # so they don't just die immediately when they hit a bullet
        # todo: R.I.P Shinzo Abe
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.delay = delay
        self.img = pygame.image.load("bullet1.png")
        self.start_time = None
        self.taken_damage = False
    # blits the bullet

    def show(self, screen: pygame.Surface):
        screen.blit(self.img, (self.x, self.y))

    # start time allows it to time the delay
    # so i can stagger the bullets
    def update(self, delta_time):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.start_time > self.delay:
            self.x += self.dx
            self.y += self.dy

# laser class is laser
# i was lazy to come up with a decent laser code that allows me to create a beam
# that's why the bullet data for scene 3 is so long


class Laser(Entity):
    def __init__(self, x, y, dx, dy, delay):
        # contains all the necessary tools for the bullet to kill the player
        # x, y determines the spawn location of the bullet
        # dx and dy show the change in the location
        # delay allows me to time when the bullets spawn
        # taken_damage allows me to stop the player from taking more damage from the same bullet
        # so they don't just die immediately when they hit a bullet
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.delay = delay
        self.img = pygame.image.load("Laser.png")
        self.start_time = None
        self.taken_damage = False

    # blits laser
    def show(self, screen: pygame.Surface):
        screen.blit(self.img, (self.x, self.y))

    # times laser
    def update(self, delta_time: int):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.start_time > self.delay:
            self.x += self.dx
            self.y += self.dy

# allows me to easily create text


class Text(Entity):
    def __init__(self, x, y, colour, font, fontSize, text):
        self.font = pygame.font.Font(font, fontSize)
        self.fontSize = fontSize
        self.text = self.font.render(text, True, colour)
        self.x = x
        self.y = y

    def show(self, screen: pygame.Surface):
        screen.blit(self.text, (self.x, self.x))

    def update(self):
        pass

# Allows me to set the background


class Background(Entity):
    def __init__(self, img):
        self.picture = img
        self.img = pygame.image.load(self.picture).convert_alpha()
        self.alpha = 100

    def set_alpha(self, alpha):
        self.img.set_alpha(alpha)

    def show(self, screen):
        screen.blit(self.img, (0, 0))

    def update(self):
        pass

# loads the libraries


pygame.init()
pygame.font.init()
pygame.mixer.init()


director = Director()
scene1 = Scene1(director)
scene1_end = Scene1_End(director)
scene2 = Scene2(director)
scene2_end = Scene2_End(director)
scene3 = Scene3(director)
scene3_end = Scene3_End(director)
gameover = GameOver(director)
intro = IntroScene(director)
credits = Credits(director)

# game starts with credits
director.change_scene(credits)

# game loop
director.loop()
