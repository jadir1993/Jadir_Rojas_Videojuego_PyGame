import pygame
import sys
import random
import math

pygame.init()

# Configuración del juego
width = 720
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Proyecto PyGame - Jadir Rojas")

# Colores
white = (255, 255, 255)
indigo =(75, 0, 130)
forestgreen = (34, 139, 34)
darkorange = (255, 140, 0)
red = (178, 34, 34)
black = (0, 0, 0)

# Jugador
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size

# Obstáculos
obstacle_size = 50
obstacle_speed = 5
obstacle_frequency = 25
obstacles = []

# Enemigos
enemy_speed = 7
enemies = []

# Reloj
clock = pygame.time.Clock()

# Función para dibujar al jugador
def draw_player(x, y):
    pygame.draw.rect(screen, darkorange, [x, y, player_size, player_size])

# Función para dibujar obstáculos
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, red, obstacle)

# Función para dibujar enemigos
def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.circle(screen, indigo, (enemy[0], enemy[1]), enemy[2])

# Función para mostrar el menú
def show_menu():
    font = pygame.font.SysFont(None, 35)

    option_play = font.render("Presiona SPACE para jugar", True, forestgreen)
    option_exit = font.render("Presiona ESC para salir", True, forestgreen)

    # Calcular las posiciones verticales centradas
    y_center = height // 2
    y_play = y_center - option_play.get_height() // 2
    y_exit = y_center + option_exit.get_height() // 2 + 10  # Separación entre los textos

    screen.blit(option_play, (width // 2 - option_play.get_width() // 2, y_play))
    screen.blit(option_exit, (width // 2 - option_exit.get_width() // 2, y_exit))
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_key = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def show_game_over():
    global obstacles, enemies

    font = pygame.font.SysFont(None, 70)
    text = font.render("Game Over", True, red)
    text_rect = text.get_rect(center=(width // 2, height // 2))

    showing_game_over = True

    while showing_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                showing_game_over = False

        screen.fill(black)

        if showing_game_over:
            screen.blit(text, text_rect)

        pygame.display.flip()

    # Limpiar listas al reiniciar el juego
    obstacles.clear()
    enemies.clear()

    # Reiniciar posición del jugador
    global player_x
    player_x = width // 2 - player_size // 2

    # Volver al bucle principal del juego
    game()
                

# Función principal del juego
def game():
    global player_x, obstacles, enemies
 
  # Limpiar listas al inicio del juego
    obstacles.clear()
    enemies.clear()
    
    show_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += 5

        screen.fill(black)

        # Generar obstáculos
        if random.randint(1, obstacle_frequency) == 1:
            obstacle_x = random.randint(0, width - obstacle_size)
            obstacle_y = 0
            obstacles.append([obstacle_x, obstacle_y, obstacle_size, obstacle_size])

        # Generar enemigos
        if random.randint(1, obstacle_frequency * 2) == 1:
            enemy_radius = random.randint(15, 30)
            enemy_x = random.randint(enemy_radius, width - enemy_radius)
            enemy_y = 0
            enemies.append([enemy_x, enemy_y, enemy_radius])

        # Mover y dibujar obstáculos
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
        draw_obstacles(obstacles)

        # Mover y dibujar enemigos
        for enemy in enemies:
            enemy[1] += enemy_speed
        draw_enemies(enemies)

        # Eliminar obstáculos fuera de la pantalla
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] < height]

        # Eliminar enemigos fuera de la pantalla
        enemies = [enemy for enemy in enemies if enemy[1] < height]

        # Dibujar jugador
        draw_player(player_x, player_y)

        # Colisiones con obstáculos
        for obstacle in obstacles:
            if (
                player_x < obstacle[0] < player_x + player_size
                or player_x < obstacle[0] + obstacle_size < player_x + player_size
            ) and (
                player_y < obstacle[1] < player_y + player_size
                or player_y < obstacle[1] + obstacle_size < player_y + player_size
            ):
                print("¡Has perdido!")
                show_game_over()
                

        # Colisiones con enemigos
        for enemy in enemies:
            distance = math.sqrt((player_x - enemy[0])**2 + (player_y - enemy[1])**2)
            if distance < player_size / 2 + enemy[2]:
                print("¡Has perdido!")
                show_game_over()
                

        pygame.display.flip()
        clock.tick(30)

# Iniciar el juego
game()
