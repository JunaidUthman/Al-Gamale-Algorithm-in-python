# Paramètres cryptographiques de l'exemple (codés en dur)
# -------------------------------------------------------------
# p est un nombre premier, m est un générateur, a est la clé privée
p = 65537
m = 2
a = 23
# La clé publique n est calculée : n = (m^a) mod p
n = pow(m, a, p) # 65409
