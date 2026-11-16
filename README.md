# 🎮 Proyecto Pygame - Juego de Supervivencia 2D

Juego de supervivencia en 2D hecho con **Python** y **Pygame** en el que dos jugadores deben esquivar obstáculos que caen desde la parte superior de la pantalla. Incluye 9 retos implementados: límites de pantalla, obstáculos aleatorios, colisiones, pausa, reinicio, cronómetro, dificultad progresiva, cambio de velocidad y récord de puntuación.

https://github.com/javiierr2007/pygame-javier/blob/main/demostraci%C3%B3n_juego.mp4

## ▶️ Cómo ejecutar el juego

python game.py

## 🕹️ Controles

| Acción | Jugador 1 (Azul) | Jugador 2 (Verde) |
| Mover arriba | Flecha arriba | `W` |
| Mover abajo | Flecha abajo | `S` |
| Mover izquierda | Flecha izquierda | `A` |
| Mover derecha | Flecha derecha | `D` |

| Acción general | Tecla |
| Pausar / Reanudar | `ESC` |
| Reiniciar (en Game Over) | `R` |
| Subir velocidad del Jugador 1 | `M` |
| Bajar velocidad del Jugador 1 | `N` |

## 📖 Explicación completa del código

### 1. Importaciones

- `import pygame`: Nos da todas las herramientas para crear ventanas, dibujar gráficos, detectar teclas, reproducir sonidos, etc.
- `import random`: Para poder generar números aleatorios.

### 2. Inicialización de Pygame

- `pygame.init()`: Arranca todos los módulos internos de Pygame. Es obligatorio llamarlo antes de usar cualquier función de Pygame. Sin esta línea, nada funcionaría.

### 3. Configuración de pantalla

- `SCREEN_WIDTH = 800` y `SCREEN_HEIGHT = 600`: Definimos el ancho y alto de la ventana del juego en píxeles. Usamos nombres en mayúsculas porque son constantes.
- `pygame.display.set_mode((800, 600))`: Crea la ventana del juego con las dimensiones indicadas. La variable screen es donde dibujaremos todo.
- `pygame.display.set_caption(...)`: Pone el título que aparece en la barra superior de la ventana.

### 4. Definición de colores

| Variable | Color | Valores RGB | Se usa para |
| `WHITE` | Blanco | (255, 255, 255) | Fondo de la pantalla |
| `BLACK` | Negro | (0, 0, 0) | Texto de puntuación y tiempo |
| `RED` | Rojo | (255, 0, 0) | Obstáculos y texto de Game Over/Pausa |
| `BLUE` | Azul | (0, 0, 255) | Jugador 1 y texto de su velocidad |
| `GREEN` | Verde | (0, 255, 0) | Jugador 2 |

### 5. Fuente y reloj

- `pygame.font.SysFont(None, 36)`: Crea un objeto de fuente para escribir texto en pantalla. None significa que usa la fuente por defecto del sistema. 36 es el tamaño en píxeles.
- `pygame.time.Clock()`: Crea un reloj que usaremos para controlar la velocidad del juego (los FPS, fotogramas por segundo). Sin esto, el juego iría demasiado rápido o diferente según el ordenador.

### 6. Clase Player (Jugador)

- `class Player(pygame.sprite.Sprite)`: Creamos la clase Player que hereda de Sprite. Esto nos permite usar funciones automáticas de Pygame como .draw(), .update(), detección de colisiones, etc.
- `def __init__(self, x, y, color)`: Es el constructor, la función que se ejecuta automáticamente al crear un jugador. Recibe la posición inicial (x, y) y el color.
- `super().__init__()`: Llama al constructor de la clase padre (Sprite) para que se inicialice correctamente.
- `self.image = pygame.Surface((40, 40))`: Crea un cuadrado de 40×40 píxeles como la "imagen" del jugador.
- self.image.fill(color): Rellena ese cuadrado con el color que le pasamos.
- `self.rect = self.image.get_rect()`: Obtiene el rectángulo que rodea la imagen. Este rectángulo es lo que Pygame usa para posicionar al jugador y detectar colisiones.
- `self.rect.x = x` y `self.rect.y = y`: Colocamos el rectángulo en la posición inicial.
- `self.speed = 5`: La velocidad de movimiento del jugador.

