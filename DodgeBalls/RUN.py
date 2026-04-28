# RUN

import random
import sys

import pygame

from Sprite import Ball, Particle, Player, PowerUp, SnowFlake
from Window import window


pygame.init()
WIDTH, HEIGHT, MOVE_SPEED = 600, 800, 7

win = window(WIDTH, HEIGHT)
IMG_PATH = "player.png"


def add_burst(particles, x, y, color, amount=16):
    for _ in range(amount):
        particles.append(Particle(x, y, color))


def reset_game():
    return {
        "player": Player(WIDTH, HEIGHT, speed=MOVE_SPEED, img_path=IMG_PATH),
        "balls": [],
        "powerups": [],
        "particles": [],
        "snowflakes": [SnowFlake(WIDTH, HEIGHT) for _ in range(90)],
        "ball_timer": 0,
        "power_timer": 3.0,
        "survival": 0,
        "score": 0,
        "combo": 1,
        "combo_timer": 0,
        "difficulty": 0,
        "slow_time": 0,
        "boost_time": 0,
        "screen_shake": 0,
    }


def apply_powerup(state, powerup):
    player = state["player"]
    if powerup.kind == "shield":
        player.shield_time = 6
    elif powerup.kind == "heal":
        player.lives = min(player.max_lives, player.lives + 1)
    elif powerup.kind == "slow":
        state["slow_time"] = 7
    elif powerup.kind == "boost":
        state["boost_time"] = 8
    state["score"] += 80
    add_burst(state["particles"], powerup.x, powerup.y, PowerUp.TYPES[powerup.kind]["color"], 24)


def update_playing(state, dt):
    player = state["player"]
    keys = pygame.key.get_pressed()
    player.move(keys, WIDTH, HEIGHT, dt)
    player.update(dt)

    state["survival"] += dt
    state["difficulty"] += dt * 0.045
    state["ball_timer"] -= dt
    state["power_timer"] -= dt
    state["slow_time"] = max(0, state["slow_time"] - dt)
    state["boost_time"] = max(0, state["boost_time"] - dt)
    state["combo_timer"] = max(0, state["combo_timer"] - dt)
    state["screen_shake"] = max(0, state["screen_shake"] - dt)

    if state["combo_timer"] == 0:
        state["combo"] = 1

    spawn_delay = max(0.22, 0.72 - state["difficulty"] * 0.055)
    if state["ball_timer"] <= 0:
        base_speed = 3.2 + min(5.4, state["difficulty"] * 0.48)
        state["balls"].append(Ball(base_speed, WIDTH))
        if state["difficulty"] > 4 and random.random() < 0.25:
            state["balls"].append(Ball(base_speed * 0.92, WIDTH))
        state["ball_timer"] = spawn_delay

    if state["power_timer"] <= 0:
        state["powerups"].append(PowerUp(WIDTH))
        state["power_timer"] = random.uniform(6.5, 9.5)

    slow_factor = 0.42 if state["slow_time"] > 0 else 1.0
    for ball in state["balls"][:]:
        ball.update(dt, slow_factor)
        if ball.collides_with(player.rect):
            add_burst(state["particles"], ball.x, ball.y, ball.color, 18)
            state["balls"].remove(ball)
            state["combo"] = 1
            state["combo_timer"] = 0
            state["screen_shake"] = 0.18
            if player.take_hit():
                return "game_over"
        elif ball.off_screen(HEIGHT):
            state["balls"].remove(ball)
            state["combo"] = min(9, state["combo"] + 1)
            state["combo_timer"] = 2.2
            multiplier = 2 if state["boost_time"] > 0 else 1
            state["score"] += ball.value * state["combo"] * multiplier

    for powerup in state["powerups"][:]:
        powerup.update(dt)
        if player.rect.colliderect(powerup.rect):
            state["powerups"].remove(powerup)
            apply_powerup(state, powerup)
        elif powerup.off_screen(HEIGHT):
            state["powerups"].remove(powerup)

    for particle in state["particles"][:]:
        particle.update(dt)
        if not particle.alive():
            state["particles"].remove(particle)

    return "playing"


def update_ambient(state, dt):
    while len(state["snowflakes"]) < 90:
        state["snowflakes"].append(SnowFlake(WIDTH, HEIGHT))
    for snow in state["snowflakes"][:]:
        snow.update(dt)
        if snow.off_screen():
            state["snowflakes"].remove(snow)


def draw_game(state, high_score):
    shake_x = 0
    shake_y = 0
    if state["screen_shake"] > 0:
        shake_x = random.randint(-4, 4)
        shake_y = random.randint(-4, 4)

    original = win.screen
    if shake_x or shake_y:
        temp = pygame.Surface((WIDTH, HEIGHT))
        win.screen = temp

    win.draw_background(state["snowflakes"], state["score"])
    for powerup in state["powerups"]:
        powerup.draw(win.screen, win.POWER)
    for ball in state["balls"]:
        ball.draw(win.screen)
    for particle in state["particles"]:
        particle.draw(win.screen)
    state["player"].draw(win.screen)
    win.draw_hud(
        state["player"],
        state["score"],
        state["survival"],
        high_score,
        state["combo"],
        state["slow_time"],
        state["boost_time"],
    )

    if shake_x or shake_y:
        win.screen = original
        win.screen.blit(temp, (shake_x, shake_y))


def run_game():
    state = reset_game()
    mode = "menu"
    high_score = 0

    while True:
        dt = win.clock.tick(60) / 1000
        dt = min(dt, 1 / 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if mode == "directions":
                        mode = "menu"
                        continue
                    pygame.quit()
                    sys.exit()
                if mode == "menu" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    state = reset_game()
                    mode = "playing"
                elif mode == "directions" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    mode = "menu"
                elif mode == "playing" and event.key == pygame.K_p:
                    mode = "paused"
                elif mode == "paused" and event.key == pygame.K_p:
                    mode = "playing"
                elif mode == "game_over" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    state = reset_game()
                    mode = "playing"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode == "menu" and win.direction_button_rect().collidepoint(event.pos):
                    mode = "directions"
                elif mode == "directions" and win.directions_back_rect().collidepoint(event.pos):
                    mode = "menu"

        update_ambient(state, dt)
        if mode == "playing":
            mode = update_playing(state, dt)
            if mode == "game_over":
                high_score = max(high_score, state["score"])

        draw_game(state, high_score)
        if mode == "menu":
            win.draw_menu(high_score)
        elif mode == "directions":
            win.draw_directions()
        elif mode == "paused":
            win.draw_pause()
        elif mode == "game_over":
            win.draw_game_over(state["score"], high_score, state["survival"])

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
