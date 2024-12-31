import pygame  # Importer la bibliothèque Pygame pour créer des jeux
import random  # Importer la bibliothèque random pour générer des nombres aléatoires

# Initialisation de pygame
pygame.font.init()  # Initialiser le module de polices pour afficher du texte
pygame.mixer.init()  # Initialiser le module de mixage pour le son

# Dimensions de la fenêtre de jeu
SCREEN_WIDTH = 800  # Largeur de la fenêtre de jeu
SCREEN_HEIGHT = 600  # Hauteur de la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Créer la fenêtre de jeu avec les dimensions définies
pygame.display.set_caption("Course de Voiture")  # Titre de la fenêtre de jeu

# Charger la musique de fond
pygame.mixer.music.load('musique.mp3')  # Remplacez par le nom de votre fichier audio
pygame.mixer.music.set_volume(0.5)  # Réglez le volume (0.0 à 1.0)

# Charger le son d'explosion
explosion_sound = pygame.mixer.Sound('Explosion.wav')  # Son de l'explosion
explosion_sound.set_volume(0.5)  # Volume de l'explosion

# Charger le son de la pièce
piece_sound = pygame.mixer.Sound('piece.wav')  # Son de l'explosion
piece_sound.set_volume(0.5)  # Volume de l'explosion

# Charger le son de la carapce
carapace_sound = pygame.mixer.Sound('carapace.wav')  # Son de l'explosion
carapace_sound.set_volume(0.5)  # Volume de l'explosion

# Définir les couleurs
WHITE = (255, 255, 255)  # Couleur blanche
BLACK = (0, 0, 0)  # Couleur noire
RED = (255, 0, 0)  # Couleur rouge
GREEN = (0, 255, 0)  # Couleur verte
BLUE = (0, 0, 255)  # Couleur bleue
YELLOW = (255, 255, 0)  # Couleur jaune
DARK_GREEN = (0, 200, 0)  # Couleur vert foncé
LIGHT_BLUE = (173, 216, 230)  # Couleur bleu clair pour la Map 
LIGHT_GRAY = (211, 211, 211)  # Couleur pour le mode clair
DARK_GRAY = (169, 169, 169)   # mode sombre
PINK = (255, 105, 180)  # Couleur rose pour le bouton Langue

##car_color = RED # Couleur par défaut de la voiture

# Variables pour les modes
current_mode = "sombre"  # Mode sombre par défaut

# Variable globale pour la langue actuelle
current_language = "fr"  # Par défaut, en français

# Variables pour la voiture
car_width = 50
car_height = 100
car_x = SCREEN_WIDTH // 2 - car_width // 2
car_y = SCREEN_HEIGHT - car_height - 10
car_speed = 0
normal_speed = 5
boost_speed = 10  # Vitesse lors du boost
boost_active = False
boost_start_time = 0
boost_duration = 2000  # Durée du boost en millisecondes

# Charger l'image du Joueur Mario
mario_image = pygame.image.load('mario.png')  # Assurez-vous que le chemin est correct
mario_image = pygame.transform.scale(mario_image, (car_width, car_height))  # Redimensionner l'image

# Variables pour l'obstacle
obstacle_width = 40
obstacle_height = 40
obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
obstacle_y = -600
obstacle_speed = 5 ##7  ##################################################

# Charger l'image de la banane (obstacle 1)
banane_image = pygame.image.load('banane.png')  # Assurez-vous que le chemin est correct
banane_image = pygame.transform.scale(banane_image, (obstacle_width, obstacle_height))  # Redimensionner l'image

# Variables pour le deuxième obstacle
second_obstacle_width = 80
second_obstacle_height = 80
second_obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
second_obstacle_y = -600
second_obstacle_visible = False
second_obstacle_timer = 0


# Charger l'image de Bowser (obstacle 2)
bowser_image = pygame.image.load('bowser.png')  # Assurez-vous que le chemin est correct
bowser_image = pygame.transform.scale(bowser_image, (second_obstacle_width, second_obstacle_height))  # Redimensionner l'image

