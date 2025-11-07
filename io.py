import pygame
import random
import sys

pygame.init()

# Configuración de pantalla y colores
ANCHO, ALTO = 800, 600
FPS = 60
COLOR_FONDO = (30, 30, 30)
COLOR_JUGADOR = (50, 200, 50)
COLOR_ENEMIGO = (200, 50, 50)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Crecimiento Total")

clock = pygame.time.Clock()

class Bloque:
    def __init__(self, x, y, tam, color, vel=0):
        self.x = x
        self.y = y
        self.tam = tam
        self.radius = max(1, tam // 2)
        self.color = color
        speed = vel
        
        # Velocidad aleatoria del enemigo
        self.vel_x = random.choice([-1, 1]) * speed if speed != 0 else 0
        self.vel_y = random.choice([-1, 1]) * speed if speed != 0 else 0

    def dibujar(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
         # Rebotes en los bordes de la pantalla
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vel_x *= -1
        if self.x + self.radius >= ANCHO:
            self.x = ANCHO - self.radius
            self.vel_x *= -1
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vel_y *= -1
        if self.y + self.radius >= ALTO:
            self.y = ALTO - self.radius
            self.vel_y *= -1
            
    # Detección de colisión entre dos círculos mediante distancia
    def collides_with(self, other) -> bool:
        dx = self.x - other.x
        dy = self.y - other.y
        distancia_sq = dx * dx + dy * dy
        suma_radios = self.radius + other.radius
        return distancia_sq <= (suma_radios * suma_radios)



def generar_enemigo():
    tam = random.randint(10, 80)
    radius = tam // 2
    x = random.randint(radius, ANCHO - radius)
    y = random.randint(radius, ALTO - radius)
    vel = random.uniform(1, 3)
    return Bloque(x, y, tam, COLOR_ENEMIGO, vel)

def generar_enemigos(num):
    return [generar_enemigo() for _ in range(num)]

def mostrar_texto(texto, tam, color, centro):
    font = pygame.font.SysFont(None, tam)
    render = font.render(texto, True, color)
    rect = render.get_rect(center=centro)
    pantalla.blit(render, rect)

def reiniciar():
    jugador = Bloque(ANCHO // 2, ALTO // 2, 30, COLOR_JUGADOR)
    enemigos = generar_enemigos(20)
    return jugador, enemigos



def menu_principal():
    circulos = []
    for _ in range(20):
        circulos.append(Bloque(
            random.randint(50, ANCHO - 50),
            random.randint(50, ALTO - 50),
            random.randint(20, 60),
            (random.randint(100,200), random.randint(100,200), random.randint(100,200)),
            random.uniform(0.5, 1.5)
        ))

    while True:
        clock.tick(FPS)
        pantalla.fill(COLOR_FONDO)
        
        # Detecta si se presiona ENTER para empezar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        for c in circulos:
            c.mover()
            c.dibujar(pantalla)

        mostrar_texto("CRECIMIENTO TOTAL", 60, (255, 255, 255), (ANCHO // 2, ALTO // 2 - 50))
        mostrar_texto("Presiona ENTER para jugar", 32, (200, 200, 200), (ANCHO // 2, ALTO // 2 + 40))

        pygame.display.flip()



def main():
    menu_principal()

    jugador, enemigos = reiniciar()
    game_over = False
    win = False
    TAM_GANAR = 250 # Tamaño necesario para ganar

    while True:
        clock.tick(FPS)
        pantalla.fill(COLOR_FONDO)
        
        # Teclas y salida del juego        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    jugador, enemigos = reiniciar()
                    game_over = False
                    win = False

        if game_over:
            jugador.dibujar(pantalla)
            for e in enemigos:
                e.dibujar(pantalla)
            mostrar_texto("¡PERDISTE!", 72, (255, 0, 0), (ANCHO // 2, ALTO // 2 - 40))
            mostrar_texto("Presiona R para reiniciar o ESC para salir", 36, (255, 255, 255), (ANCHO // 2, ALTO // 2 + 40))
            pygame.display.flip()
            continue

        if win:
            jugador.dibujar(pantalla)
            for e in enemigos:
                e.dibujar(pantalla)
            mostrar_texto("¡GANASTE!", 72, (0, 255, 0), (ANCHO // 2, ALTO // 2 - 40))
            mostrar_texto("Presiona R para reiniciar o ESC para salir", 36, (255, 255, 255), (ANCHO // 2, ALTO // 2 + 40))
            pygame.display.flip()
            continue
        
        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        vel_jugador = 5
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jugador.x -= vel_jugador
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jugador.x += vel_jugador
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jugador.y -= vel_jugador
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jugador.y += vel_jugador

        # Límites pantalla
        jugador.x = max(jugador.radius, min(jugador.x, ANCHO - jugador.radius))
        jugador.y = max(jugador.radius, min(jugador.y, ALTO - jugador.radius))
        
        # Mover enemigos
        for e in enemigos:
            e.mover()
            
        # Colisiones jugador-enemigo
        for e in enemigos[:]:
            if jugador.collides_with(e):
                if jugador.tam >= e.tam:
                    jugador.tam += max(1, int(e.tam * 0.15))
                    jugador.radius = jugador.tam // 2
                    enemigos.remove(e)
                    enemigos.append(generar_enemigo())

                    if jugador.tam >= TAM_GANAR:
                        win = True
                        break
                else:
                    game_over = True
                    break

        jugador.dibujar(pantalla)
        for e in enemigos:
            e.dibujar(pantalla)

        mostrar_texto(f"Diámetro: {jugador.tam}", 28, (255, 255, 255), (100, 30))
        mostrar_texto("Presiona R para reiniciar | ESC para salir", 20, (200, 200, 200), (ANCHO - 220, 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()
