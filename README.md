
# 🧮 L3 Projet : Théorie des Graphes

Projet de Théorie des Graphes de 3ème année à l'EFREI Paris du groupe B3.


## 🖊️ Auteurs 

- [Amna Boulouha](https://github.com/blhmna)
- [Kevin Kurtz](https://github.com/ktzkvin)
- [Romane Segui](https://github.com/Airseg)
- [Salomé Clavière](https://github.com/salobinks)
	

## 💾 Installation 

Toutes commandes à suivre sont à exécuter dans le terminal de votre IDE.

### Installation :
#### Clôner le depôt github :
```bash
    git clone https://github.com/ktzkvin/GraphProjectL3.git
```

#### Naviguer dans le répertoire `GraphProjectL3` :
```bash
    cd GraphProjectL3
```

#### Installer les dépendances nécessaires :
```bash
    pip install -r requirements.txt
```

#### Pour lancer l'application, exécuter la commande suivante :
```bash
    python B3_main.py
```

Ou bien exécuter le fichier B3_main.py à l'aide de votre IDE.
## 🛠️ Fonctionnalités

Chaque étape du processus d'ordonnancement est illustrée ci-dessous avec un GIF démonstratif :

### 1. Lecture du Tableau de Contraintes
Le programme lit un tableau de contraintes à partir d'un fichier texte et stocke les informations en mémoire. Puis, un menu vous est affiché pour choisir une fonctionnalité à lancer sur le tableau de contraintes.

![Lecture du tableau de contraintes](https://cdn.discordapp.com/attachments/1222083642206060687/1229878743158489158/sequence_1.gif?ex=663148d6&is=661ed3d6&hm=e4135b787fb987a96f9e82b9ff23af729719b1f6d279df1ad27382bb1a3b2893&)

### 2. Affichage Matriciel
Un graphe est généré sous forme matricielle, y compris les sommets fictifs alpha (α) et omega (ω).

![Affichage matriciel](https://cdn.discordapp.com/attachments/1222083642206060687/1229880422238916829/Screenshot_1.png?ex=66314a66&is=661ed566&hm=37c0d8d2b8284b0554a057b110aa12847b8f20f537b83edfe9c23bbea196c765&)
![Affichage matriciel](https://cdn.discordapp.com/attachments/1222083642206060687/1229879404013031454/Screenshot_2.png?ex=66314973&is=661ed473&hm=554beeba2693966ce8d54c906e9747ec994007cc13559287ede519070f91b22d&)


### 3. Vérification des Propriétés du Graphe
Le graphe est examiné pour s'assurer qu'il ne contient pas de circuits et que toutes les valeurs d'arc sont non négatives.

![Vérification des propriétés](https://cdn.discordapp.com/attachments/422113586597593088/1227010856659849308/1_1.gif?ex=6626d9e8&is=661464e8&hm=9c90b80ddf6b784c84e14d747c582b2dc374fbbc53c0cb0e7d93f6fb134c9b61&)

### 4. Calcul des Rangs
Les rangs de tous les sommets du graphe sont calculés pour préparer la planification des tâches.

![Calcul des rangs](https://cdn.discordapp.com/attachments/422113586597593088/1227010856659849308/1_1.gif?ex=6626d9e8&is=661464e8&hm=9c90b80ddf6b784c84e14d747c582b2dc374fbbc53c0cb0e7d93f6fb134c9b61&)

### 5. Calendriers et Marges
Les calendriers au plus tôt et au plus tard sont déterminés, ainsi que les marges associées à chaque tâche.

![Calendriers et marges](https://cdn.discordapp.com/attachments/422113586597593088/1227010856659849308/1_1.gif?ex=6626d9e8&is=661464e8&hm=9c90b80ddf6b784c84e14d747c582b2dc374fbbc53c0cb0e7d93f6fb134c9b61&)

### 6. Chemins Critiques
Les chemins critiques sont identifiés, marquant les séquences

### BONUS : afficher le graphe
