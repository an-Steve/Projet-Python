from ursina import Ursina
from ursina import *
from random import uniform
from random import uniform, choice
import math
import time

app = Ursina() ##Utilisation de ursina

##VARIABLE##
current_language = "fr"
is_dark_mode = True
dernier_lancement_boule_feu = 0
dernier_champignon = 0 
player = None
bowserjr = None
point_A = None
point_B = None
point_C = None
point_D = None
champignon = None  
pieces = []
carapaces = []
bananes = []
score_piece=0
selected_player = "Mario"  
is_first_person = False  # Commence par la vue classique
selected_map = 1
is_jumping = False  
velocity_y = 0  
space_press_count = 0  
last_press_time = 0  
ground_level = 1  
boost_time = 0  # Le temps depuis lequel le boost a commencé
boost_duration = 3  # Durée du boost en secondes
boules_de_feu = []
dernier_lancement_boule_feu = time.time()

##MUSQIUE##
musique_fond = Audio('voiture.wav',autoplay=True,volume=0.5)
sound_effect = Audio('carapace.wav', loop=False, autoplay=False)
sound_fire = Audio('fire.wav', loop=False, autoplay=False)
son_piece = Audio('piece.wav', loop=False, autoplay=False)
sound_explosion= Audio('explosion.wav', loop=False, autoplay=False)
son_acc= Audio('acceleration.mp3', loop=False, autoplay=False)

##TRADUCTIONS##
translations = {
    "fr": {
        "play": "Jouer",
        "settings": "Paramètres",
        "quit": "Quitter",
        "change_language": "Changer la langue",
        "select_map": "Sélectionner un lieu",
        "toggle_theme": "Mode sombre/Mode clair",
        "select_player": "Sélectionner un joueur",
        "back": "Retour",
        "random_character": "Personnage Aléatoire",
        "selected_character": "Personnage sélectionné :",
        "mushroom_kingdom": "Le royaume Champignon",
        "sarasaland": "Sarasaland",
        "comet_observatory": "Observatoire de la Comète",
        "bowser_castle": "Château de Bowser",
        "random_map": "Map Aléatoire",
        "game_over": "Game Over !",
        "defeated": "Bowser Jr vous a vaincu !",
        "coins_collected": "Pièces collectées: ",
        "time_elapsed": "Temps écoulé: ",
        "seconds": "secondes",
        "replay": "Rejouer",
        "quit": "Quitter",
        "project_by": "Projet réalisé par ",
        "student": " , étudiant en L3 ISEI à l'Université de Paris 8!",
        "game_over": "Game Over !",
        "defeated": "Bowser Jr vous a vaincu !",
        "coins_collected": "Pièces collectées: ",
        "time_elapsed": "Temps écoulé: ",
        "seconds": "secondes",
        "replay": "Rejouer",
        "quit": "Quitter",
        "project_by": "Projet réalisé par ",
        "student": " , étudiant en L3 ISEI à l'Université de Paris 8!",
        "well_played": "Bien Joué !",
        "bowser_defeated": "Vous avez tué Bowser Jr !",
        "move": "Se déplacer : flèche",
        "launch_shell": "Lancer des carapaces : espace",
        "special_attack": "Attaque spéciale : S",
        "camera_zoom_out": "Caméra (dézoom) : D",
        "camera_zoom_in": "Caméra (zoom) : B"
    },
    "en": {
        "play": "Play",
        "settings": "Settings",
        "quit": "Quit",
        "change_language": "Change Language",
        "select_map": "Select a map",
        "toggle_theme": "Dark/Light Mode",
        "select_player": "Select Player",
        "back": "Back",
        "random_character": "Random Character",
        "selected_character": "Selected Character:",
        "mushroom_kingdom": "Mushroom Kingdom",
        "sarasaland": "Sarasaland",
        "comet_observatory": "Comet Observatory",
        "bowser_castle": "Bowser's Castle",
        "random_map": " Random Map",
        "game_over": "Game Over!",
        "defeated": "Bowser Jr defeated you!",
        "coins_collected": "Coins collected: ",
        "time_elapsed": "Elapsed time: ",
        "seconds": "seconds",
        "replay": "Play Again",
        "quit": "Exit",
        "project_by": "Project made by ",
        "student": " , student in L3 ISEI at the University of Paris 8!",
        "game_over": "Game Over!",
        "defeated": "Bowser Jr defeated you!",
        "coins_collected": "Coins collected: ",
        "time_elapsed": "Elapsed time: ",
        "seconds": "seconds",
        "replay": "Play Again",
        "quit": "Exit",
        "project_by": "Project made by ",
        "student": " , student in L3 ISEI at the University of Paris 8!",
        "well_played": "Well Played!",
        "bowser_defeated": "You defeated Bowser Jr!",
        "move": "Move: Arrow keys",
        "launch_shell": "Launch shells: Space",
        "special_attack": "Special attack: S",
        "camera_zoom_out": "Camera (zoom out): D",
        "camera_zoom_in": "Camera (zoom in): B"
    }
}


