
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
## 🎥 Démonstration

Chaque étape du processus d'ordonnancement est illustrée ci-dessous avec un GIF démonstratif :

### 1. Lecture du Tableau de Contraintes
Le programme lit un tableau de contraintes à partir d'un fichier texte et stocke les informations en mémoire. Puis, un menu vous est affiché pour choisir une fonctionnalité à lancer sur le tableau de contraintes.

![Lecture du tableau de contraintes](https://cdn.discordapp.com/attachments/422113586597593088/1227008840558579772/1.gif?ex=6626d808&is=66146308&hm=4b057e8718f16bd996d203401e4cb5229973476afca0db0cce7a25f09219b090&)

### 2. Affichage Matriciel
Un graphe est généré sous forme matricielle, y compris les sommets fictifs alpha (α) et omega (ω).

![Affichage matriciel](lien_vers_le_gif_affichage_matriciel.gif)

### 3. Vérification des Propriétés du Graphe
Le graphe est examiné pour s'assurer qu'il ne contient pas de circuits et que toutes les valeurs d'arc sont non négatives.

![Vérification des propriétés](lien_vers_le_gif_verification_proprietes.gif)

### 4. Calcul des Rangs
Les rangs de tous les sommets du graphe sont calculés pour préparer la planification des tâches.

![Calcul des rangs](lien_vers_le_gif_calcul_rangs.gif)

### 5. Calendriers et Marges
Les calendriers au plus tôt et au plus tard sont déterminés, ainsi que les marges associées à chaque tâche.

![Calendriers et marges](lien_vers_le_gif_calendriers_marges.gif)

### 6. Chemins Critiques
Les chemins critiques sont identifiés, marquant les séquences

### BONUS : afficher le graphe
