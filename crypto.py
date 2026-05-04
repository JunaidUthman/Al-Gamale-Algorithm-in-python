import random
from config import p, m, a, n
from encoding import encode_bloc, decode_bloc

def chiffrer(message):
    """
    Chiffre une chaîne de caractères bloc par bloc selon l'algorithme ElGamal.
    """
    blocs = encode_bloc(message)
    blocs_chiffres = []
    
    for x in blocs:
        # 1. Choisir k aléatoire tel que 1 <= k <= p - 1
        k = random.randint(1, p - 1)
        
        # 2. Calculer y1 = (m^k) mod p
        y1 = pow(m, k, p)
        
        # 3. Calculer y2 = (x * (n^k)) mod p
        y2 = (x * pow(n, k, p)) % p
        
        blocs_chiffres.append((y1, y2))
        
    return blocs_chiffres

def dechiffrer(blocs_chiffres):
    """
    Déchiffre une liste de couples (y1, y2) bloc par bloc selon l'algorithme ElGamal.
    """
    blocs_dechiffres = []
    
    for y1, y2 in blocs_chiffres:
        # Pour retrouver x : x = (y1^(p - 1 - a) * y2) mod p
        # pow(y1, p - 1 - a, p) utilise l'exponentiation modulaire optimisée
        x = (pow(y1, p - 1 - a, p) * y2) % p
        blocs_dechiffres.append(x)
        
    return decode_bloc(blocs_dechiffres)