##############  MENU PRINCIPALE ########################################
def afficher_menu_principal():
    scene.clear()
    musique_fond.play()

    current_time = time.strftime("%d/%m/%Y-%H:%M") #Affiche la date et l'heure
    Text(current_time, position=(0.1, 0.45), scale=1, color=color.white, origin=(0.5, 0.5))
    Text("Mario Kart", position=(0.1, 0.4), scale=2, color=color.red, origin=(0.5, 0.5))
    Text("Jeu d'arcade", position=(0.1, 0.35), scale=1.5, color=color.yellow, origin=(0.5, 0.5))

    image = Entity(model='quad', texture='fond.png', scale=(4, 4), position=(-5, 0))
    image_bowser = Entity(model='quad', texture='fond_bowserjr.png', scale=(4, 4), position=(5, 0))
    texture_toggle_image = True
    texture_toggle_bowser = True

    def changer_image_survol():
        nonlocal texture_toggle_image
        image.texture = 'fond.png' if texture_toggle_image else 'peachmoto.png'
        texture_toggle_image = not texture_toggle_image
        invoke(changer_image_survol, delay=3)

    def changer_image():
        nonlocal texture_toggle_bowser
        image_bowser.texture = 'fond_bowserjr.png' if texture_toggle_bowser else 'bowserboxe.png'
        texture_toggle_bowser = not texture_toggle_bowser
        invoke(changer_image, delay=3)

    changer_image_survol()
    changer_image()

    def ajouter_go(button):
        button.go_label_left = Text("-", position=(button.x - 0.25, button.y), scale=1, color=color.white)
        button.go_label_right = Text("-", position=(button.x + 0.22, button.y), scale=1, color=color.white)

    def retirer_go(button):
        if hasattr(button, 'go_label_left'):
            destroy(button.go_label_left)
        if hasattr(button, 'go_label_right'):
            destroy(button.go_label_right)

    boutons = [
        Button(text=translations[current_language]["play"], scale=(0.4, 0.1), position=(0, 0.2), color=color.green, on_click=lancer_interface),
        Button(text=translations[current_language]["settings"], scale=(0.4, 0.1), position=(0, 0), color=color.blue, on_click=afficher_parametres),
        Button(text=translations[current_language]["quit"], scale=(0.4, 0.1), position=(0, -0.2), color=color.red, on_click=quitter_application)
    ]

    for bouton in boutons:
        bouton.on_mouse_enter = lambda b=bouton: ajouter_go(b)
        bouton.on_mouse_exit = lambda b=bouton: retirer_go(b)

    t = translations[current_language]  
    Text(t["project_by"], position=(-0.50, -0.35), scale=1, color=color.white)
    Text("ANTON NELCON Steve", position=(-0.28, -0.35), scale=1, color=color.red, bold=True)
    Text(t["student"], position=(0, -0.35), scale=1, color=color.white)
    Text("LinkedIn:https://www.linkedin.com/in/ansteve", position=(-0.50, -0.45), scale=0.8, color=color.blue, underline=True)
    Text("Github: https://github.com/an-Steve", position=(0, -0.45), scale=0.8, color=color.blue, underline=True)


####################### FIN DU MENU PRINCIPALE ##############################
    
##################### PAGE DE PARAMETRE #########################

def afficher_parametres():
    global gombas
    scene.clear()
    gombas = Entity(model='quad', texture='gombas.png', scale=(4), position=(5, -2))

    Text("Mario Kart", position=(-0.10, 0.5), scale=2, color=color.red)

    def ajouter_go(button):
        button.go_label_left = Text("-", position=(button.x - 0.25, button.y), scale=1, color=color.white)
        button.go_label_right = Text("-", position=(button.x + 0.20, button.y), scale=1, color=color.white)

    def retirer_go(button):
        if hasattr(button, 'go_label_left'):
            destroy(button.go_label_left)
        if hasattr(button, 'go_label_right'):
            destroy(button.go_label_right)

    boutons = [
        Button(text=translations[current_language]["change_language"], scale=(0.4, 0.1), position=(0, 0.4), color=color.green, on_click=changer_la_langue),
        Button(text=translations[current_language]["toggle_theme"], scale=(0.4, 0.1), position=(0, 0.2), color=color.blue, on_click=toggle_theme),
        Button(text=translations[current_language]["select_player"], scale=(0.4, 0.1), position=(0, 0), color=color.yellow, on_click=afficher_selection_joueur),
        Button(text=translations[current_language]["select_map"], scale=(0.4, 0.1), position=(0, -0.2), color=color.orange, on_click=afficher_selection_map),
        Button(text=translations[current_language]["back"], scale=(0.4, 0.1), position=(0, -0.4), color=color.red, on_click=afficher_menu_principal)
    ]

    for bouton in boutons:
        bouton.on_mouse_enter = lambda b=bouton: ajouter_go(b)
        bouton.on_mouse_exit = lambda b=bouton: retirer_go(b)



# Fonction mode sombre/clair
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    if is_dark_mode:
        window.color = color.black
        Button.default_color = color.gray
        Button.default_text_color = color.white
    else:
        window.color = color.white
        Button.default_color = color.azure
        Button.default_text_color = color.black
    afficher_parametres()

# Fonction pour changer la langue
def changer_la_langue():
    global current_language
    current_language = "en" if current_language == "fr" else "fr"
    afficher_parametres()