#### Método `update` del jugador:

- `keys`: Es un diccionario con todas las teclas del teclado. Si una tecla está pulsada, su valor es True.
- `Movimiento`: Si la tecla de la izquierda está pulsada, restamos speed a la posición X (se mueve a la izquierda). Si es la derecha, sumamos. Arriba resta Y, abajo suma Y. (En Pygame, el eje Y va de arriba a abajo: Y=0 es arriba, Y=600 es abajo.)
- `Límites (RETO 1)`: Después de mover, comprobamos que el jugador no se haya salido de la pantalla. Si se sale por la izquierda (left < 0), lo ponemos en el borde izquierdo. Y así con los cuatro lados.

### 7. Clase Obstacle (Obstáculo)

- `size = random.randint(20, 70)` (RETO 2): Genera un tamaño aleatorio entre 20 y 70 píxeles. Cada obstáculo será de un tamaño diferente.
- `self.image = pygame.Surface((size, size))`: Crea un cuadrado rojo del tamaño aleatorio.
- `self.rect.x = random.randint(0, SCREEN_WIDTH - size)`: Posición horizontal aleatoria. Restamos size al ancho para que nunca aparezca cortado por el borde derecho.
- `self.rect.y = -size`: Empieza justo encima de la pantalla (posición negativa), para que parezca que "entra" cayendo.
- `self.speed_y = random.randint(3, 7)`: Velocidad de caída aleatoria entre 3 y 7 píxeles por fotograma.

#### Método `update` del obstáculo:

- `self.rect.y += self.speed_y`: Mueve el obstáculo hacia abajo sumando su velocidad a la posición Y.
- `self.kill()`: Si el obstáculo ha salido completamente por debajo de la pantalla, se elimina del juego. Esto es importante para no gastar memoria con obstáculos invisibles.

### 8. Variables del juego

- `player1` y `player2`: Creamos los dos jugadores. El Jugador 1 es azul y empieza en (300, 500). El Jugador 2 es verde y empieza en (500, 500).
- `all_sprites`: Es un grupo de sprites. Un grupo permite dibujar y actualizar muchos objetos a la vez con una sola línea. Metemos ambos jugadores aquí.
- `obstacles`: Otro grupo, solo para los obstáculos. Lo usamos para detectar colisiones.
- `SPAWN_OBSTACLE = pygame.USEREVENT + 1`: Creamos un evento personalizado. Pygame tiene eventos como "tecla pulsada" o "ratón movido", pero aquí inventamos el nuestro: un evento que se dispara periódicamente para crear obstáculos.
- `obstacle_spawn_time = 1000`: Cada 1000 milisegundos (1 segundo) aparece un obstáculo nuevo.
- `pygame.time.set_timer(SPAWN_OBSTACLE, 1000)`: Le decimos a Pygame que dispare el evento SPAWN_OBSTACLE cada 1000 ms.
- `score = 0`: Puntuación actual (cuenta cuántos obstáculos han aparecido).
- `high_score = 0`(RETO 9): Récord de puntuación. Se mantiene aunque reinicies la partida.
- `start_ticks`: Guarda el momento exacto en que empezó la partida, para calcular el tiempo de supervivencia.
- `game_over = False`: Indica si el juego ha terminado (algún jugador fue golpeado).
- `paused = False`(RETO 4): Indica si el juego está en pausa.

### 9. Bucle principal del juego
#### 9.1 — Gestión de eventos
- `while running`: El bucle se repite mientras running sea True.
- `pygame.event.get()`: Recoge todos los eventos que han ocurrido desde el último fotograma.
- `pygame.QUIT`: Si el usuario cierra la ventana (clic en la X), ponemos running = False para salir del bucle.

