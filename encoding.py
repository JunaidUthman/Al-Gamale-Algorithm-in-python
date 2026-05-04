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
