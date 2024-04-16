
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

### 0. Lecture du Tableau de Contraintes : Menu principal
Le programme lit un tableau de contraintes à partir d'un fichier texte et stocke les informations en mémoire. Puis, un menu est affiché pour choisir une fonctionnalité à lancer sur le tableau de contraintes.

![Lecture du tableau de contraintes](https://cdn.discordapp.com/attachments/1222083642206060687/1229878743158489158/sequence_1.gif?ex=663148d6&is=661ed3d6&hm=e4135b787fb987a96f9e82b9ff23af729719b1f6d279df1ad27382bb1a3b2893&)

### 1. Affichage du Tableau de Contraintes
Le graphe mémorisé est généré sous forme de **tableau**, y compris les sommets fictifs 0 (α) et N+1 (ω).
De même, le graphe est affiché sous forme de triplets pour une meilleure compréhension.

![Tableau de contraintes](https://cdn.discordapp.com/attachments/1222083642206060687/1229881122352140338/Screenshot_1_1.png?ex=66314b0d&is=661ed60d&hm=49c0593b03a90ebd4d06c194372392a9207eedfebae8cce2d071c140221bf430&)
![Affichage par triplets](https://cdn.discordapp.com/attachments/1222083642206060687/1229881589522104400/Screenshot_2_1.png?ex=66314b7d&is=661ed67d&hm=b4801b4b0d9b88c26b05529f5c77b3627831df76d1048977efde03078b913d18&)

### 2. Affichage Matriciel
Le graphe mémorisé est généré sous forme **matricielle**, y compris les sommets fictifs 0 (α) et N+1 (ω).

![Affichage matriciel](https://cdn.discordapp.com/attachments/1222083642206060687/1229883670949662750/Screenshot_3.png?ex=66314d6d&is=661ed86d&hm=1955062260d09e6bd5ca3289814b1c8391fec56691d04f9b5f8ed68f1487c1d5&)

### 3.1 Vérification des Propriétés du Graphe
Le graphe est examiné pour s'assurer que toutes les valeurs d'arc sont positives et qu'il ne contient pas de circuit.

![Vérification arc négatif](https://cdn.discordapp.com/attachments/1222083642206060687/1229887060698071191/Screenshot_7.png?ex=66315095&is=661edb95&hm=106a00905844223bc3cf088b13b26b42f28ca35e998b45e748a069faf18714fe&)
_Vérification des arcs_


![Vérification des circuits](https://cdn.discordapp.com/attachments/1222083642206060687/1229884943111557230/Screenshot_5.png?ex=66314e9c&is=661ed99c&hm=7641dbe48174e401191f2ba27d8e84e5f47cb1447e0a6fafb6f9f162433c030c&)
_Vérification de la présence de circuit_


Si aucun arc à valeur négative n'a été trouvé et que le graphe ne comporte aucun circuit, alors une proposition de **calcul des calendriers** est lancée _(cf. 3.2)_ :

![Proposition du calcul des calendriers](https://cdn.discordapp.com/attachments/1222083642206060687/1229884943459418122/Screenshot_6.png?ex=66314e9c&is=661ed99c&hm=49456bdb5f476e45034870e8432cae655998f5fde0b1c3a351b741e8e9ae7d9a&)

### 3.2 Calcul des calendriers
Le graphe est examiné pour s'assurer qu'il ne contient pas de circuits et que toutes les valeurs d'arc sont non négatives.

![Calcul des rangs 1](https://cdn.discordapp.com/attachments/1222083642206060687/1229888804773695661/Screenshot_10.png?ex=66315235&is=661edd35&hm=ec4f02d70cd575e382361160b78fd99beb4a1deb82e66b8069a8010efc7c52f3&)
![Calcul des rangs 2](https://cdn.discordapp.com/attachments/1222083642206060687/1229888805075681340/Screenshot_11.png?ex=66315235&is=661edd35&hm=d4425e98e32cdf03eb745fd6ce6f66029988cba6458e26d1e1a7a3efdb5528f7&)


### 4. Calcul des Rangs
Les rangs de tous les sommets du graphe sont calculés pour préparer la planification des tâches.

![Calcul des rangs]()

### 5. Calendriers et Marges
Les calendriers au plus tôt et au plus tard sont déterminés, ainsi que les marges associées à chaque tâche.

![Calendriers et marges]()

### 6. Chemins Critiques
Les chemins critiques sont identifiés, marquant les séquences

### BONUS : afficher le graphe
