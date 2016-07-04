#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import time
import sqlite3
import datetime

BLANCO = (255, 255, 255)

class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen_asteroide
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()

    def update(self, aceleracion):
        # Desplazamos 10 píxel hacia la izquierda el asteroide.
        self.rect.x -= 10 + aceleracion
        # Si el asteroide se escapa del fondo de la pantalla.
        if self.rect.x < 0:
            # Lo movemos justo a la derecha del todo
            x = random.randrange(1400, 1500)
            self.rect.x = x
            # Le damos una nueva ubicación a y
            y = random.randrange(0, 600)
            self.rect.y = y

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen_nave
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.y = 100
        self.rect.x = 50

    def movimiento(self, y):
        self.rect.y += y
        # Limites de la nave para que no salga de la pantalla
        if self.rect.y > 548:
            self.rect.y = 547
        elif self.rect.y < 0:
            self.rect.y = 1

    def fin(self):
        self.image = imagen_explosion
        self.image.set_colorkey(BLANCO)
        sonido.play()
        pantalla.blit(texto1, (600,200))
        return True
 
pygame.init()

# Asigna el tamaño de la pantalla y la crea
tamaño = [1500, 600]
pantalla = pygame.display.set_mode(tamaño)
pygame.display.set_caption("La Nave Loca")

# Asigna las imagenes a las variables
imagen_fondo = pygame.image.load("imagen_fondo.jpg").convert()
imagen_nave = pygame.image.load("nave.png").convert()
imagen_asteroide = pygame.image.load("astroid.png").convert()
imagen_explosion = pygame.image.load("1.png").convert()

# Asigna el audio a la variable
sonido = pygame.mixer.Sound("atari_boom.ogg")

# Crea la imagen del texto "Perdiste"
fuente = pygame.font.Font(None, 100)
texto1 = fuente.render("Perdiste!", 0, (BLANCO))

asteroide_lista = pygame.sprite.Group()
lista_todos_los_sprites = pygame.sprite.Group()

for i in range(9):
    # Esto representa un asteroide
    asteroide = Asteroide() 

    # Establece una ubicación aleatoria para el asteroide
    asteroide.rect.x = random.randrange(1400, 1500)
    asteroide.rect.y = random.randrange(0, 600)
 
    # Añade el asteroide a la lista de objetos
    asteroide_lista.add(asteroide)
    lista_todos_los_sprites.add(asteroide)

nave = Nave()
lista_todos_los_sprites.add(nave)

aceleracion = 1
puntos_jugador = 0
contador = 0

# Se usa para gestionar cuan rápido se actualiza la pantalla
reloj = pygame.time.Clock()

# Lo hace hasta que el usuario pincha sobre el botón de cierre.
hecho = False

# -------- Bucle Principal del Programa -----------
while not hecho:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
    
    # Pone la imagen de fondo
    pantalla.blit(imagen_fondo, (0, 0))

    # Puntos
    contador += 1
    if contador == 60:
        puntos_jugador += 1
        contador = 0
        aceleracion += 0.3
        
    # Crea la imagen del texto "Puntos"   
    fuente2 = pygame.font.Font(None, 70)
    puntos_texto = "Puntos: {}".format(puntos_jugador)
    texto2 = fuente2.render(puntos_texto, 0, (BLANCO))
    pantalla.blit(texto2, (0, 0))
    
    # Controla las teclas
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_UP:
            nave.movimiento(-5)
        if evento.key == pygame.K_DOWN:
            nave.movimiento(5)

    if evento.type == pygame.KEYUP:
        if evento.key == pygame.K_UP:
            nave.movimiento(0)
        if evento.key == pygame.K_DOWN:
            nave.movimiento(0)
        
    # Colision entre la nave y los asteroides
    lista_impactos_asteroides = pygame.sprite.spritecollide(nave, asteroide_lista, False)

    if lista_impactos_asteroides != []:
        hecho = nave.fin()

    lista_todos_los_sprites.draw(pantalla)

    asteroide_lista.update(aceleracion)
    # Limitación de 60 fotogramas por segundo
    reloj.tick(60)

    # Actualiza la pantalla
    pygame.display.flip()

time.sleep(2) 
pygame.quit()

nombre_jugador = input("Ingrese su nombre: ")

fecha_hoy = datetime.datetime.now()

# ------------Base de datos de los puntos------------
connection = sqlite3.connect("Puntos.db")
cursor = connection.cursor()

# Crea la tabla
sql_command = """ CREATE TABLE IF NOT EXISTS tabla (
numero INTEGER PRIMARY KEY,
nombre VARCHAR(10),
puntos INTEGER,
fecha DATETIME);"""
cursor.execute(sql_command)

# Ingresa los datos
sql_command = """ INSERT INTO tabla (numero,nombre,puntos,fecha)
VALUES (NULL,?,?,?);"""
cursor.execute(sql_command,(nombre_jugador,puntos_jugador,fecha_hoy))

# Ordena la tabla de mayor a menor y los muestra
sql_command = "SELECT * FROM tabla ORDER BY puntos DESC;"
cursor.execute(sql_command)

data = cursor.fetchall()

print("\n\n\t\t\t\t  TOP TEN\n")
print("\t\t    Nombre\t  Puntos\tFecha y Hora\n")

holaaa = 0

for row in data:
    if holaaa < 10:
        dnombre = row[1]
        dpuntos = row[2]
        dfecha = row[3]
        print("\t\t%10s \t   %3d \t  %s" % (dnombre, dpuntos, dfecha))
        holaaa += 1

connection.commit()
connection.close()
