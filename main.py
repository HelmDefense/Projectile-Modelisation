import numpy as np
import matplotlib.pyplot as plt
from matrice import rotation, multiply


def draw_object(obj, style):
	x = obj[0, :]
	y = obj[1, :]
	plt.plot(x, y, style)


def draw_line(p1, p2, style):
	line = np.concatenate((p1, p2), 1)
	draw_object(line, style)


def draw_circle(x, y, r, c="b", ls="-"):
	axes.add_artist(plt.Circle((x, y), radius=r, fill=False, color=c, ls=ls))


# Génération aléatoire d'ennemis (cercles) autour du point de tir (0, 0)

axes = plt.gca()
plt.axis("scaled")
size = 35
plt.xlim(-size - 1, size + 1)
plt.ylim(-size - 1, size + 1)
axes.set_aspect(1)

nb_enemies = 35
size_enemy = 2

enemies = np.random.rand(2, nb_enemies) * 2 * size - size
protection = 15
i = 0
while i < nb_enemies:
	enemyX = enemies[0, i]
	enemyY = enemies[1, i]
	if -protection < enemyX < protection and -protection < enemyY < protection:
		enemies = np.delete(enemies, i, 1)
		nb_enemies -= 1
	else:
		i += 1

shooter = np.array([[6, 3, 0, -3, 0, 3, 6], [0, 0.75, 6, 0, -6, -0.75, 0]])
origin = np.array([[0], [0]])
start_orientation = np.array([[1], [0]])

shoot_angle = np.random.rand() * 2 * np.pi
shoot_rotation = rotation(shoot_angle)
shooter = multiply(shoot_rotation, base=shooter)
shoot_orientation = multiply(shoot_rotation, base=start_orientation)
draw_object(shooter, "g-")

# Représentation de la vision du tireur

shoot_vision = np.pi / 2
angle_reduction = (np.pi - shoot_vision) / 2
vectN1 = np.dot(rotation(-angle_reduction), shoot_orientation)
vectN2 = np.dot(rotation(angle_reduction), shoot_orientation)
dots1 = np.dot(vectN1.reshape(1, 2), enemies)
dots2 = np.dot(vectN2.reshape(1, 2), enemies)

draw_line(origin, origin + multiply(rotation(np.pi / 2), base=vectN1 * size), "k:")
draw_line(origin, origin + multiply(rotation(-np.pi / 2), base=vectN2 * size), "k:")

i = 0
while i < nb_enemies:
	enemyX = enemies[0, i]
	enemyY = enemies[1, i]
	if dots1[0, i] > 0 and dots2[0, i] > 0:
		draw_circle(enemyX, enemyY, size_enemy)
		i += 1
	else:
		draw_circle(enemyX, enemyY, size_enemy / 2, "r", ":")
		enemies = np.delete(enemies, i, 1)
		dots1 = np.delete(dots1, i, 1)
		dots2 = np.delete(dots2, i, 1)
		nb_enemies -= 1

# Détection de l'ennemi visible le plus proche

minI = -1
minDist = 2 * size ** 2 + 1
for i in range(nb_enemies):
	enemyX = enemies[0, i]
	enemyY = enemies[1, i]
	dist = enemyX ** 2 + enemyY ** 2
	if dist < minDist:
		minDist = dist
		minI = i

targetX = enemies[0, minI]
targetY = enemies[1, minI]
draw_circle(targetX, targetY, size_enemy * 1.5, "m", ":")

# Visualisation de la trajectoire du projectile principal

shoot = np.array([[targetX], [targetY]])
minDistSqrt = np.sqrt(minDist)
shoot_unit = shoot / minDistSqrt
shoot = shoot_unit * (minDistSqrt - size_enemy)
draw_line(origin, origin + shoot, "m:")

# TODO Calcul des trajectoires des projectiles secondaires et détermination des cibles potentielles

multishoot_angle = np.pi / 12
multishoot1 = multiply(rotation(multishoot_angle), base=shoot)
draw_line(origin, origin + multishoot1, "g:")
multishoot2 = multiply(rotation(-multishoot_angle), base=shoot)
draw_line(origin, origin + multishoot2, "g:")

# TODO Représentation du projectile à l'instant T

t = 0.5
projectile = np.array([
	[0, -1, -1, 0, -3, -4, -3, -4, -5, -4, -5, -4, -3, -4],
	[0, 1, -1, 0, 0, 1, 0, 0, 1, 0, -1, 0, 0, -1]
])

a = np.arccos(np.dot(shoot_unit.reshape(1, 2), start_orientation))
if np.dot(shoot_unit.reshape(1, 2), np.array([[0], [1]])) < 0:
	a = -a
projectile = multiply(rotation(a), base=projectile)
draw_object(projectile, "c-")

plt.show()
