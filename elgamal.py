from crypto import chiffrer, dechiffrer

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
