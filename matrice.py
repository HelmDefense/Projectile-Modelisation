from math import cos, sin, radians

import numpy as np


def scaling(sx, sy=None):
	"""
	Génère une matrice de mise à l'échelle.

	:param float sx: Le facteur de mise à l'échelle des X
	:param float sy: Le facteur de mise à l'échelle des Y
	:return: La matrice de mise à l'échelle
	"""
	if sy is None:
		return scaling(sx, sx)
	return np.array([[sx, 0], [0, sy]])


def rotation(theta, deg=False):
	"""
	Génère une matrice de rotation.

	:param float theta: L'angle de rotation
	:param bool deg: Si la valeur de l'angle est en degré
	:return: La matrice de rotation
	"""
	if deg:
		theta = radians(theta)
	cos_theta = cos(theta)
	sin_theta = sin(theta)
	return np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])


def reflection():
	"""
	Génère une matrice de réflexion selon l'axe des abscisses.

	:return: La matrice de symétrie
	"""
	return np.array([[1, 0], [0, -1]])


def multiply(*matrices, base=None):
	"""
	Multiplie les matrices reçues en partant de la matrice base.

	:param matrices: Les matrices à multiplier
	:param base: La base du calcul
	:return: La matrice résultat
	"""
	if base is None:
		base = np.identity(2)
	for matrice in matrices:
		base = np.dot(matrice, base)
	return base