#### 9.2 — Pausa con ESC (RETO 4)

- `pygame.KEYDOWN`: Se activa cuando el usuario pulsa una tecla (solo una vez, no continuamente).
- Si se pulsa `ESC`, alternamos el valor de `paused`: si estaba en pausa, la quitamos; si no estaba, la ponemos.

#### 9.3 — Reiniciar partida con R (RETO 5)
- Solo funciona si el juego ha terminado (game_over == True) y se pulsa la tecla R.
- Resetea todo: puntuación a 0, quita el game over, reinicia el cronómetro, elimina todos los obstáculos del grupo, pone a los jugadores en su posición inicial, restaura la velocidad del Jugador 1 a 5 y vuelve a poner el intervalo de spawn a 1 segundo.

#### 9.4 — Cambiar velocidad con M/N (RETO 8)

- `M` sube la velocidad del Jugador 1 en 1 (máximo 12).
- `N` baja la velocidad del Jugador 1 en 1 (mínimo 2).
- Solo funciona si el juego NO ha terminado.

#### 9.5 — Spawn de obstáculos y dificultad (RETO 7)
- Cada vez que se dispara el evento SPAWN_OBSTACLE, se crea un nuevo obstáculo y se suma 1 al score.
- Dificultad progresiva (RETO 7): Cada 10 puntos (score % 10 == 0), reducimos el tiempo entre obstáculos en 50 ms. Pero nunca baja de 150 ms para que no sea imposible.

#### 9.6 — Lógica del juego (movimiento, colisiones, cronómetro)

- `pygame.key.get_pressed()`: Devuelve un diccionario con el estado de todas las teclas. A diferencia de KEYDOWN (que se activa una vez), esto detecta si la tecla sigue pulsada, lo que permite movimiento continuo y fluido.
- `player1.update(...)`: Mueve al Jugador 1 según las flechas del teclado.
- `player2.update(...)`: Mueve al Jugador 2 según las teclas WASD.
- `obstacles.update()`: Mueve todos los obstáculos hacia abajo.
- Colisiones (RETO 3): Recorremos todos los obstáculos y comprobamos si el rectángulo de algún jugador se solapa con el de un obstáculo usando `colliderect()`. Si colisionan, el juego termina.
- Récord (RETO 9): Al terminar, si el score actual supera el récord, lo actualizamos.
- Cronómetro (RETO 6): Calculamos los segundos de supervivencia restando el tick actual menos el tick de inicio y dividiendo entre 1000 (de milisegundos a segundos). // es la división entera (sin decimales).

#### 9.7 — Dibujado en pantalla

- `screen.fill(WHITE)`: Borra todo lo anterior pintando la pantalla de blanco. Esto se hace cada fotograma para evitar que los dibujos anteriores se "acumulen".
- `all_sprites.draw(screen)`: Dibuja todos los sprites (jugadores y obstáculos) en la pantalla.
- En pausa**: Se dibujan los sprites (congelados) y se muestra el texto "PAUSE".
- `font.render(...)`: Convierte un texto en una imagen que se puede dibujar. El True activa el anti-aliasing (bordes suaves). El tercer parámetro es el color.
- `screen.blit(imagen, (x, y))`: "Pega" una imagen en la pantalla en las coordenadas indicadas. Así se muestran los textos.
- En Game Over**: Se muestra el mensaje "GAME OVER - Press 'R' to Restart" en rojo centrado en pantalla.
- `pygame.display.flip()`: Actualiza la pantalla. Todo lo que hemos dibujado con blit o draw no se ve hasta que llamamos a flip(). Pygame usa un sistema de doble búfer: dibujamos en un búfer invisible y luego lo mostramos de golpe.
- `clock.tick(60)`: Limita el juego a 60 FPS (fotogramas por segundo). Esto hace que el juego vaya a la misma velocidad en todos los ordenadores.

#### 9.8 — Cierre del juego

pygame.quit()

- Cuando salimos del bucle `while`, esta línea cierra Pygame correctamente y libera los recursos.