# Implémentation de l'Algorithme d'ElGamal en Python

## 🎯 Objectif du Projet
Ce projet fournit une implémentation **minimale, pédagogique et modulaire** de l'algorithme de cryptographie asymétrique **ElGamal**. L'algorithme repose mathématiquement sur la complexité et la difficulté de calcul du problème du logarithme discret. 

L'objectif final de ce code est de :
1. Démontrer le fonctionnement d'un découpage de message texte en blocs de taille fixe afin de les encoder sous forme d'entiers mathématiques de taille gérable.
2. Chiffrer ces entiers un à un à l'aide des paramètres de base d'ElGamal pour générer des cryptogrammes sous forme de couples mathématiques.
3. Déchiffrer ces cryptogrammes automatiquement en utilisant une clé privée mathématique pour retrouver la chaîne d'origine, prouvant ainsi la validité du concept (Proof of Concept).
4. Rendre ces étapes ultra-claires et lisibles pour faciliter l'apprentissage en répartissant la logique complète au sein de plusieurs modules spécialisés.

---

## 📂 Architecture des Fichiers
- **`config.py`** : Définit les paramètres cryptographiques et les clés du sysème (clés publique et privée).
- **`encoding.py`** : Gère la conversion du texte classique en entiers numériques structurés via un système d'encodage par bloc.
- **`crypto.py`** : Contient le cœur mathématique d'ElGamal incluant l'intégralité de la logique de chiffrement et de déchiffrement.
- **`elgamal.py`** : Point d'entrée principal de l'application permettant de gérer l'interaction avec l'utilisateur via le terminal.

---

## 🔍 Explication Détaillée des Méthodes et Modules

### 1. Module `config.py` (Paramètres Cryptographiques)
Ce module initialise l'environnement mathématique en constantes fixes (codé "en dur") pour les besoins de notre démonstration de cours.
* **`p = 65537`** : Un nombre premier qui sert de module pour toutes les opérations. Absolument tous les calculs finaux s'effectuent dans le groupe modulo $p$.
* **`m = 2`** : Un générateur (aussi appelé racine primitive modulo $p$).
* **`a = 23`** : **La clé privée** de l'utilisateur. Seul celui qui déchiffre connaît cette valeur (elle doit rester strictement secrète).
* **`n = pow(m, a, p)`** : Il s'agit de la fameuse **clé publique**, générée mathématiquement conjointement depuis la formule $n = m^a \pmod p$. Dans la réalité, la clé publique globale et communiquée au monde sans aucune restriction est le trio $(p, m, n)$.

### 2. Module `encoding.py` (Manipulation et Conversion de Données)

#### > `encode_bloc(texte)`
* **Objectif** : Transformer les caractères alphabétiques de la chaîne de texte en valeurs entières compactes (qui sont strictement inférieures au modulo $p=65537$) pour pouvoir effectuer nos opérations arithmétiques.
* **Logique détaillée en profondeur** :
  1. On navigue sur la chaîne de caractères (le `texte`) avec un pas de saut de 2 pour la découper en **blocs de 2 caractères limités**.
  2. Pour le bloc courant, on convertit chaque valeur numérique dans sa correspondance de table ASCII standard en invoquant la fonction native `ord()`.
  3. *Note sur la contrainte de taille ("Padding")* : Si le texte originel est de taille globale impaire, le tout dernier bloc ne possédera mathématiquement qu'une seule lettre. Dans ce cas, la méthode comble le vide en positionnant une valeur arbitraire forcée à $0$ en guise de 2ème caractère de bourrage (padding).
  4. L'opération clé : On fusionne nos 2 caractères textuels en 1 nouvel et unique condensé entier (qu'on nomera $x$) via une formule de compression de format binaire : 
     $x = \text{ASCII\_1} \times 256^1 + \text{ASCII\_2} \times 256^0$. 
     Étant donné que la table ASCII ne va que jusqu'à $255$, la fusion garantit très exactement un nombre qui ira de 0 à un maximum strict de 65535, ce qui a l'avantage de "toujours rentrer" parfaitement avant le dépassement du module $p$ plafonné à 65537.
  5. Ce formatage $x$ calculé pour chaque duo de caractères est inséré dans un tableau liste et renvoyé pour être sécurisé.