# Variables pour les pièces
coin_width = 30
coin_height = 30
coin_x = random.randint(0, SCREEN_WIDTH - coin_width)
coin_y = random.randint(-600, -coin_height)  # Apparition aléatoire au-dessus de l'écran
coin_speed = 5
coin_score = 0  # Score des pièces

# Charger l'image de la carapace verte
carapace_image = pygame.image.load('carapace.png')  # Assurez-vous que le chemin est correct
carapace_image = pygame.transform.scale(carapace_image, (30, 30))  # Redimensionner si besoin

# Variables pour la carapace
carapace_x, carapace_y = None, None  # Position initiale de la carapace
carapace_speed = 10  # Vitesse de la carapace

# Fonction pour afficher la voiture avec la couleur actuelle
def draw_car(x, y):
    screen.blit(mario_image, (x, y))  # Afficher l'image de la banane

# Fonction pour afficher une pièce
def draw_coin(x, y):
    pygame.draw.circle(screen, YELLOW, (x + coin_width // 2, y + coin_height // 2), coin_width // 2)


# Fonction pour afficher l'obstacle (banane)
def draw_obstacle(x, y):
    screen.blit(banane_image, (x, y))  # Afficher l'image de la banane

# Fonction pour afficher le deuxième obstacle (Bowser)
def draw_second_obstacle(x, y):
    screen.blit(bowser_image, (x, y))  # Afficher l'image de Bowser


# Variable pour la couleur de la route
road_color = BLACK  # Couleur par défaut

# Fonction pour afficher la route
def draw_road():
    for i in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, i), (SCREEN_WIDTH // 2, i + 20), 5)

# Lancer la carapace
def launch_carapace():
    global carapace_x, carapace_y
    if carapace_x is None and carapace_y is None:
        carapace_x, carapace_y = car_x + car_width // 2, car_y  # La carapace démarre depuis Mario
        carapace_sound.play()

# Gérer le déplacement et collision de la carapace avec Bowser
def move_carapace():
    global carapace_x, carapace_y, second_obstacle_visible, second_obstacle_y, second_obstacle_x

    if carapace_x is not None and carapace_y is not None:
        carapace_y -= carapace_speed  # La carapace monte vers Bowser

        # Vérifier la collision avec Bowser
        if second_obstacle_visible:  # Vérifie d'abord si Bowser est visible
            # Conditions de collision entre la carapace et Bowser
            if (carapace_x < second_obstacle_x + obstacle_width and 
                carapace_x + 30 > second_obstacle_x and 
                carapace_y < second_obstacle_y + obstacle_height and 
                carapace_y + 30 > second_obstacle_y):
                
                second_obstacle_visible = False  # Désactiver Bowser après la collision
                carapace_x, carapace_y = None, None  # Réinitialiser la carapace après la collision
                return  # Sortir de la fonction pour éviter d'exécuter le code en dessous

        # Supprimer la carapace si elle dépasse l'écran
        if carapace_y < 0:
            carapace_x, carapace_y = None, None

# Afficher la carapace si elle est lancée
def draw_carapace():
    if carapace_x is not None and carapace_y is not None:
        screen.blit(carapace_image, (carapace_x, carapace_y))

# Fonction pour changer le mode (clair/sombre)
def toggle_mode():
    global current_mode
    if current_mode == "sombre":
        current_mode = "clair"
    else:
        current_mode = "sombre"

# Fonction pour basculer entre le français et l'anglais
def toggle_language():
    global current_language
    current_language = "en" if current_language == "fr" else "fr"

# Fonction pour dessiner un bouton avec un texte plus petit et fond rose
def draw_button_language(text, x, y, width, height, text_color, bg_color, action=None):
    font = pygame.font.SysFont(None, 20)  # Réduire la taille de la police pour un texte plus petit
    text_render = font.render(text, True, text_color)
    
    # Dessiner le fond du bouton
    pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=10)

    # Dessiner le texte sur le bouton
    screen.blit(text_render, (x + (width - text_render.get_width()) // 2, y + (height - text_render.get_height()) // 2))

    # Vérifier si le bouton est cliqué
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + width and y < mouse_y < y + height:
        if pygame.mouse.get_pressed()[0] == 1 and action is not None:  # Si clic gauche
            action()    
# Charger les images des personnages
characters = {
    "Mario": pygame.image.load('mario.png'),
    "Luigi": pygame.image.load('luigi.png'),
    "Peach": pygame.image.load('peach.png'),
    "Daisy": pygame.image.load('daisy.png'),
    "Toad": pygame.image.load('toad.png'),
    "Harmonie": pygame.image.load('harmonie.png')
}

# Redimensionner les images des personnages à la taille de la voiture
car_width, car_height = 70,100  # Taille des icônes
characters = {name: pygame.transform.scale(img, (car_width, car_height)) for name, img in characters.items()}

# Variables pour le personnage sélectionné (par défaut Mario)
selected_character_name = "Mario"
selected_character_image = characters[selected_character_name]

# Fonction pour afficher la voiture avec le personnage actuel
def draw_car(x, y):
    screen.blit(selected_character_image, (x, y))

# Fonction pour ouvrir la fenêtre de paramètres pour choisir un personnage
def open_character_settings():
    global selected_character_name, selected_character_image, road_color
    settings_open = True
    character_names = list(characters.keys())
    font = pygame.font.SysFont(None, 20)
    character_spacing = 100  # Espacement entre chaque personnage

    # Définir les dimensions et positions des boutons
    button_width = 100
    button_height = 50
    map1_button_pos = (SCREEN_WIDTH // 4 - button_width // 2, SCREEN_HEIGHT - 210)  
    map2_button_pos = (3 * SCREEN_WIDTH // 4 - button_width // 2, SCREEN_HEIGHT - 210) 

    while settings_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_open = False

            # Détection du clic de l'utilisateur sur un personnage
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for i, name in enumerate(character_names):
                    if 100 + i * character_spacing < mouse_x < 150 + i * character_spacing and 170 < mouse_y < 350:
                        selected_character_name = name
                        selected_character_image = characters[name]
                        settings_open = False

             # Vérifier si l'utilisateur clique sur Map 1
                if map1_button_pos[0] < mouse_x < map1_button_pos[0] + button_width and map1_button_pos[1] < mouse_y < map1_button_pos[1] + button_height:
                    road_color = BLACK  # Route noire pour la Map 1
                    settings_open = False

                # Vérifier si l'utilisateur clique sur Map 2
                elif map2_button_pos[0] < mouse_x < map2_button_pos[0] + button_width and map2_button_pos[1] < mouse_y < map2_button_pos[1] + button_height:
                    road_color = LIGHT_BLUE  # Route bleu clair pour la Map 2
                    settings_open = False


        # Fond de la fenêtre de sélection avec un effet de transparence
        screen.fill((0, 0, 0, 128))  # Fond transparent pour l'arrière-plan complet
        pygame.draw.rect(screen, (40, 40, 40), (50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200), border_radius=20)

        # Police pour les textes avec la même taille
        font_size = 40  # Définir une taille uniforme
        title_font = pygame.font.SysFont(None, font_size)  # Taille pour le titre

        # Afficher le texte d'instruction avec la police
        # Vérifier la langue actuelle et modifier le texte du titre
        if current_language == "fr":
            title_text = title_font.render("Sélectionnez un personnage", True, (255, 255, 255))  # Texte en français
        else:
            title_text = title_font.render("Select a character", True, (255, 255, 255))  # Texte en anglais
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 130))

        # Afficher les options de personnages avec leur nom
        for i, name in enumerate(character_names):
            character_image = characters[name]
            x_position = 100 + i * character_spacing
            y_position = 170  # Réduire cette valeur pour rapprocher des personnages

            # Créer un cercle d'arrière-plan pour chaque personnage
            pygame.draw.circle(screen, (60, 60, 60), (x_position + car_width // 2, y_position + car_height // 2), car_width // 2 + 10)
            screen.blit(character_image, (x_position, y_position))

            # Afficher le nom du personnage en dessous
            character_text = font.render(name, True, (200, 200, 200))
            screen.blit(character_text, (x_position - character_text.get_width() // 2 + car_width // 2, y_position + car_height + 5))  # Ajuster l'espacement ici

            # Surligner le personnage sélectionné avec un contour lumineux
            if selected_character_name == name:
                pygame.draw.circle(screen, (255, 215, 0), (x_position + car_width // 2, y_position + car_height // 2), car_width // 2 + 12, 3)

        # Nouveau texte pour "Sélectionnez une map" dans le fond transparent
        # Vérifier la langue actuelle et modifier le texte de la map
        if current_language == "fr":
            map_text = title_font.render("Sélectionnez une map", True, (255, 255, 255))  # Texte en français
        else:
            map_text = title_font.render("Select a map", True, (255, 255, 255))  # Texte en anglais

        screen.blit(map_text, (SCREEN_WIDTH // 2 - map_text.get_width() // 2, SCREEN_HEIGHT - 260))  # Position selon vos besoins

        # Gestion des couleurs des boutons
        button_color = (100, 100, 200)  #Bleu claire
        button_hover_color = (120, 120, 220) #Bleu claire

        # Détection de survol des boutons
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if map1_button_pos[0] < mouse_x < map1_button_pos[0] + button_width and map1_button_pos[1] < mouse_y < map1_button_pos[1] + button_height:
            pygame.draw.rect(screen, button_hover_color, (map1_button_pos[0], map1_button_pos[1], button_width, button_height), border_radius=10)  # Bouton Map 1
        else:
            pygame.draw.rect(screen, button_color, (map1_button_pos[0], map1_button_pos[1], button_width, button_height), border_radius=10)  # Bouton Map 1

        if map2_button_pos[0] < mouse_x < map2_button_pos[0] + button_width and map2_button_pos[1] < mouse_y < map2_button_pos[1] + button_height:
            pygame.draw.rect(screen, button_hover_color, (map2_button_pos[0], map2_button_pos[1], button_width, button_height), border_radius=10)  # Bouton Map 2
        else:
            pygame.draw.rect(screen, button_color, (map2_button_pos[0], map2_button_pos[1], button_width, button_height), border_radius=10)  # Bouton Map 2

        # Afficher le texte sur les boutons
        map1_text = font.render("Map 1", True, (255, 255, 255))
        map2_text = font.render("Map 2", True, (255, 255, 255))
        screen.blit(map1_text, (map1_button_pos[0] + button_width // 2 - map1_text.get_width() // 2, map1_button_pos[1] + button_height // 2 - map1_text.get_height() // 2))
        screen.blit(map2_text, (map2_button_pos[0] + button_width // 2 - map2_text.get_width() // 2, map2_button_pos[1] + button_height // 2 - map2_text.get_height() // 2))

        pygame.display.update()


# Fonction pour dessiner un bouton avec couleur de texte personnalisée
def draw_button(text, x, y, width, height, color, hover_color, action=None, text_color=WHITE):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    
    # Vérifier si la souris est sur le bouton
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, hover_color, button_rect)
        if pygame.mouse.get_pressed()[0] == 1 and action:
            action()  # Exécute l'action du bouton
    else:
        pygame.draw.rect(screen, color, button_rect)
    
    # Ajouter le texte (ou l'icône) sur le bouton avec la couleur du texte définie
    font = pygame.font.SysFont(None, 40)
    text_render = font.render(text, True, text_color)
    screen.blit(text_render, (x + (width - text_render.get_width()) // 2, y + (height - text_render.get_height()) // 2))



# Fonction pour afficher l'écran de démarrage
def game_intro():
    global current_mode
    
    pygame.mixer.music.play(-1)  # Lecture en boucle (-1 pour répéter)
    
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Changer la couleur de fond en fonction du mode
        if current_mode == "sombre":
            screen.fill(BLACK)
        else:
            screen.fill(LIGHT_GRAY)
        
        # Afficher le titre
        font = pygame.font.SysFont(None, 55)
        text = font.render("Course de Voiture", True, WHITE if current_mode == "sombre" else BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))

        
        # Afficher le bouton pour changer de mode (icône 💡)
        draw_button("💡", SCREEN_WIDTH - 60, 20, 40, 40, WHITE, DARK_GREEN, toggle_mode)

        # Vérifier si l'emoji est cliqué pour changer le mode
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and pygame.Rect(SCREEN_WIDTH - 60 - 20, 20 - 20, 40, 40).collidepoint(mouse_x, mouse_y):
            toggle_mode()  # Appeler la fonction de changement de mode
        
        
        # Afficher les autres boutons
        draw_button("Jouer", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 50, GREEN, DARK_GREEN, game_loop)
        draw_button("Paramètres", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50, BLUE, DARK_GREEN, open_character_settings)
        draw_button("Quitter", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 110, 200, 50, RED, DARK_GREEN, pygame.quit)
        draw_button_language("Langue" if current_language == "fr" else "Language", SCREEN_WIDTH - 160, 20, 80, 40, BLACK, (255, 105, 180), toggle_language)
        
        ##CHANGER LA LANGUE
        play_text = "Jouer" if current_language == "fr" else "Play"
        settings_text = "Paramètres" if current_language == "fr" else "Settings"
        quit_text = "Quitter" if current_language == "fr" else "Quit"
        draw_button(play_text, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 50, GREEN, DARK_GREEN, game_loop)
        draw_button(settings_text, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50, BLUE, DARK_GREEN, open_character_settings)
        draw_button(quit_text, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 110, 200, 50, RED, DARK_GREEN, pygame.quit)


        # Afficher le texte en bas du menu
        footer_font = pygame.font.SysFont(None, 30)
        footer_text = footer_font.render("Par ANTON NELCON Steve L3 ISEI", True, WHITE if current_mode == "sombre" else BLACK)
        screen.blit(footer_text, (SCREEN_WIDTH // 2 - footer_text.get_width() // 2, SCREEN_HEIGHT - 30))  # Centrer le texte en bas

        pygame.display.update()


####ECRAN DE FIN DE JEU#####
def game_over():
    game_over_screen = True
    font_main = pygame.font.SysFont("Arial", 80, bold=True)  # Police principale agrandie et stylisée
    font_secondary = pygame.font.SysFont("Arial", 45)  # Police secondaire pour les détails
    clock = pygame.time.Clock()
    button_radius = 25  # Rayon pour des boutons arrondis

    # Animation pour le texte "Game Over" (clignotement léger)
    blink = True
    blink_timer = 0

    while game_over_screen:
        screen.fill((20, 20, 40))  # Fond sombre pour plus de contraste
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Animation de clignotement
        blink_timer += 1
        if blink_timer % 30 == 0:
            blink = not blink

        # Ombre du texte "Game Over"
        shadow_text = font_main.render("Game Over", True, (0, 0, 0))
        screen.blit(shadow_text, (SCREEN_WIDTH // 2 - shadow_text.get_width() // 2 + 5, SCREEN_HEIGHT // 6 + 5))

        # Texte "Game Over" avec clignotement
        if blink:
            game_over_text = font_main.render("Game Over", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 6))

        # Affichage du score total
        score_text = font_secondary.render(f"Score Total : {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3 + 40))

        # Affichage du temps final
        time_text = font_secondary.render(f"{'Temps écoulé' if current_language == 'fr' else 'Elapsed Time'}: {elapsed_time} sec", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        # Affichage des pièces ramassées
        coin_text = font_secondary.render(f"{'Pièces collectées' if current_language == 'fr' else 'Collected Coins'}: {coin_score}", True, YELLOW)
        screen.blit(coin_text, (SCREEN_WIDTH // 2 - coin_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        # Bouton "Rejouer" avec arrondi et surbrillance au survol
        draw_rounded_button("Rejouer" if current_language == "fr" else "Replay", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60, GREEN, DARK_GREEN, replay_game, button_radius)
        # Bouton "Quitter" avec arrondi et surbrillance au survol
        draw_rounded_button("Quitter" if current_language == "fr" else "Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 180, 200, 60, RED, (200, 0, 0), pygame.quit, button_radius)

        # Mise à jour de l'affichage et gestion des FPS
        pygame.display.update()
        clock.tick(60)

###ANIMATION POUR LE GAME OVER###
def draw_rounded_button(text, x, y, width, height, color, hover_color, action=None, radius=20):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Gestion de la couleur en fonction du survol
    current_color = hover_color if x < mouse[0] < x + width and y < mouse[1] < y + height else color
    
    # Dessiner un bouton arrondi
    pygame.draw.rect(screen, current_color, (x, y, width, height), border_radius=radius)
    
    # Déclencher l'action au clic
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        if click[0] == 1 and action is not None:
            action()
            
    # Afficher le texte sur le bouton
    button_font = pygame.font.SysFont("Arial", 35, bold=True)
    text_surface = button_font.render(text, True, WHITE)
    screen.blit(text_surface, (x + width // 2 - text_surface.get_width() // 2, y + height // 2 - text_surface.get_height() // 2))



# Fonction pour réinitialiser les variables du jeu
def reset_game():
    global car_x, car_y, car_speed, boost_active 
    global boost_start_time, coin_score, obstacle_y, second_obstacle_y, second_obstacle_visible, carapace_x, carapace_y, coin_x , coin_y
    global obstacle_speed, coin_speed

    # Réinitialiser la position de la voiture
    car_x = SCREEN_WIDTH // 2 - car_width // 2
    car_y = SCREEN_HEIGHT - car_height - 10
    car_speed = 0
    obstacle_speed = 5
    boost_active = False
    boost_start_time = 0
    coin_score = 0  # Réinitialiser le score des pièces
    obstacle_y = -600  # Réinitialiser la position de l'obstacle
    second_obstacle_y = -600  # Réinitialiser la position du deuxième obstacle
    second_obstacle_visible = False
    carapace_x, carapace_y = None, None  # Réinitialiser la carapace
    coin_speed = 5
    coin_x = random.randint(0, SCREEN_WIDTH - coin_width)
    coin_y = random.randint(-600, -coin_height)  # Apparition aléatoire au-dessus de l'écran

# Modifier l'action du bouton "Rejouer" pour appeler reset_game et relancer la boucle du jeu
def replay_game():
    reset_game()  # Appeler la fonction pour tout réinitialiser
    game_loop()   # Redémarrer le jeu


# Fonction principale du jeu
def game_loop():
    pygame.mixer.music.stop()  # Arrêter la musique de démarre dès que game_loop commence
    global car_x, car_y, car_speed, obstacle_x, obstacle_y, obstacle_speed, road_color
    global second_obstacle_x, second_obstacle_y, second_obstacle_visible, second_obstacle_timer
    global boost_active, boost_start_time, normal_speed, boost_speed , elapsed_time
    global coin_x, coin_y, coin_score , score
    

    clock = pygame.time.Clock()
    running = True
    score = 0
    start_time = pygame.time.get_ticks()  # Temps de début
    obstacle_timer = pygame.time.get_ticks()  # Timer pour le nouvel obstacle

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Contrôles de la voiture
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_speed = -normal_speed if not boost_active else -boost_speed
                elif event.key == pygame.K_RIGHT:
                    car_speed = normal_speed if not boost_active else boost_speed
                elif event.key == pygame.K_SPACE and not boost_active:  # Activation du boost
                    boost_active = True
                    boost_start_time = pygame.time.get_ticks()  # Démarrer le timer du boost

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_speed = 0

            # Ajouter le code pour détecter la touche "S"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    launch_carapace()

        # Gestion du boost
        if boost_active:
            if pygame.time.get_ticks() - boost_start_time > boost_duration:
                boost_active = False  # Désactiver le boost après la durée
            else:
                car_speed = boost_speed if car_speed > 0 else -boost_speed  # Garder la direction actuelle

        # Mouvement de la voiture
        car_x += car_speed
        if car_x < 0:
            car_x = 0
        elif car_x > SCREEN_WIDTH - car_width:
            car_x = SCREEN_WIDTH - car_width
        
        # Mouvement de la pièce
        coin_y += coin_speed
        if coin_y > SCREEN_HEIGHT:  # Réinitialiser la pièce après qu'elle ait quitté l'écran
            coin_y = random.randint(-600, -coin_height)
            coin_x = random.randint(0, SCREEN_WIDTH - coin_width)


        # Mouvement de l'obstacle
        obstacle_y += obstacle_speed
        if obstacle_y > SCREEN_HEIGHT:
            obstacle_y = -obstacle_height
            obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
            score += 1
            obstacle_speed += 0.5  # Augmente la vitesse au fur et à mesure

        # Gestion du deuxième obstacle
        if pygame.time.get_ticks() - obstacle_timer > 10000:  # Vérifier si 10 secondes se sont écoulées
            second_obstacle_visible = True
            second_obstacle_timer = pygame.time.get_ticks()  # Démarrer le timer pour la durée de visibilité
            second_obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)  # Nouvelle position
            obstacle_timer = pygame.time.get_ticks()  # Réinitialiser le timer

        if second_obstacle_visible:
            second_obstacle_y += obstacle_speed  # Faire descendre le deuxième obstacle
            if second_obstacle_y > SCREEN_HEIGHT or pygame.time.get_ticks() - second_obstacle_timer > 3000:
                second_obstacle_visible = False  # Cacher le deuxième obstacle après 3 secondes
                second_obstacle_y = -obstacle_height  # Réinitialiser la position de Y

        # Détection des collisions
        if (car_x < obstacle_x + obstacle_width and
            car_x + car_width > obstacle_x and
            car_y < obstacle_y + obstacle_height and
            car_y + car_height > obstacle_y):
            explosion_sound.play()  # Jouer le son d'explosion
            print("Collision avec l 'obstacle  principale! Score final :", score)
            pygame.time.delay(3000)  # Délai pour laisser le son jouer un peu avant de l'arrêter 
            explosion_sound.stop()  # Arrêter le son d'explosion
            running = False
            game_over()  # Appeler la fonction game_over

        if second_obstacle_visible and car_y < second_obstacle_y + obstacle_height and car_y + car_height > second_obstacle_y:
            if car_x < second_obstacle_x + obstacle_width and car_x + car_width > second_obstacle_x:
                explosion_sound.play()  # Jouer le son d'explosion
                print("Collision avec le deuxième obstacle ! Score final :", score)
                pygame.time.delay(500)  # Délai pour laisser le son jouer un peu avant de l'arrêter (facultatif)
                explosion_sound.stop()  # Arrêter le son d'explosion
                running = False
                game_over()  # Appel de game_over 

         # Détection de collision avec la pièce
        if car_y < coin_y + coin_height and car_y + car_height > coin_y:
            if car_x < coin_x + coin_width and car_x + car_width > coin_x:
                piece_sound.play()
                coin_score += 1
                coin_y = random.randint(-600, -coin_height)
                coin_x = random.randint(0, SCREEN_WIDTH - coin_width)

        # Affichage du jeu
        screen.fill(road_color)
        draw_car(car_x, car_y)
        draw_coin(coin_x, coin_y)

        # Afficher la route
        draw_road()

        # Afficher la voiture et les obstacles
        draw_car(car_x, car_y)
        draw_obstacle(obstacle_x, obstacle_y)

        if second_obstacle_visible:
            draw_second_obstacle(second_obstacle_x, second_obstacle_y)

        # Afficher le score
        font = pygame.font.SysFont(None, 35)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # Texte des pièces avec traduction selon la langue
        coin_text = font.render(f"{'Pièces' if current_language == 'fr' else 'Coins'}: {coin_score}", True, YELLOW)

        screen.blit(coin_text, (10, 40))

        # Afficher le timer
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convertir en secondes
        # Texte du timer avec traduction selon la langue
        timer_text = font.render(f"{'Temps' if current_language == 'fr' else 'Time'}: {elapsed_time}s", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))  # Positionner le timer à droite

        # Afficher un indicateur de boost
        if boost_active:
            boost_text = font.render("Boost Actif!", True, YELLOW)
            screen.blit(boost_text, (SCREEN_WIDTH // 2 - boost_text.get_width() // 2, 50))

        # Dans la boucle principale du jeu après la détection d'événements et le mouvement de la voiture
        move_carapace()  # Gérer le déplacement et la collision de la carapace
        draw_carapace()  # Afficher la carapace si elle a été lancée


        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Lancer l'écran d'introduction
game_intro()