import random

# -------------------------------------------------------------
# Paramètres cryptographiques de l'exemple (codés en dur)
# -------------------------------------------------------------
# p est un nombre premier, m est un générateur, a est la clé privée
p = 65537
m = 2
a = 23
# La clé publique n est calculée : n = (m^a) mod p
n = pow(m, a, p) # 65409

def encode_bloc(texte):
    """
    Découpe le message en blocs de 2 caractères maximum et encode chaque bloc en un entier.
    La formule : x = ASCII_1 * 256^1 + ASCII_2 * 256^0
    """
    blocs = []
    # Parcourt le texte par pas de 2 caractères
    for i in range(0, len(texte), 2):
        bloc_texte = texte[i:i+2]
        
        # On définit les caractères ASCII
        # S'il n'y a qu'un seul caractère (fin de chaîne impaire), on pad avec 0
        ascii_1 = ord(bloc_texte[0])
        ascii_2 = ord(bloc_texte[1]) if len(bloc_texte) > 1 else 0
        
        # Encodage du bloc en un seul entier x
        x = ascii_1 * (256 ** 1) + ascii_2 * (256 ** 0)
        blocs.append(x)
        
    return blocs

def decode_bloc(blocs):
    """
    Prend une liste d'entiers x et la décode pour retrouver la chaîne de texte d'origine.
    On inverse la formule : ASCII_1 = x // 256 et ASCII_2 = x % 256
    """
    message_decode = ""
    for x in blocs:
        ascii_1 = x // 256
        ascii_2 = x % 256
        
        # On ajoute le premier caractère
        message_decode += chr(ascii_1)
        # On ajoute le deuxième caractère s'il ne vaut pas 0 (ce qui arrive en cas de padding final)
        if ascii_2 != 0:
            message_decode += chr(ascii_2)
            
    return message_decode

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

def main():
    # Affichage de présentation minimaliste
    print("--- Implémentation Minimale ElGamal ---")
    
    # 1. Minimum d'entrées : On demande uniquement le message à chiffrer
    message = input("Entrez le message à chiffrer : ")
    
    # 2. Chiffrement (les clés sont déjà générées en arrière-plan)
    message_chiffre = chiffrer(message)
    
    # 3. Affichage du message chiffré (les couples y1, y2)
    print("\n[+] Message chiffré (couples de y1, y2) :")
    for i, couple in enumerate(message_chiffre):
        print(f"  Bloc {i+1} : {couple}")
        
    # 4. Déchiffrement automatique pour prouver que l'algorithme fonctionne
    message_dechiffre = dechiffrer(message_chiffre)
    
    print(f"\n[+] Message déchiffré d'origine : {message_dechiffre}")
    print("---------------------------------------")

if __name__ == "__main__":
    main()