#### > `decode_bloc(blocs)`
* **Objectif** : Mécanisme rigoureusement inverse. Il transforme les entiers mathématiques déchiffrés et récupérés durant le processus pour re-former les véritables mots humainement lisibles.
* **Logique détaillée en profondeur** : 
  1. À partir de notre bloc compressé déchiffré $x$, on est en mesure d'isoler les deux caractères d'origine en usant de la division euclidienne basique base-256.
  2. Le `Premier Caractère` sera récupéré grâce au quotient exact de la division : $(x // 256)$.
  3. Le `Deuxième Caractère` sera récupéré via le reste exclusif de cette division modulo 256 : $(x \pmod{256})$.
  4. Les nombres abstraits sont finalement reconvertis et concaténés à la chaîne via la méthode Python string ASCII `chr()`. En gardant en tête la contrainte d'un éventuel blocage précédent : si jamais la variable du 2ème caractère vaut numériquement $0$, l'algorithme "sait" qu'il s'agit du padding de bourrage artificiel, il ignorera purement cet octet inutile et n'ajoutera qu'un unique caractère final.

### 3. Module `crypto.py` (La Magie Sécuritaire - Le Cœur ElGamal)

#### > `chiffrer(message)`
* **Objectif** : Protéger le message en convertissant ses entiers en mystérieux cryptogrammes illisibles pour quiconque ignorerait la clé privée.
* **Logique détaillée en profondeur** :
  1. Le texte classique est envoyé en tant que paramètre puis basculé vers notre liste structurelle d'entiers via : `encode_bloc(texte)`.
  2. La boucle forcé s'attarde sur chaque paquet d'entier compressé $x$.
  3.  Le point fort asymétrique de l'Algorithme : l'introduction d'un "aléa protecteur". On sélectionne avec le module Random Python un nombre éphémère $k$, choisi arbitrairement dans l'intervalle $1 \le k \le p-1$. Ce nombre (ou "nonce") amène une imprévisibilité d'état et assure fermement qu'encoder le simple mot "Hello" dix fois d'affilée offrira en finalité dix cryptogrammes entièrement différents et sans similitude visuelle apparente.
  4. Étape de l'indice partagé : on génère $y_1$ via la formule $y_1 = m^k \pmod{p}$.
  5. Etape du masquage de l'entier : on génère le message encrypté $y_2$ à l'aide de notre clé originelle publique (n) et de notre message bloc secret $x$ via $y_2 = x \times n^k \pmod{p}$.
  6. Le programme retourne la liste compilée de tous ces duos indéchiffrables $[(y_1, y_2)]$.

#### > `dechiffrer(blocs_chiffres)`
* **Objectif** : Simuler la réception finale. Fort des deux variables des cryptogrammes de forme $(y_1, y_2)$ transmis (qui sont théoriquement publiques mais illisibles) et de la fameuse clé unique et privée secrète de résolution $a$. On casse l'équation mathématique.
* **Logique détaillée en profondeur** :
  1. La théorie d'ElGamal indique que ré-obtenir notre message secret originel (connu sous le variable $x$) s'effectue via l'opération complexe mais formelle suivante : $x = y_1^{p - 1 - a} \times y_2 \pmod p$.
  2. **Remarque technique d'optimisation indispensable :** Le calcul itératif de nombres exposés à de très grandes puissances coûte extrêmement cher (paralysant voire plantant le CPU) en calcul informatique basique. Plutôt que de compiler inutilement une variable gigantesque du type $(y_1)^{(p - 1 - a)}$ de manière standard pour la tronquer ensuite, ce qui crasherait Python à cause de la saturation mémoire d'un si gros entier; l'algorithme est subtilement contraint à faire appel à la formule fonctionnelle native de Python : `pow(y1, p - 1 - a, p)`. Cette intégration native embarque un code compilé en C utilisant l'**Exponentiation modulaire rapide** qui maintient les entiers bas et courts en permanence avant chaque élévation à la puissance.
  3. L'entier magique $x$ désormais redevenu lisible est stocké en mémoire puis passé de nouveau vers le `decode_bloc` qui remet à nu en console les tous premiers lettres du créateur originel !

### 4. Module `elgamal.py` (Script Principal Executif)
#### > `main()`
* **Objectif** : Orchestrer l'ensemble des modules séparés du projet et donner de la vie de façon minimaliste à l'interface affichée de terminal.
* **Logique détaillée en profondeur** :
  1. On déclenche une instruction interactive `input()` dans la console bash pour saisir dynamiquement la demande (Message en clair).
  2. Le script appelle silencieusement la nouvelle architecture modulaire `chiffrer(message)`.
  3. Le cryptogramme public complexe s'affiche joliment pour prouver les opérations mathématiques effectuées bloc par bloc dans la console sans rien cacher.
  4. Finalement, `dechiffrer(message)` intervient avec élégance non-interactive afin d'accomplir le Proof of Concept. Il donne ainsi de réelles assurances en confirmant, prouvant et imprimant que le cycle est rigoureusement exact puisque le texte est réapparu au terminal, démontrant la puissance, l'autonomie formelle, et la perfection mathématique d'ElGamal modulaire en pleine action.

---

## 🚀 Comment Exécuter l'Implémentation ?
En ligne de commande, placez-vous strictement à la base du projet de votre dossier, puis lancez le programme avec la syntaxe console python :
```bash
python elgamal.py
```
