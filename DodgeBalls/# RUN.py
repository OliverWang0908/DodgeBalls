# RUN

from Sprite import Player, Ball, SnowFlake
from Window import window
import pygame
import time
import sys

# basic settings
pygame.init()
WIDTH, HEIGHT, move_speed = 600, 800, 7

win = window(WIDTH, HEIGHT)
img_path = "player.png"



# run
def run_game():
    player = Player(WIDTH, HEIGHT, speed = move_speed, img_path = "player.png")
    balls = []
    snowflakes = []
    spawn_timer = 0
    score_start = time.time()
    game_over = False
    fall_speed = 4


    while True:
        win.screen.fill((245, 245, 245))
        keys = pygame.key.get_pressed()
        
      

     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over and event.type == pygame.KEYDOWN:
                return 
        
        if len(snowflakes) < 80:   
            snowflakes.append(SnowFlake(WIDTH, HEIGHT))

        
        for snow in snowflakes[:]:
            snow.update()
            if snow.off_screen():
                snowflakes.remove(snow)

        if not game_over:
            player.move(keys, WIDTH)

            spawn_timer += 1
            if spawn_timer > 48:  
                balls.append(Ball(fall_speed, WIDTH))
                spawn_timer = 0

            
            fall_speed += 0.002

           
            for ball in balls:
                ball.update()

            # ====== collision detection ======
            for ball in balls:
                if player.rect.colliderect(ball.rect):
                    game_over = True
                    survival = time.time() - score_start

        # ====== visual ======
        player.draw(win.screen)
        for ball in balls:
            ball.draw(win.screen)

        # score
        if not game_over:
            survival = time.time() - score_start
        score_text = win.FONT.render(f"Time: {survival:.1f}s", True, (0, 0, 0))
        win.screen.blit(score_text, (20, 20))

        # Game Over 
        if game_over:
            msg1 = win.FONT.render("GAME OVER!", True, (200, 0, 0))
            msg2 = win.FONT.render("Press any key to restart", True, (0, 0, 0))
            win.screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, HEIGHT//2 - 40))
            win.screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, HEIGHT//2 + 10))

        pygame.display.flip()
        win.clock.tick(60)


if __name__ == "__main__":
    run_game()