# Fonction pour afficher l'écran de sélection de joueur
def afficher_selection_joueur():
    global selected_player ,lakitu
    scene.clear()

    lakitu= Entity(model='quad',texture='lakitu.png',  scale=(2),position=(5,2))

    Text(text=translations[current_language]["select_player"],position=(-0.1, 0.4),scale=1.5,color=color.white,background=True)
    texte_personnage = Text(text=translations[current_language]["selected_character"],position=(-0.7, 0.3),scale=1.2,color=color.white)

    # Dictionnaire des couleurs associées aux personnages
    couleurs_personnages = {
        "Mario": color.red,
        "Luigi": color.green,
        "Peach": color.pink,
        "Toad": color.blue,
        "Daisy": color.orange,
        "Harmonie": color.cyan
    }

    # Liste des noms des personnages
    personnages = list(couleurs_personnages.keys())

    # Fonction pour mettre à jour le texte du personnage survolé
    def mettre_a_jour_texte_survol(nom_personnage):
        if nom_personnage:
            texte_personnage.text = f"{translations[current_language]['selected_character']} {nom_personnage}"
            texte_personnage.color = couleurs_personnages[nom_personnage]  # Change la couleur du nom du personnage
        else:
            texte_personnage.text = translations[current_language]["selected_character"]
            texte_personnage.color = color.white

    # Boutons pour choisir les personnages avec événements de survol
    Button(scale=(0.2, 0.1), position=(-0.4, 0.1), color=color.red, icon='mario.png',
           on_click=lambda: choisir_personnage("Mario"),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol("Mario"),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    Button(scale=(0.2, 0.1), position=(0.0, 0.1), color=color.green, icon='luigi.png',
           on_click=lambda: choisir_personnage("Luigi"),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol("Luigi"),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    Button(scale=(0.2, 0.1), position=(0.4, 0.1), color=color.pink, icon='peach.png',
           on_click=lambda: choisir_personnage("Peach"),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol("Peach"),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    Button(scale=(0.2, 0.1), position=(-0.4, -0.1), color=color.blue, icon='toad.png',
           on_click=lambda: choisir_personnage("Toad"),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol("Toad"),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    Button(scale=(0.2, 0.1), position=(0.0, -0.1), color=color.orange, icon='daisy.png',
           on_click=lambda: choisir_personnage("Daisy"),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol("Daisy"),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    Button(scale=(0.2, 0.1), position=(0.4, -0.1), color=color.cyan, icon='Harmonie.png',
           on_click=lambda: choisir_personnage("Harmonie"),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol("Harmonie"),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    # Bouton aléatoire pour sélectionner un joueur au hasard
    def selectionner_joueur_aleatoire():
        personnage_aleatoire = random.choice(personnages)
        choisir_personnage(personnage_aleatoire)

    Button(
        text=translations[current_language]["random_character"],
        scale=(0.4, 0.1),
        position=(0, -0.25),
        color=color.yellow,
        on_click=selectionner_joueur_aleatoire
    )

    Button(
        text=translations[current_language]["back"],
        scale=(0.4, 0.1),
        position=(0, -0.4),
        color=color.red,
        on_click=afficher_parametres
    )  # Bouton retour

# Fonction pour choisir le personnage
def choisir_personnage(personnage):
    global selected_player
    selected_player = personnage
    print(f"{translations[current_language]['selected_character']} {selected_player}")
    afficher_selection_map()

##Fonction pour choisir la map
def afficher_selection_map():
    global selected_map  
    scene.clear()

    Text(text=translations[current_language]["select_map"], position=(-0.1, 0.5), scale=1.5, color=color.white, background=True)
    texte_map = Text(text="Map sélectionnée :", position=(-0.6, 0.4), scale=1.2, color=color.white)

    # Fonction pour mettre à jour le texte de la map survolée
    def mettre_a_jour_texte_survol(nom_map):
        texte_map.text = fr"Map sélectionnée : {nom_map}" if nom_map else "Selectionned Map :"

    # Boutons pour choisir les maps
    Button(scale=(0.3, 0.3), position=(-0.4, 0.2), icon='paysage.png',color=color.clear, on_click=lambda: choisir_map(1),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol(translations[current_language]["mushroom_kingdom"]),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    Button(scale=(0.3, 0.3), position=(0.4, 0.2), icon='dessert.png',color=color.clear, on_click=lambda: choisir_map(2),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol(translations[current_language]["sarasaland"]),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    Button(scale=(0.3, 0.3), position=(-0.4, -0.2), icon='galaxie.png',color=color.clear,on_click=lambda: choisir_map(3),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol(translations[current_language]["comet_observatory"]),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    Button(scale=(0.3, 0.3), position=(0.4, -0.2), icon='chateau.png',color=color.clear, on_click=lambda: choisir_map(4),
           on_mouse_enter=lambda: mettre_a_jour_texte_survol(translations[current_language]["bowser_castle"]),
           on_mouse_exit=lambda: mettre_a_jour_texte_survol(""))

    # Bouton aléatoire pour sélectionner une map au hasard
    def selectionner_map_aleatoire():
        numero_map_aleatoire = random.randint(1, 4)  # Choisit une map au hasard
        choisir_map(numero_map_aleatoire)

    Button(text=translations[current_language]["random_map"], scale=(0.4, 0.1), position=(0, -0.3), color=color.yellow,
           on_click=selectionner_map_aleatoire)

    Button(text=translations[current_language]["back"], scale=(0.4, 0.1), position=(0, -0.4), color=color.red,
           on_click=afficher_parametres)

# Fonction pour choisir la map
def choisir_map(numero_map):
    global selected_map
    selected_map = numero_map 
    print(f"Map {numero_map} sélectionnée")
    lancer_interface()

#################  FIN DE LA PAGE DES PARAMETRES ########

 ################# PAGE DU JEU ###############################
# Fonction pour lancer l'interface de jeu
def lancer_interface():
    global player, selected_player, score_piece, start_time, timer_text, retour_button, score_pieces_text, camera_button
    global sky, ground, musique_fond ,regle3, regle1,regle2, regle4, regle5 , tree,lac, tropic, tour , brique, ennemi

    scene.clear()
    musique_fond.stop()
    score_piece = 0

    creer_bowserjr()             # Lancer la création de BowserJr
    start_time = time.time()     # Initialisation du temps de départ

    # choix de la  map##
    if selected_map == 1:  # Le royaume Champignon (Map 1)
        sky = Entity(model='cube', texture='paysage.png', scale=100, double_sided=True)  # Ciel pour la Map 1
        ground = Entity(model='plane', texture='grass', collider='mesh', scale=(20, 20, 20))  # Sol pour la Map 1
        trees = []
        for i in range(5):  
            tree = Entity(model='quad',texture='tree.png',scale=10, position=(random.uniform(-10, 10), 4, random.uniform(-10, 10)))
        trees.append(tree) #arbe

        briques = []
        spacing = 0.02  
        briqueespace = 5  
        for i in range(5):
            brique = Entity(model='quad',texture='brique.png',scale=1,position=(i * (1 + spacing),briqueespace , 0)  )
        briques.append(brique)   #brique

        ennemi = Entity(model='quad', texture='goomba.png', scale=1, position=(0, 0.5, 0))
        deplacement_ennemi(ennemi)  #goomba (regarder ligne environ 750 )


    elif selected_map == 2:  # Sarasaland (Map 2)
        sky = Entity(model='cube', texture='dessert.png', scale=100, double_sided=True)  # Ciel pour la Map 2
        ground = Entity(model='plane', texture='sand.png', collider='mesh', scale=(20, 20, 20))  # Sol pour la Map 2
        lacs = [] 
        for i in range(2):  
            lac= Entity(model='plane',texture='lac.png',scale=2, position=(random.uniform(-10, 10), 0.1, random.uniform(-10, 10)))
        lacs.append(lac) #lac

        tropics=[]
        for i in range(5):  
            tropic= Entity(model='quad',texture='tropic.png',scale=10, position=(random.uniform(-10, 10), 3, random.uniform(-10, 10)))
        tropics.append(tropic) #tropic

        ennemi = Entity(model='quad', texture='pokey.png', scale=2, position=(0, 1, 4))
        deplacement_ennemi(ennemi)  #pookey


    elif selected_map == 3:  # Univers (Map 3)
        sky = Entity(model='cube', texture='galaxie.png', scale=100, double_sided=True)  # Ciel pour la Map 3
        ground = Entity(model='plane', texture='sol.png', collider='mesh', scale=(20, 20, 20))  # Sol pour la Map 3
        stars = []
        for i in range(20):  
            star = Entity(model='quad',texture='starts.png',scale=0.5,  position=(random.uniform(-10, 10), 10, random.uniform(-10, 10)))
        stars.append(star)
        ennemi = Entity(model='quad', texture='gloobe.png', scale=2, position=(0, 1, 4))
        deplacement_ennemi(ennemi) ##violet


    elif selected_map == 4:  # Chateau Bowser(Map 4)
        sky = Entity(model='cube', texture='chateau.png', scale=100, double_sided=True)  # Ciel pour la Map 4
        ground = Entity(model='plane', texture='dea.png', collider='mesh', scale=(20, 20, 20))  # Sol pour la Map 4
        tours=[]
        for i in range(5):  
            tour= Entity(model='quad',texture='tour.png',scale=15, position=(random.uniform(-10, 10), 3, random.uniform(-10, 10)))
        tours.append(tour)
        ennemi = Entity(model='quad', texture='Roi BOO.png', scale=3, position=(5, 5, 5))
        deplacement_ennemi(ennemi) 



    ###CHOIX DES PERSONNAGES##
    if selected_player == "Mario":
        player = Entity(model='quad', texture='mario.png', scale=(1, 2, 1), collider='box', position=(0, 1, -10))  # Mario
    elif selected_player == "Luigi":
        player = Entity(model='quad', texture='luigi.png', scale=(1, 2, 1), collider='box', position=(0, 1, -10))  # Luigi
    elif selected_player == "Peach":
        player = Entity(model='quad', texture='peach.png', scale=(1, 2, 1), collider='box', position=(0, 1, -10))  # Peach
    elif selected_player == "Toad":
        player = Entity(model='quad', texture='toad.png', scale=(1, 2, 1), collider='box', position=(0, 1, -10))  # Toad
    elif selected_player == "Daisy":
        player = Entity(model='quad', texture='daisy.png', scale=(1, 2, 1), collider='box', position=(0, 1, -10))  # Daisy
    elif selected_player == "Harmonie":
        player = Entity(model='quad', texture='harmonie.png', scale=(1, 2, 1), collider='box', position=(0, 1, -10))  # Harmonie


    # Déplacer la caméra pour dézoomer
    camera.position = (0, 10, -10)
    camera.rotation_x = 35
    camera.parent = player
    global is_first_person   # Initialisation de la vue
    is_first_person = False

    camera_button = Button(text="Camera", scale=(0.4, 0.1), position=(0.8, 0.4), color=color.blue, on_click=toggle_camera_view) # Bouton pour changer de vue de caméra
    score_pieces_text = Button(text="Piece: 0", origin=(0, 0), position=(-0.4, 0.4),scale=(0.2, 0.1), color=color.yellow) # Texte pour afficher le score des pièces à côté du bouton retour
    timer_text = Button(text="Temps: 0.0", origin=(0, 0), position=(0, 0.4), scale=(0.2, 0.1), color=color.orange)  # Timer affiché en haut à gauche
    retour_button = Button(text=translations[current_language]["back"], scale=(0.4, 0.1), position=(-0.8, 0.4), color=color.red, on_click=afficher_menu_principal)
    
    t = translations[current_language]  
    regle1 = Text(t["move"], position=(-0.6, -0.2), scale=1, color=color.white, origin=(0.5, 0.5))
    regle2 = Text(t["launch_shell"], position=(-0.5, -0.3), scale=1, color=color.white, origin=(0.5, 0.5))
    regle3 = Text(t["special_attack"], position=(-0.6, -0.4), scale=1, color=color.white, origin=(0.5, 0.5))
    regle4 = Text(t["camera_zoom_out"], position=(0.8, -0.4), scale=1, color=color.white, origin=(0.5, 0.5))
    regle5 = Text(t["camera_zoom_in"], position=(0.8, -0.3), scale=1, color=color.white, origin=(0.5, 0.5))



######################### FIN DE L'INTERFACE DU JEU #############################


################################LES OBJETS DU JEU#########################""""
# Fonction pour créer une carapace
def lancer_carapace():
    global player, sound_effect
    if player:  
        position_initiale = player.position + player.forward *0 # Position initiale : devant Mario
        sound_effect = Audio('carapace.wav', loop=False, autoplay=True)  # Le son se joue immédiatement
        carapace = Entity(model='quad',texture='carapace.png',scale=(0.5, 0.5, 0.5),position=position_initiale,collider='box',rotation=player.rotation)
        carapaces.append(carapace)
        invoke(supprimer_carapace, carapace, delay=5) # La carapace disparaît après 5 secondes


# Fonction pour supprimer une carapace
def supprimer_carapace(carapace):
    if carapace in carapaces:
        carapaces.remove(carapace)
        destroy(carapace)

# Fonction pour lancer une boule de feu
boules_de_feu = []
def lancer_boule_feu():
    sound_fire.play()  
    global bowserjr
    if bowserjr:  
        boule_feu = Entity(model='quad',texture='boulefeu.png',scale=(0.5, 0.5, 0.5),position=bowserjr.position + Vec3(0, 0, 0),  collider='box')
        
        # Choix aléatoire de direction de la boule de feu 
        direction_principale = choice([
            Vec3(0, 0, -1),  # Devant
            Vec3(0, 0, 1),   # Derrière
            Vec3(-1, 0, 0),  # Gauche
            Vec3(1, 0, 0)    # Droite
        ])

        # Direction des boule de feu
        variation = Vec3(uniform(1, 1), uniform(-0.5, 0.5), uniform(-0.5, 0.5))
        boule_feu.direction = (direction_principale + variation).normalized()
        boules_de_feu.append(boule_feu)
        invoke(supprimer_boule_feu, boule_feu, delay=10) # La boule de feu disparaît après 10 secondes  ##invoke sert a appeler une autre fonction


def supprimer_boule_feu(boule_feu):
    if boule_feu in boules_de_feu:
        boules_de_feu.remove(boule_feu)
    destroy(boule_feu)


# Fonction pour créer une banane à une position aléatoire
def creer_banane():
    x = uniform(-10, 10)
    z = uniform(-10, 10)
    banane = Entity(model='quad', texture='banane.png', scale=(1, 1, 1), position=(x, 0.5, z), collider='box')
    banane.apparue = time.time()  
    bananes.append(banane)
    invoke(disparaitre_banane, banane, delay=10)  # Faire disparaître la banane après 10 secondes

# Fonction pour faire disparaître une banane
def disparaitre_banane(banane):
    if banane in bananes:
        bananes.remove(banane)
        destroy(banane)

##Fonction pour la caméra
def toggle_camera_view():
    global is_first_person
    is_first_person = not is_first_person

    if is_first_person:
        # Vue subjective : la caméra suit la position de Mario
        camera.parent = player
        camera.position = (0, 2, 0)  # Position au niveau des yeux de Mario
        camera.rotation = (0, 0, 0)  # Orientée vers l'avant
    else:
        # Vue classique : caméra dézoomée
        camera.parent = None
        camera.position = (0, 10, -10)
        camera.rotation_x = 35

   
# Fonction pour créer une pièce à une position aléatoire
def creer_piece():
    x = uniform(-10, 10)
    z = uniform(-10, 10)
    piece = Entity(model='quad', texture='piece.png', scale=(1, 1, 1), position=(x, 1, z), collider='box')
    piece.collected = False  # Propriété pour marquer si la pièce a été collectée
    pieces.append(piece)
    invoke(disparaitre_piece, piece, delay=10) # disparaître la pièce après 10 secondes

# Fonction pour faire disparaître la pièce
def disparaitre_piece(piece):
    destroy(piece)

# Fonction pour créer BowserJr à une position aléatoire
def creer_bowserjr():
    global bowserjr, point_A, point_B
    if not bowserjr:  # Vérifie que BowserJr n'existe pas déjà
        x = uniform(-10, 10)
        z = uniform(-10, 10)
        bowserjr = Entity(model='quad', texture='bowserjr.png', scale=(1, 2, 1), position=(x, 1, z), rotation_y=0)
        # Ombre pour BowserJr
        bowserjr.shadow = Entity(model='circle', color=color.black33, scale=(1.5, 1.5, 1), position=(bowserjr.position.x, 0.01, bowserjr.position.z), rotation_x=90)
        
        # Générer un point de départ (A) et un point d'arrivée (B)
        point_A = Vec3(uniform(-10, 10), 1, uniform(-10, 10))
        point_B = Vec3(uniform(-10, 10), 1, uniform(-10, 10))

# Fonction pour créer un champignon à une position aléatoire
def creer_champi():
    global champignon, point_C, point_D
    x = uniform(-10, 10)
    z = uniform(-10, 10)
    champignon = Entity(model='quad', texture='champignon.png', scale=(1, 2, 1), position=(x, 1, z), rotation_y=0)
       
    # Générer un point de départ (A) et un point d'arrivée (B)
    point_C = Vec3(uniform(-10, 10), 1, uniform(-10, 10))
    point_D = Vec3(uniform(-10, 10), 1, uniform(-10, 10))

    invoke(disparaitre_piece, champignon, delay=10) #

# Fonction pour faire disparaître le champignon
def disparaitre_champi(champignon):
    champignon.disable()


# Fonction pour créer une onde de choc
def create_shockwave(position):# Crée une onde de choc autour de Peach
    shockwave = Entity(model='circle', color=color.white, scale=(1, 1, 1), position=position, collider='box')
    # L'onde de choc s'agrandit au fil du temps
    shockwave.scale = Vec3(3, 3, 1)  # Ajustez la taille de l'onde de choc 
    destroy(shockwave, delay=0.5)  # Supprime l'onde de choc après 0.5 seconde

    # Vérification de la collision  pouvoir de peach avec BowserJr 
    if bowserjr and (bowserjr.position - position).length() < shockwave.scale.x:
        # Repousse BowserJr à l'extérieur du rayon de l'onde de choc
        bowserjr.position += (bowserjr.position - position).normalized() * 2
        print(f"BowserJr  a été repoussé par la vague de choc créer par Peach!")

#########################FIN DES OBJETS####################


def update():
    global bowserjr, player, point_A, point_B, dernier_lancement_boule_feu, start_time, carapaces, boules_de_feu,bananes, score_piece
    global space_press_count, last_press_time, is_jumping, velocity_y,ground_level,speed_champignon, boost_time
    
        # Tourner la caméra autour du personnage  (360 degrés)
    if is_first_person:
        camera.rotation_y += held_keys['right arrow'] * 1  # Tourne à droite
        camera.rotation_y -= held_keys['left arrow'] * 1   # Tourne à gauche

       ##########################Caractérique des personnages####################
    if player:
        speed = 5 * time.dt

        if selected_player == "Toad":
            if held_keys['s']: 
                speed *= 2  # Toad roule plus vite lorsqu'on maintient la touche 'S'

            ###Harmonie devient invincible lorsque elle touche Bowser JR ##

                # Daisy  flotte temporairement lorsqu'on appuie sur 'S'
        if selected_player == "Daisy":
            if held_keys['s'] and not is_jumping:  # Appui sur 'S' pour activer le flotement
                is_jumping = True
                velocity_y = 1  # Vitesse réduite pour flotter
            if is_jumping:
                player.y += velocity_y  
                velocity_y += -0.05  # Appliquer une faible gravité pour rester en l'air plus longtemps
            if player.y <= ground_level:  # Quand Daisy touche le sol
                player.y = ground_level
                is_jumping = False

        # Peach crée une vague de choc avec la touche 'S'
        if selected_player == "Peach":
            if held_keys['s']:  # Lorsque la touche 'S' est maintenue
                create_shockwave(player.position)  # Créer une onde de choc qui repousse BowserJr

        ##Luigi peut se téléporter##
        if selected_player == "Luigi":
            if held_keys['s']:  
                teleport_x = player.position.x + random.randint(-10, 10)  
                teleport_y = player.position.y + random.randint(-10, 10)  
                teleport_y = ground_level  
                player.position = Vec3(teleport_x, teleport_y, ground_level)

    ###########FIN DES POUVOIRS (caractéristique) DES PERSONNAGES###########################

    ############################################################
                    ##CLAVIER##
        # Déplacements avec les flèches directionnelles
        if held_keys['up arrow']:
            player.position += player.forward * speed
        if held_keys['down arrow']:
            player.position -= player.forward * speed
        if held_keys['left arrow']:
            player.position -= player.right * speed
        if held_keys['right arrow']:
            player.position += player.right * speed

        # Lancer une carapace avec la touche espace
        if held_keys['space']:
            lancer_carapace()

        # Contrôle du zoom avec B et D
        if held_keys['b']:
            camera.position += Vec3(0, -0.2, 0.2)
        if held_keys['d']:
            camera.position += Vec3(0, 0.2, -0.2)

    ############################################################

# Vérification de collision entre le joueur et le champignon
        if champignon and (player.position - champignon.position).length() < 1:
            son_acc.play()
            speed = 10
            boost_duration = 5  # Durée du boost en secondes
            boost_time = time.dt  # Enregistrer le temps lorsque le boost est activé
            print("Boost accéléré.")
            destroy(champignon)

        # Vérifie si le boost est actif
        if boost_time > 0 and time.time() - boost_time < boost_duration:  # Si le boost est encore actif
            speed = 8  # Appliquer le boost à la vitesse du joueur
        else:
            boost_time = 0  # Réinitialiser le boost_time pour désactiver le boost
            player.speed = 2  # Vitesse par défaut du joueur
            

        ##Apparaition des bananes toutes les 5 secondes
        if time.time() % 5 < time.dt:  # Créer une banane toutes les 5 secondes
            creer_banane()

        ##Apparaition des champignons toutes les 5 secondes
        if time.time() % 5 < time.dt:  # Créer un champi toutes les 5 secondes
            creer_champi()

        # Gérer le déplacement des carapaces
        for carapace in carapaces[:]:
            if carapace and carapace.enabled:  
                carapace.position += carapace.forward * 10 * time.dt

                # Supprimer la carapace si elle sort des limites
                if abs(carapace.position.x) > 10 or abs(carapace.position.z) > 10:
                    supprimer_carapace(carapace)

        # Limiter la position de Mario
        player.position = Vec3(
            clamp(player.position.x, -10, 10),
            player.position.y,
            clamp(player.position.z, -10, 10)
        )

        # Afficher le timer
        elapsed_time = time.time() - start_time
        timer_text.text = f"{'TEMPS' if current_language == 'fr' else 'TIME'}: {elapsed_time:.1f}"

        # Créer une pièce toutes les 5 secondes
        if int(elapsed_time) % 5 == 0 and elapsed_time % 5 < time.dt:
            creer_piece()

    ###################----COLLISION ENTRE OBJETS-----#######################333

# Vérification de collision entre Mario , Luigi, Peach, Daisy Toad et BowserJr
        if bowserjr and (player.position - bowserjr.position).length() < 1:
            if selected_player in ["Mario", "Luigi", "Peach", "Daisy","Toad"]:
                print("Game Over! Mario a touché BowserJr.")
                sound_explosion.play()
                gameover()

        # Vérification de collision entre Mario et l'ennemi
        if ennemi and (player.position - ennemi.position).length() < 1:
            if selected_player in ["Mario", "Luigi", "Peach", "Daisy","Toad"]:
                print("Game Over! Mario a été touché par un ennemi.")
                sound_explosion.play()
                gameover()

# Vérification de collision entre Harmonie et BowserJr
        if selected_player == "Harmonie" and bowserjr and (player.position - bowserjr.position).length() < 1:
            pass  # Rien ne se passe, pas de Game Over pour Harmonie



    for piece in pieces:
            if piece and (player.position - piece.position).length() < 0.5 and not piece.collected:
                print("Mario a touché une pièce!")
                son_piece.play()  # Joue le son de la pièce
                piece.collected = True  #
                disparaitre_piece(piece) 
                score_piece += 1  
                score_pieces_text.text = f"Piece: {score_piece}"  # Mettre à jour le texte du bouton pour afficher le score

# Vérifier si une boule de feu touche Mario
    for boule_feu in boules_de_feu[:]:
        if boule_feu and hasattr(boule_feu, 'position') and boule_feu.enabled:
            if (player.position - boule_feu.position).length() < 1:
                print("Game Over! Mario a été touché par une boule de feu.")
                sound_explosion.play()
                gameover()

    # Vérifier si une bananes  touche Mario
    for banane in bananes[:]:
        if banane and hasattr(banane, 'position') and banane.enabled:
            if (player.position - banane.position).length() < 1:
                print("Game Over! Mario a été touché par une bananes.")
                sound_explosion.play()
                gameover()

        # Vérifier collision entre carapaces et BowserJr
    for carapace in carapaces[:]:
        if carapace and carapace.enabled:  # Vérifie si la carapace existe
            if (carapace.position - bowserjr.position).length() < 1:
                print("BowserJr a été touché par une carapace.")
                sound_explosion.play()
                game_end()

# Vérifier collision entre carapaces et l'ennemi
    for carapace in carapaces[:]:
        if carapace and carapace.enabled:
            if (carapace.position - ennemi.position).length() < 1:
                print("L'ennemi a été touché par une carapace.")
                invoke(detruire_ennemi, ennemi, delay=0.5)  
                carapace.disable()  

    ###################---- FIN DES COLLISION ENTRE OBJETS ET ENNEMI......-----####################33

    ##DEPLACEMENT ALEATOIRE########################
    # Déplacement de BowserJr entre deux points
    if bowserjr:
        direction = (point_B - point_A).normalized()
        speed_bowserjr = 1
        bowserjr.position += direction * speed_bowserjr * time.dt

        if (bowserjr.position - point_A).length() >= (point_B - point_A).length():
            point_A = point_B
            point_B = Vec3(uniform(-10, 10), 1, uniform(-10, 10))

        bowserjr.position = Vec3(
            clamp(bowserjr.position.x, -10, 10),
            clamp(bowserjr.position.y, 0.5, 2),
            clamp(bowserjr.position.z, -10, 10)
        )
        bowserjr.position += Vec3(0, math.sin(time.time() * 4) * 0.05, 0)
        bowserjr.rotation_y += 1 * time.dt

                # Mise à jour de l'ombre de BowserJr
        if hasattr(bowserjr, 'shadow') and bowserjr.shadow:
            bowserjr.shadow.position = Vec3(bowserjr.position.x, 0.01, bowserjr.position.z)

    # Déplacement des champignon entre deux points
    if champignon:
        direction = (point_B - point_A).normalized()
        speed_champignon = 1
        champignon.position += direction * speed_champignon * time.dt

        if (champignon.position - point_A).length() >= (point_D - point_C).length():
            point_A = point_B
            point_B = Vec3(uniform(-10, 10), 1, uniform(-10, 10))

        champignon.position = Vec3(
            clamp(champignon.position.x, -10, 10),
            clamp(champignon.position.y, 0.5, 2),
            clamp(champignon.position.z, -10, 10)
        )
        champignon.position += Vec3(0, math.sin(time.time() * 4) * 0.05, 0)
        champignon.rotation_y += 1 * time.dt

        ##### FIN DEPLACEMENT ALEATOIRE########################


########### BOULE DE FEU#############
# Lancer une boule de feu toutes les 5 secondes
    if time.time() - dernier_lancement_boule_feu >= 5:
        lancer_boule_feu()
        dernier_lancement_boule_feu = time.time()


    # Déplacer les boules de feu
    boules_a_supprimer = []
    for boule_feu in boules_de_feu[:]:
        if boule_feu and hasattr(boule_feu, 'position') and boule_feu.enabled:
            # Déplacement selon la direction
            boule_feu.position += boule_feu.direction * time.dt
            # Supprimer la boule si elle sort trop loin
            if abs(boule_feu.position.z) > 10  or abs(boule_feu.position.x) > 10 or abs(boule_feu.position.y) > 10:
                boules_a_supprimer.append(boule_feu)

    # Supprimer après les boule de feu
    for boule_feu in boules_a_supprimer:
        supprimer_boule_feu(boule_feu)
################# FIN BOULE DE FEU ############""


##############DEPLACEMENT ALEATOIRE ENNEMI#######
def deplacement_ennemi(ennemi): # Pour que l'ennemi puisse se déplacer aléatoirement
    nouveau_point = Vec3(random.uniform(-10, 10), ennemi.y, random.uniform(-10, 10)) 
    ennemi.animate_position(nouveau_point, duration=0.5, curve=curve.linear)
    invoke(deplacement_ennemi, ennemi, delay=2.5)                  

# Fonction pour gérer la disparaition de l'ennemi
def detruire_ennemi(ennemi):
    print("L'ennemi est détruit!")
    sound_explosion.play()
    ennemi.disable()  # Désactive l'ennemi
    invoke(reapparition_ennemi, ennemi, delay=5)  
# Fonction pour gérer la réapparition de l'ennemi
def reapparition_ennemi(ennemi):
    ennemi.position = (random.uniform(-10, 10), 1, random.uniform(-10, 10))  
    ennemi.enable()  

#########FIN DEPLACEMENT ENNNEMI ALEATOIRE#####


####### PAGE DE FIN SI LE JOEUR PERD #######
def gameover():
    elapsed_time = int(time.time() - start_time)  
    scene.clear()
    
    t = translations[current_language]  
    
    Text(t["project_by"], position=(-0.50, 0.5), scale=1, color=color.white)
    Text("ANTON NELCON Steve", position=(-0.29, 0.5), scale=1, color=color.red, bold=True)
    Text(t["student"], position=(-0.020, 0.5), scale=1, color=color.white)
    
    Button(scale=(0.6, 0.6), position=(-0.6, -0.1), color=color.clear, icon='gameo.png', border=False)
    Button(scale=(0.6, 0.6), position=(0.6, -0.1), color=color.clear, icon='bowserfin.png', border=False)
    
    Text(text=t["game_over"], position=(0, 0.3), scale=2.5, origin=(0, 0), color=color.red)
    Text(text=t["defeated"], position=(0, 0.7 - 0.5), scale=1.5, origin=(0, 0), color=color.white)
    Text(text=f"{t['coins_collected']}{score_piece}", origin=(0, 0), scale=1.5, color=color.yellow, position=(0, 0.1))
    Text(text=f"{t['time_elapsed']}{elapsed_time} {t['seconds']}", origin=(0, 0), scale=1.5, color=color.green, position=(0, 0.05))
    Button(text=t["replay"], scale=(0.3, 0.1), position=(0, -0.2), color=color.green, on_click=rejouer)
    Button(text=t["quit"], scale=(0.3, 0.1), position=(0, -0.4), color=color.red, on_click=quitter)

#######  FIN PAGE DE FIN SI LE JOEUR PERD #######


####### PAGE DE FIN SI LE JOEUR GAGNE #######

def game_end():
    elapsed_time = int(time.time() - start_time)  
    scene.clear()
    
    t = translations[current_language]  
    Text(t["project_by"], position=(-0.50, 0.5), scale=1, color=color.white)
    Text("ANTON NELCON Steve", position=(-0.29, 0.5), scale=1, color=color.red, bold=True)
    Text(t["student"], position=(-0.020, 0.5), scale=1, color=color.white)
    
    Button(scale=(0.6, 0.6), position=(-0.6, -0.1), color=color.clear, icon='ami.png', border=False)
    Button(scale=(0.6, 0.6), position=(0.6, -0.1), color=color.clear, icon='bowserpleure.png', border=False)
    
    Text(text=t["well_played"], position=(0, 0.3), scale=2.5, origin=(0, 0), color=color.gold)
    Text(text=t["bowser_defeated"], position=(0, 0.25), scale=1.5, origin=(0, 0), color=color.red)
    Text(text=f"{t['coins_collected']}{score_piece}", origin=(0, 0), scale=1.5, color=color.yellow, position=(0, 0.05))
    Text(text=f"{t['time_elapsed']}{elapsed_time} {t['seconds']}", origin=(0, 0), scale=1.5, color=color.green, position=(0, 0))
    Button(text=t["replay"], scale=(0.3, 0.1), position=(0, -0.2), color=color.azure, text_color=color.black, on_click=rejouer)
    Button(text=t["quit"], scale=(0.3, 0.1), position=(0, -0.4), color=color.red, text_color=color.white, on_click=quitter)

####### FIN  PAGE DE FIN SI LE JOEUR GAGNE #######

######## BOUTON REJOUER#########
def rejouer():
    afficher_menu_principal()
    lancer_interface()

###########"""FIN BOUTON REJOUER#####""

def quitter():
    application.quit()
        
is_dark_mode = True  # Par défaut, mode sombre

# Fonction pour quitter l'application
def quitter_application():
    application.quit()

afficher_menu_principal() # Lancer le menu principal
app.run()# Démarrer l'application Ursin